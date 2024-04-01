from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from decimal import Decimal
from datetime import datetime, date
from app.models.biological_test import TestType


class BaseRequest(BaseModel): ...


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


class OrderCreateRequest(BaseRequest):
    test_id: str
    comments: Optional[str]


class BloodTestBaseRequest(BaseRequest):
    birthday: date
    sex: str


class BloodMarketBAEstimationTestCreateRequest(BloodTestBaseRequest):
    albumin: float
    alkaline_phosphatase: float
    urea: float
    cholesterol: float
    creatinine: float
    cystatin_c: float
    glycated_haemoglobin: float
    log_c_reactive_protein: float
    log_gamma_glutamyltransf: float
    red_blood_cell_erythrocyte_count: float
    mean_corpuscular_volume: float
    red_blood_cell_erythrocyte_distribution_width: float
    monocyte_count: float
    neutrophill_count: float
    lymphocyte_percentage: float
    mean_sphered_cell_volume: float
    log_alanine_aminotransfe: float
    log_shbg: float
    log_vitamin_d: float
    high_light_scatter_reticulocyte_percentage: float
    glucose: float
    platelet_distribution_width: float
    mean_corpuscular_haemoglobin: float
    platelet_crit: float
    apolipoprotein_a: float


class DNAmPhenoAgeLevine2018TestRequest(BloodTestBaseRequest):
    albumin: float
    creatinine: float
    glucose: float
    c_reactive_protein: float
    lymphocytes_percentage: float
    mean_corpuscular_volume: float
    red_blood_cell_distribution_width: float
    alkaline_phosphatase: float
    white_blood_cell_count: float
