from fastapi import HTTPException, status
from sqlmodel import select
from app.database.models import User
from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import generate_access_token
from passlib.context import CryptContext



password_context = CryptContext(
    schemes=['bcrypt']
)


class UserService(BaseService):
    def __init__(self, model: User , session: AsyncSession):
        super().__init__(model, session)
        
    async def _add_user(self, data:dict):
        user_data = data.model_dump(exclude={'password'})
        user = self.model(
            **user_data,
            password_hash = password_context.hash(data.password) # Access .password directly
        )
        return await self._add(user)
    
    
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
        
        return generate_access_token(
            data={
                "user":{
                    'name':user.name,
                    'id': str(user.id )  
                } 
            }
        )
        
        