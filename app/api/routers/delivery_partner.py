from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import   DeliveryPartnerServiceDep, get_partner_access_token,DeleviryPartnerDep
from app.api.schemas.delivery_partner import DeliveryPartnerRead, DeliveryPartnerCreate, DeliveryPartnerUpdate
from app.database.redis import add_jti_to_blacklist



router = APIRouter(prefix='/partner', tags=['Delivery Partner'])


@router.post('/signup', response_model=DeliveryPartnerRead)
async def register_delivery_partner(delivery_partner: DeliveryPartnerCreate, service:DeliveryPartnerServiceDep):
    
    return await service.add(delivery_partner)

@router.post('/token')
async def login_delivery_partner(
    request_form: Annotated[ OAuth2PasswordRequestForm,Depends()] ,
    service :DeliveryPartnerServiceDep
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
    
   

@router.post('/', response_model= DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeleviryPartnerDep,
    service:DeliveryPartnerServiceDep
):
    
    update = partner_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    # return await service.update(
    #     partner.sqlmodel_update(update),
    # )
    # 1. Update the partner object with the data 
    partner.sqlmodel_update(partner_update.model_dump(exclude_none=True))

    # 2. Now 'partner' is updated, so we save it and return the actual object
    return await service.update(partner)
    