from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str
    name: Optional[str]
    address: Optional[str]


class ProductCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

    @validator("price")
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price must be a positive number.")
        return value


class OrderCreateRequest(BaseModel):
    user_id: str
    product_id: str
    comments: Optional[str] = None
