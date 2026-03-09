from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException, status
from app.database.models import Seller
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import oauth2_scheme
from app.utils import decode_access_token


SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session : SessionDep):
    return ShipmentService(session)

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

def get_seller_service(session: SessionDep):
    return SellerService(session)

SellerServiceDep = Annotated[ SellerService, Depends(get_seller_service)]


async def get_access_token(token:Annotated[str,Depends(oauth2_scheme)])->dict:
    data= decode_access_token(token)
    if data is None or await is_jti_blacklisted(data["jti"]) :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid  or expired access token')
    return data

async def get_current_seller(token : Annotated[str,Depends(get_access_token)],
                             session:SessionDep
):
    return  await session.get(Seller,UUID(token['user']['id']))

sellerDep = Annotated[Seller,Depends(get_current_seller)]