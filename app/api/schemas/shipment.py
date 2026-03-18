
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from app.database.models import Seller, ShipmentEvent, ShipmentStatus



class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destenation: int 
    


class Shipment(BaseShipment):
    id : UUID
    seller: Seller
    timeline : list[ShipmentEvent]
    estimated_delivery:datetime


class ShipmentCreate(BaseShipment):
    pass
    

class ShipmentUpdate(BaseModel):
    location : int | None = Field(default= None)
    status: ShipmentStatus | None = Field(default= None)
    description : str | None = Field(default= None)
    estimated_delivery:datetime | None = Field(default= None) # type: ignore