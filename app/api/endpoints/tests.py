from fastapi import APIRouter, Depends
from app.logic.tests import calculate_dnam_pheno_age_levine_2018
from app.models.user import User
from app.models.biological_test import DNAmPhenoAgeLevine2018Test
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.requests import (
    DNAmPhenoAgeLevine2018TestRequest,
)
from app.schemas.responses import (
    DNAmPhenoAgeLevine2018TestResponse,
)
from app.schemas.data import tests
from app.api import deps
from datetime import datetime

router = APIRouter()


@router.get("/all")
async def get_tests():
    return tests


@router.post(
    "/dnam-pheno-age-levine-2018", response_model=DNAmPhenoAgeLevine2018TestResponse
)
async def create_dnam_pheno_age_levine_2018_test(
    test_data: DNAmPhenoAgeLevine2018TestRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user_cookies),
):
    result = calculate_dnam_pheno_age_levine_2018(test_data)["DNAmAge"]

    test_record = DNAmPhenoAgeLevine2018Test(
        name="DNAmPhenoAgeLevine2018",
        price=0.0,
        result=result,
        birthday=test_data.birthday,
        sex=test_data.sex,
        albumin=test_data.albumin,
        creatinine=test_data.creatinine,
        glucose=test_data.glucose,
        c_reactive_protein=test_data.c_reactive_protein,
        lymphocytes_percentage=test_data.lymphocytes_percentage,
        mean_corpuscular_volume=test_data.mean_corpuscular_volume,
        red_blood_cell_distribution_width=test_data.red_blood_cell_distribution_width,
        alkaline_phosphatase=test_data.alkaline_phosphatase,
        white_blood_cell_count=test_data.white_blood_cell_count,
    )
    session.add(test_record)
    await session.commit()
    await session.refresh(test_record)

    return DNAmPhenoAgeLevine2018TestResponse(
        user_id=current_user.id,
        result=test_record.result,
        created_at=test_record.created_at,
    )
