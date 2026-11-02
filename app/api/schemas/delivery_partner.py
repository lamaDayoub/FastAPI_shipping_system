from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    serviceable_zib_codes: list[int]
    max_handling_capacity: int


class DeliveryPartnerRead(BaseDeliveryPartner):
    model_config = ConfigDict(from_attributes=True)


class DeliveryPartnerUpdate(BaseModel):
    serviceable_zib_codes: list[int] | None = Field(default=None)
    max_handling_capacity: int | None = Field(default=None)


class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str
