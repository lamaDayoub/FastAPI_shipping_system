from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import SellerServiceDep, SessionDep, _get_access_token
from app.api.schemas.seller import SellerRead, SellerCreate

from app.database.models import Seller
from app.database.redis import add_jti_to_blacklist



router = APIRouter(prefix='/seller', tags=['Seller'])


@router.post('/signup', response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    
    return await service.add(seller)

@router.post('/token')
async def login_seller(
    request_form: Annotated[ OAuth2PasswordRequestForm,Depends()] ,
    service :SellerServiceDep
):
    token = await service.token(request_form.username,request_form.password)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
@router.get('/logout')
async def logout_seller(token : Annotated[str,Depends(_get_access_token)]):
    await add_jti_to_blacklist(token["jti"])
    return{
        'detail': "Successfully logged out"
    }
    

@router.get('/verify')
async def verify_seller_email(token : str, service :SellerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account verified!"}