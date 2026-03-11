from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import   get_partner_access_token,DeleviryPartnerDep
from app.api.schemas.delivery_partner import DeliveryPartnerRead, DeliveryPartnerCreate, DeliveryPartnerUpdate
from app.database.redis import add_jti_to_blacklist



router = APIRouter(prefix='/partner', tags=['Delivery Partner'])


@router.post('/signup', response_model=DeliveryPartnerRead)
async def register_delivery_partner(delivery_partner: DeliveryPartnerCreate, service):
    
    return await service.add(delivery_partner)

@router.post('/token')
async def login_delivery_partner(
    request_form: Annotated[ OAuth2PasswordRequestForm,Depends()] ,
    service 
):
    token = await service.token(request_form.username,request_form.password)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
@router.get('/logout')
async def logout_delivery_partner(token : Annotated[str,Depends(get_partner_access_token)]):
    await add_jti_to_blacklist(token["jti"])
    return{
        'detail': "Successfully logged out"
    }
    
   

@router.post('/')
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeleviryPartnerDep,
    service
):
    pass