from typing import List

from pydantic import BaseModel, EmailStr



class BaseDeliveryPartner(BaseModel):
    name:str
    email:EmailStr
    max_handling_capacity : int
    serviceable_zib_codes : List[int]
    
class DeliveryPartnerRead(BaseDeliveryPartner):
    pass


class DeliveryPartnerUpdate(BaseModel):
    max_handling_capacity : int
    serviceable_zib_codes : List[int]

class DeliveryPartnerCreate(BaseDeliveryPartner):
    
    password: str