
from datetime import datetime
from typing import List
from unittest.mock import Base
from uuid import UUID

from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
from app.database.models import Seller, ShipmentEvent, ShipmentStatus, Tag, TagName



class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destenation: int 
    
class TagRead(BaseModel):
    name: TagName
    instruction: str

class Shipment(BaseShipment):
    id : UUID
    seller: Seller
    timeline : list[ShipmentEvent]
    estimated_delivery:datetime
    tags:List[TagRead]


class ShipmentCreate(BaseShipment):
    client_contact_email:EmailStr
    client_contact_phone: str | None = Field(default= None)
    

class ShipmentUpdate(BaseModel):
    location : int | None = Field(default= None)
    status: ShipmentStatus | None = Field(default= None)
    verification_code : str | None =Field(default = None)
    description : str | None = Field(default= None)
    estimated_delivery:datetime | None = Field(default= None) # type: ignore
    
    
class ShipmentReview(BaseModel):
    rating: int = Field(ge = 1, le = 5)
    comment: str | None = Field(default = None)