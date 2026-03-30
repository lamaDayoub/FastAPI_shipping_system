from random import randint

from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.database.redis import add_shipment_verification_code
from app.services.base import BaseService
from app.config import  app_settings
from app.utils import generate_url_safe_token
from app.worker.tasks import send_email_with_template, send_sms

class ShipmentEventService(BaseService):
    def __init__(self,session ):
        super().__init__(ShipmentEvent, session)
        
        
    async def add(
        self,
        shipment:Shipment,
        location:int =None,
        status:ShipmentStatus =None,
        description:str =None
    ) -> ShipmentEvent:
        print("!!! EVENT SERVICE ADD CALLED !!!")
        if not location or not status:
        # If there's no timeline or it's empty, we can't get a 'last_event'
            if not shipment.timeline or len(shipment.timeline) == 0:
                # Provide defaults if it's the very first event
                location = location or 0 
                status = status or ShipmentStatus.placed
            else:
                # Only do this if a timeline actually exists
                last_event = await self.get_latest_event(shipment)
                location = location if location else last_event.location
                status = status if status else last_event.status
        
        # if not location or not status:
        #     last_event = await self.get_latest_event(shipment)
        #     location = location if location else last_event.location
        #     status = status if status else last_event.status
        new_event = ShipmentEvent(
            location=location,
            status = status,
            description= description
            if description 
            else self._generate_description(
                status,location
            ),
            shipment_id= shipment.id
        )
        await self._notify(shipment,status)
        return await self._add(new_event)
    
    async def get_latest_event(self,shipment:Shipment):
        timeline = shipment.timeline
        if not timeline:
            return None
    
        sorted_timeline = sorted(shipment.timeline, key=lambda event: event.created_at)
        return sorted_timeline[-1]
        # timeline.sort(key = lambda event : event.created_at)
        # return timeline[-1]
    
    def _generate_description(self,  status:ShipmentStatus, location :int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.delivered:
                return "successfully deliveredr"
            case ShipmentStatus.out_for_delivery:
                return "shipment out for delivery"
            case ShipmentStatus.cancled:
                return "cancled by the seller"
            case _:
                return f'scanned at{location}'
            
    async def _notify(self, shipment: Shipment, status: ShipmentStatus):
        
        if status == ShipmentStatus.in_transit:
            return

        subject: str
        context = {}
        template_name: str

        match status:
            case ShipmentStatus.placed:
                subject="Your Order is Shipped 🚛"
                context["seller"] = shipment.seller.name
                context["id"] = shipment.id
                context["partner"] = shipment.delivery_partner.name
                template_name="mail_placed.html"

            case ShipmentStatus.out_for_delivery:
                subject="Your Order is Arriving Soon 🛵"
                template_name = "mail_out_for_delivery.html"
                # ... inside Case ShipmentStatus.out_for_delivery ...

                code = randint(100000, 999999)
                print(f"DEBUG: Saving code {code} to Redis")

                # 1. Save to Redis (This happens first)
                await add_shipment_verification_code(shipment.id, code)

                # 2. Trigger SMS (Now non-blocking)
                if shipment.client_contact_phone:
                    # REMOVE 'await' from this line:
                    send_sms.delay(
                        to=shipment.client_contact_phone,
                        body=f"Your order is arriving soon! share this {code} with your delivery excutive"
                    )
                else:
                    context["verification_code"] = code
                
                    
                
            case ShipmentStatus.delivered:
                subject = "Your Order is Delivered ✅"
                context["seller"] = shipment.seller.name
                token=generate_url_safe_token({"id":str(shipment.id)})
                context["review_url"]=f"http://{app_settings.APP_DOMAIN}/shipment/review?token={token}"
                template_name = "mail_delivered.html"

            case ShipmentStatus.cancled:
                subject = "Your Order is cancled ❌"
                template_name = "mail_cancelled.html"

        send_email_with_template.delay(
            recipients=[shipment.client_contact_email],
            subject=subject,
            context=context,
            template_name=template_name,
        )
