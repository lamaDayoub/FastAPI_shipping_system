from typing import Annotated
from uuid import UUID
from fastapi import BackgroundTasks, Depends, HTTPException, status
from app.database.models import Seller,DeliveryPartner
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.services.delivery_partner import DeliveryPartnerService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import oauth2_scheme_seller, oauth2_scheme_partner
from app.services.shipment_event import ShipmentEventService
from app.utils import decode_access_token


SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session : SessionDep, tasks: BackgroundTasks):
    return ShipmentService(
        session,
        DeliveryPartnerService(session,tasks),
        ShipmentEventService(session, tasks)
    )

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

def get_seller_service(session: SessionDep, tasks:BackgroundTasks):
    return SellerService(session, tasks)

SellerServiceDep = Annotated[ SellerService, Depends(get_seller_service)]


async def _get_access_token(token:str)->dict:
    data= decode_access_token(token)
    if data is None or await is_jti_blacklisted(data["jti"]) :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid  or expired access token')
    return data

async def get_seller_access_token(token: Annotated[str,Depends(oauth2_scheme_seller)])->dict:
    return await _get_access_token(token)


async def get_current_seller(token : Annotated[str,Depends(get_seller_access_token)],
                             session:SessionDep
):
    seller = await session.get(Seller,UUID(token['user']['id']))
    if seller is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not authorized')
    
    return seller

sellerDep = Annotated[Seller,Depends(get_current_seller)]


async def get_partner_access_token(token: Annotated[str,Depends(oauth2_scheme_partner)])->dict:
    return await _get_access_token(token)
    


async def get_current_partner(token : Annotated[str,Depends(get_partner_access_token)],
                             session:SessionDep
):
    partner =  await session.get(DeliveryPartner,UUID(token['user']['id']))
    if partner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not authorized')
    
    return partner

DeleviryPartnerDep = Annotated[DeliveryPartner,Depends(get_current_partner)]


def get_delivery_partner_service(session:SessionDep, tasks:BackgroundTasks):
    return DeliveryPartnerService(session, tasks)

DeliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService,
    Depends(get_delivery_partner_service)
]