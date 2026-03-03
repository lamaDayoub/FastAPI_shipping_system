from pydantic import BaseModel, EmailStr

class SellerCreate():
    name: str
    email: EmailStr
    password: str