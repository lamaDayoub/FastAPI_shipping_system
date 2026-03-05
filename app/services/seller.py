from datetime import datetime, timedelta

from fastapi import HTTPException, status
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from passlib.context import CryptContext
from app.config import security_settings


password_context = CryptContext(
    schemes=['bcrypt']
)
class SellerService():
    def __init__(self,session:AsyncSession):
        self.session = session
        
    async def add(self, credentials: SellerCreate )-> Seller:
        seller = Seller(
           **credentials.model_dump(exclude=['password']),
           password_hash = password_context.hash(credentials.password)
           
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
    
    async def token(self, email, password)-> str:
        #validate the credential 
        result = await self.session.execute(
         select(Seller).where(Seller.email == email)
        )
        seller = result.scalar()
        if  seller is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='seller with given email is not found ')
        
        true_password = password_context.verify(
            password,
            seller.password_hash
        )
        if not true_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid password')
        
        token = jwt.encode(
            payload={
                "user":{
                    'name':seller.name,
                    'email':seller.email
                },
                "exp": datetime.now()+timedelta(days = 1)
            },
            algorithm =security_settings.JWT_ALGORITHM,
            key = security_settings.JWT_SECRET_KEY
            
        )
        return token
        
            