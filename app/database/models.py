from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import List
from pydantic import EmailStr
from sqlalchemy import Column
from sqlmodel import Relationship, SQLModel,Field
from uuid import uuid4,UUID
from sqlalchemy.dialects import postgresql  
from sqlalchemy import ARRAY, INTEGER
class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancled ="cancled"

class Shipment (SQLModel, table =True): 
    __tablename__='shipment'
    
    id: UUID = Field(
        sa_column = Column(
            postgresql.UUID(),
            default = uuid4,
            primary_key = True,
        )
    )
    content: str
    weight: float = Field(le=25)
    destenation: int
    
    estimated_delivery: datetime
    seller_id : UUID = Field(foreign_key = "seller.id")
    created_at: datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default = datetime.now,
        )
    )
    seller : "Seller" = Relationship(
        back_populates = "shipments",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
    delivery_partner_id : UUID =Field(foreign_key = "delivery_partner.id")
    delivery_partner : "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
    timeline :List["ShipmentEvent"]=Relationship(
        back_populates="shipment",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
    client_contact_email :EmailStr | None
    client_contact_phone: str | None
    review :"Review" =Relationship(
        back_populates="shipment",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
    @property
    def status(self):
        if not self.timeline:
            return None
    
        sorted_timeline = sorted(self.timeline, key=lambda event: event.created_at)
        return sorted_timeline[-1].status
    
       
class ShipmentEvent(SQLModel, table = True):
    __tablename__='shipments_event'
    id: UUID = Field(
        sa_column = Column(
            postgresql.UUID(),
            default = uuid4,
            primary_key = True,
        )
    )
    created_at: datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default = datetime.now,
        )
    )
    location:int 
    status: ShipmentStatus
    description : str| None =Field(default= None)
    shipment_id : UUID = Field(foreign_key='shipment.id')
    shipment :Shipment =Relationship(
        back_populates="timeline",
        sa_relationship_kwargs={"lazy":"selectin"}
        
    )
    
class User(SQLModel):
    name:str
    email:EmailStr
    password_hash: str
    email_verified :bool = Field(default = False)
    
class Seller(User, table= True):
    __tablename__='seller'
    id: UUID = Field(
        sa_column = Column(
            postgresql.UUID(),
            default = uuid4,
            primary_key = True,
        )
    )
    created_at: datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default = datetime.now,
        )
    )
    shipments:list[Shipment]=Relationship(
        back_populates ="seller",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
    address: str | None = Field(default=None)
    zip_code :int | None = Field(default=None)
    
class DeliveryPartner(User, table= True):
    __tablename__='delivery_partner'
    id: UUID = Field(
        sa_column = Column(
            postgresql.UUID(),
            default = uuid4,
            primary_key = True,
        )
    )   
    serviceable_zib_codes : List[int] = Field(
        sa_column = Column(postgresql.ARRAY(INTEGER))
    )
    created_at: datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default = datetime.now,
        )
    )
    max_handling_capacity : int
    shipments : List["Shipment"] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
    @property
    def active_shipments(self):
        shipments_list = self.shipments or [] 
        return [
            shipment 
            for shipment in shipments_list
            if shipment.status != ShipmentStatus.delivered and shipment.status != ShipmentStatus.cancled 
        ]
    @property  
    def current_handling_capacity(self):
        return self.max_handling_capacity -len(self.active_shipments)
    
    
class Review(SQLModel, table = True):
    __tablename__='review'
    id: UUID = Field(
        sa_column = Column(
            postgresql.UUID(),
            default = uuid4,
            primary_key = True,
        )
    )   
   
    created_at: datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default = datetime.now,
        )
    )
    rating : int =Field(ge = 1, le= 5)
    comment :str | None = Field(default = None)
    shipment_id : UUID= Field(foreign_key="shipment.id")
    shipment :Shipment =Relationship(
        back_populates="review",
        sa_relationship_kwargs={"lazy":"selectin"}
    )