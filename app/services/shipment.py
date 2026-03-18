     
from datetime import datetime, timedelta
from http.client import UNAUTHORIZED
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.database.models import DeliveryPartner, Seller, Shipment, ShipmentStatus
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
        
        

    # Update an existing shipment
    async def update(
        self,
        id: UUID,
        shipment_update: ShipmentUpdate,
        partner: DeliveryPartner
    ) -> Shipment:
        shipment = await self.get(id)
    
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = 'the shipment with the provided id id not exsist'
            )
        if shipment.delivery_partner_id != partner.id :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authorized'
            )
        update = shipment_update.model_dump(exclude_none= True)
        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery
        if len(update) >1 or not shipment_update.estimated_delivery: 
            await self.event_service.add(
                shipment= shipment,
                **update     
            )
            
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
        
        