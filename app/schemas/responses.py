from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


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


class ProductResponse(BaseResponse):
    id: str
    name: str
    description: Optional[str]
    price: float


class OrderResponse(BaseResponse):
    id: str
    user_id: str
    test_id: str
    comments: Optional[str]
    created_at: datetime
    updated_at: datetime


class UserResponse(BaseResponse):
    id: str
    email: EmailStr
    name: Optional[str]


class BloodTestBaseResponse(BaseResponse):
    user_id: str
    result: float
    created_at: datetime


class BloodMarketBAEstimationTestResponse(BloodTestBaseResponse): ...


class DNAmPhenoAgeLevine2018TestResponse(BloodTestBaseResponse): ...
