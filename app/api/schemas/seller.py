from pydantic import BaseModel, ConfigDict, EmailStr


class BaseSeller(BaseModel):
    name: str
    email: EmailStr


class SellerRead(BaseSeller):
    model_config = ConfigDict(from_attributes=True)


class SellerCreate(BaseSeller):
    password: str
    address: str
    zip_code: int
