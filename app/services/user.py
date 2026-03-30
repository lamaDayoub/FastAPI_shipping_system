from datetime import timedelta
from uuid import UUID

from fastapi import  HTTPException, status
from sqlmodel import select
from app.database.models import User
from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import generate_access_token, generate_url_safe_token
from passlib.context import CryptContext
from app.config import app_settings
from app.utils import decode_url_safe_token
from app.worker.tasks import send_email_with_template

password_context = CryptContext(
    schemes=['bcrypt']
)


class UserService(BaseService):
    def __init__(self, model: User , session: AsyncSession):
        super().__init__(model, session)
        
        
    async def _add_user(self, data:dict, router_prefix: str)-> User:
        user_data = data.model_dump(exclude={'password'})
        user = self.model(
            **user_data,
            password_hash = password_context.hash(data.password) # Access .password directly
        )
        user = await self._add(user)
        token = generate_url_safe_token({
            "email":user.email,
            "id":str(user.id)
        })
        send_email_with_template.delay(
            recipients=[user.email],
            subject="Verify your Account with FastShip",
            context = {
                "username":user.name,
                "verification_url":f'http://{app_settings.APP_DOMAIN}/{router_prefix}/verify?token={token}'
            },
            template_name='mail_email_verify.html'
        )
        
        return user
    
    
    async def _get_by_email(self, email)-> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )
    
    async def _generate_token(self, email, password):
        user = await self._get_by_email(email)
        
        if  user  is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user with given email is not found ')
        
        true_password = password_context.verify(
            password,
            user.password_hash
        )
        if not true_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid password')
        if not user.email_verified:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail ="Email not verified"
            )
        return generate_access_token(
            data={
                "user":{
                    'name':user.name,
                    'id': str(user.id )  
                } 
            }
        )
    async def verify_email(self, token: str):
        token_data= decode_url_safe_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
        user = await self._get(UUID(token_data["id"]))
        user.email_verified = True
        await self._update(user)
        
        
    async def send_password_reset_email(self,email, router_prefix: str):
        user = await self._get_by_email(email)
        token = generate_url_safe_token(
            {
                "id":str(user.id)
            },
            salt = "password-reset"
        )
        send_email_with_template.delay(
            recipients=[user.email],
            subject = "Fastship Account Password Reset",
            context={
              "username":user.name,
              "reset_url" :f'http://{app_settings.APP_DOMAIN}{router_prefix}/reset_password_form?token={token}' 
            },
            template_name="mail_password_reset.html"
        )
        
    async def reset_password(self, token : str, password: str)-> bool:
        token_data = decode_url_safe_token(
            token, 
            salt = "password-reset",
            expiry = timedelta(days=1)
        )
        if not token_data :
            return False
        user =  await self._get(UUID(token_data["id"]))
        user.password_hash= password_context.hash(password)
        await self._update(user)
        return True