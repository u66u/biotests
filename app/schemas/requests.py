from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.models.biological_test import TestType


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


class ProductCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

    @validator("price")
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price must be a positive number.")
        return value


class BloodTestCreateRequest(BaseModel):
    name: str
    description: Optional[str]
    price: Decimal
    glucose: Optional[float]
    cholesterol: Optional[float]


class DNATestCreateRequest(BaseModel):
    name: str
    description: Optional[str]
    price: Decimal
    gene1: Optional[str]
    gene2: Optional[str]


class OrderCreateRequest(BaseModel):
    test_id: str
    comments: Optional[str]
