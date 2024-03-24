from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from app.models.biological_test import TestType


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class ProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float


class BloodTestResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: Decimal
    test_type: TestType
    glucose: Optional[float]
    cholesterol: Optional[float]
    created_at: datetime
    updated_at: datetime


class DNATestResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: Decimal
    test_type: TestType
    gene1: Optional[str]
    gene2: Optional[str]
    created_at: datetime
    updated_at: datetime


class OrderResponse(BaseModel):
    id: str
    user_id: str
    test_id: str
    comments: Optional[str]
    created_at: datetime
    updated_at: datetime


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str]
