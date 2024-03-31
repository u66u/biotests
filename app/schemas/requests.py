from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from decimal import Decimal
from datetime import datetime, date
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


class ProductCreateRequest(BaseRequest):
    name: str
    description: Optional[str] = None
    price: float

    @validator("price")
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price must be a positive number.")
        return value


class BloodTestCreateRequest(BaseRequest):
    name: str
    description: Optional[str]
    price: Decimal
    glucose: Optional[float]
    cholesterol: Optional[float]


class OrderCreateRequest(BaseRequest):
    test_id: str
    comments: Optional[str]


class BloodTestBaseRequest(BaseRequest):
    birthday: date
    sex: str


class BloodMarketBAEstimationTestCreateRequest(BloodTestBaseRequest):
    albumin: Optional[float]
    alkaline_phosphatase: Optional[float]
    urea: Optional[float]
    cholesterol: Optional[float]
    creatinine: Optional[float]
    cystatin_c: Optional[float]
    glycated_haemoglobin: Optional[float]
    log_c_reactive_protein: Optional[float]
    log_gamma_glutamyltransf: Optional[float]
    red_blood_cell_erythrocyte_count: Optional[float]
    mean_corpuscular_volume: Optional[float]
    red_blood_cell_erythrocyte_distribution_width: Optional[float]
    monocyte_count: Optional[float]
    neutrophill_count: Optional[float]
    lymphocyte_percentage: Optional[float]
    mean_sphered_cell_volume: Optional[float]
    log_alanine_aminotransfe: Optional[float]
    log_shbg: Optional[float]
    log_vitamin_d: Optional[float]
    high_light_scatter_reticulocyte_percentage: Optional[float]
    glucose: Optional[float]
    platelet_distribution_width: Optional[float]
    mean_corpuscular_haemoglobin: Optional[float]
    platelet_crit: Optional[float]
    apolipoprotein_a: Optional[float]


class DNAmPhenoAgeLevine2018TestRequest(BloodTestBaseRequest):
    albumin: Optional[float]
    creatinine: Optional[float]
    glucose: Optional[float]
    c_reactive_protein: Optional[float]
    lymphocytes_percentage: Optional[float]
    mean_corpuscular_volume: Optional[float]
    red_blood_cell_distribution_width: Optional[float]
    alkaline_phosphatase: Optional[float]
    white_blood_cell_count: Optional[float]
