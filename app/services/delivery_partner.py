

from sqlmodel import Sequence, any_, select
from fastapi import HTTPException,status
from app.api.schemas.delivery_partner import DeliveryPartnerCreate
from app.core.exceptions import DeliveryPartnerNotAvailable
from app.database.models import DeliveryPartner, Shipment
from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session):
        super().__init__(DeliveryPartner,session)
        
    async def add(self, delivery_partner: DeliveryPartnerCreate):
        
        return await self._add_user(
            delivery_partner,
            'partner'
        )
    
    async def get_partner_by_zipcode(self,zipcode: int) -> Sequence[DeliveryPartner]:
        return (
            await self.session.scalars(
                select(DeliveryPartner).where(
                    zipcode == any_( DeliveryPartner.serviceable_zib_codes)
                )
            )
        ).all()
        
    async def assign_shipment(self,shipment: Shipment):
        eligible_partners = await self.get_partner_by_zipcode(shipment.destenation)
        
        for partner in eligible_partners:
            if partner.current_handling_capacity >0 :
               
                partner.shipments.append(shipment)
                await self.update(partner)
                return partner
        raise DeliveryPartnerNotAvailable()
                
            
        
    
    async def update(self,partner: DeliveryPartner):
        return await self._update(partner)
    
    async def token(self, email, password)-> str:
        return await self._generate_token(email,password)
        