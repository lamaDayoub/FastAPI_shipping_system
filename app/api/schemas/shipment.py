
from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from app.database.models import ShipmentStatus



class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destenation: int 
    


class Shipment(BaseShipment):
    id : int =Field(default= None , primary_key= True)
    status: ShipmentStatus
    estimated_delivery:datetime


class ShipmentCreate(BaseShipment):
    pass
    

class ShipmentUpdate(BaseModel):
    
    status: ShipmentStatus | None = Field(default= None)
    estimated_delivery:datetime | None = Field(default= None) # type: ignore