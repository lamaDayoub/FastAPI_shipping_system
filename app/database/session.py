from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlmodel import SQLModel,Session 
from app.config import settings
from sqlalchemy.orm import sessionmaker
engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True,
    
    
)

async def create_db_tables():
    async with engine.begine() as connection:
        from app.schemas import Shipment
        await connection.run_sync(
            SQLModel.metadata.create_all
        )
       
    


async def get_session():
    async_session = sessionmaker(
        bind= engine,
        class_ = AsyncSession,
        expire_on_commit= False,
        
    )
    async with async_session( ) as session:
        yield session
    
SessionDep = Annotated[AsyncSession, Depends(get_session)]