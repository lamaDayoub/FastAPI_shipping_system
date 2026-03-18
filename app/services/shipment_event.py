from functools import cache

from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService
from app.services.notification import NotificationService


class ShipmentEventService(BaseService):
    def __init__(self,session ,tasks):
        super().__init__(ShipmentEvent, session)
        self.notification_service = NotificationService(tasks)
        
        
    async def add(
        self,
        shipment:Shipment,
        location:int =None,
        status:ShipmentStatus =None,
        description:str =None
    ) -> ShipmentEvent:
        
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
            
    async def _notify(self, shipment:Shipment, status:ShipmentStatus):
        match status:
            case ShipmentStatus.placed:
                await self.notification_service.send_message(
                    recipients= [shipment.client_contact_email],
                    subject = "Your order is shipped",
                    body= f"Your order with {shipment.seller.name}"
                    f" is picked up by {shipment.delivery_partner.name} "
                    " and it is on way to you."
                ) 
            
            case ShipmentStatus.out_for_delivery:
                await self.notification_service.send_message(
                    recipients= [shipment.client_contact_email],
                    subject = "Your order is Arriving",
                    body= "Our delivery excutive is on their way to delivery your order ."
                    "Please ensure you are available "
                    " to recieve the same"
                   
                )
        