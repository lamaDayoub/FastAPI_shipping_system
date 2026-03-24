     
from datetime import datetime, timedelta
from http.client import UNAUTHORIZED
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.database.models import DeliveryPartner, Seller, Shipment, ShipmentStatus
from app.database.redis import get_shipment_verification_code
from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService
from app.services.shipment_event import ShipmentEventService

class ShipmentService(BaseService):
    def __init__(
        self, 
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventService
        
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service
        self.event_service = event_service

    # Get a shipment by id 
    async def get(self, id: UUID) -> Shipment | None:
        return await self._get( id)

    # Add a new shipment
    async def add(self, shipment_create: ShipmentCreate, seller : Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id= seller.id
        )
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        shipment = await self._add(new_shipment)
        event = await self.event_service.add(
            shipment=shipment,  
            location = seller.zip_code,
            status = ShipmentStatus.placed,
            description = f'assigned to {partner.name}'
        )
        shipment.timeline.append(event)
        return shipment
        
        
    async def update(
        self,
        id: UUID,
        shipment_update: ShipmentUpdate,
        partner: DeliveryPartner
    ) -> Shipment:
        # 1. Fetch the shipment
        shipment = await self.get(id)

        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='The shipment with the provided ID does not exist'
            )

        # 2. Authorization: Check if this partner owns this shipment
        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authorized to update this shipment'
            )

        # 3. VERIFICATION CHECK: If status is 'delivered', we MUST check Redis
        if shipment_update.status == ShipmentStatus.delivered:
            # We fetch the code stored in Redis DB 1
            stored_code = await get_shipment_verification_code(shipment.id)
            
            # Compare stored code with the one provided in the request body
            if str(stored_code) != str(shipment_update.verification_code):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid verification code. Client not authorized to receive."
                )
            print(f"DEBUG: Verification successful for shipment {shipment.id}")

        # 4. Prepare data for the ShipmentEvent (Status/Location)
        event_data = shipment_update.model_dump(
            exclude_none=True,
            exclude=["verification_code", "estimated_delivery"]
        )

        # 5. Update main Shipment fields (Estimated Delivery)
        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery

        # 6. Create the Timeline Event (This triggers _notify / Redis SET / SMS)
        if event_data: 
            await self.event_service.add(
                shipment=shipment,
                **event_data     
            )
            
        # 7. Final Commit to Database
        return await self._update(shipment)

    # Delete a shipment
    async def delete(self, id: UUID) -> None:
        await self._delete(await self._get(id))
        
    async def cancel(self, id:UUID, seller:Seller)-> Shipment:
        shipment = await self.get(id)
        if shipment.seller_id != seller.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authorized'
            )
            
        event =  await self.event_service.add(
            shipment= shipment,
            status = ShipmentStatus.cancled
        )
        shipment.timeline.append(event)
        return shipment
        
        