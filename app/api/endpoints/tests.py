from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.logic.tests import (
    calculate_blood_market_ba_estimation,
    calculate_dnam_pheno_age_levine_2018,
)
from app.models.biological_test import (
    BloodMarketBAEstimationTest,
    DNAmPhenoAgeLevine2018Test,
)
from app.models.user import User
from app.schemas.data import tests
from app.schemas.requests import (
    BloodMarketBAEstimationTestCreateRequest,
    DNAmPhenoAgeLevine2018TestRequest,
)
from app.schemas.responses import (
    BloodMarketBAEstimationTestResponse,
    DNAmPhenoAgeLevine2018TestResponse,
)

router = APIRouter()


@router.get("/all")
async def get_tests():
    return tests


@router.get("/my")
async def get_user_tests(
    current_user: User = Depends(deps.get_current_user_cookies),
):
    return current_user.tests


@router.post(
    "/dnam-pheno-age-levine-2018", response_model=DNAmPhenoAgeLevine2018TestResponse
)
async def create_dnam_pheno_age_levine_2018_test(
    test_data: DNAmPhenoAgeLevine2018TestRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: Optional[User] = Depends(deps.get_current_user_cookies_optional),
):
    result = calculate_dnam_pheno_age_levine_2018(test_data)["DNAmAge"]

    test_record = DNAmPhenoAgeLevine2018Test(
        name="DNAmPhenoAgeLevine2018",
        user_id=current_user.id if current_user else None,
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
        user_id=current_user.id if current_user else None,
        result=test_record.result,
        created_at=test_record.created_at,
    )


@router.post(
    "/blood-marker-ba-estimation", response_model=BloodMarketBAEstimationTestResponse
)
async def create_blood_market_ba_estimation_test(
    test_data: BloodMarketBAEstimationTestCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: Optional[User] = Depends(deps.get_current_user_cookies_optional),
):
    result = calculate_blood_market_ba_estimation(test_data)

    test_record = BloodMarketBAEstimationTest(
        name="BloodMarketBAEstimationTest",
        user_id=current_user.id if current_user else None,
        price=0.0,
        result=result,
        birthday=test_data.birthday,
        sex=test_data.sex,
        albumin=test_data.albumin,
        alkaline_phosphatase=test_data.alkaline_phosphatase,
        urea=test_data.urea,
        cholesterol=test_data.cholesterol,
        creatinine=test_data.creatinine,
        cystatin_c=test_data.cystatin_c,
        glycated_haemoglobin=test_data.glycated_haemoglobin,
        log_c_reactive_protein=test_data.log_c_reactive_protein,
        log_gamma_glutamyltransf=test_data.log_gamma_glutamyltransf,
        red_blood_cell_erythrocyte_count=test_data.red_blood_cell_erythrocyte_count,
        mean_corpuscular_volume=test_data.mean_corpuscular_volume,
        red_blood_cell_erythrocyte_distribution_width=test_data.red_blood_cell_erythrocyte_distribution_width,
        monocyte_count=test_data.monocyte_count,
        neutrophill_count=test_data.neutrophill_count,
        lymphocyte_percentage=test_data.lymphocyte_percentage,
        mean_sphered_cell_volume=test_data.mean_sphered_cell_volume,
        log_alanine_aminotransfe=test_data.log_alanine_aminotransfe,
        log_shbg=test_data.log_shbg,
        log_vitamin_d=test_data.log_vitamin_d,
        high_light_scatter_reticulocyte_percentage=test_data.high_light_scatter_reticulocyte_percentage,
        glucose=test_data.glucose,
        platelet_distribution_width=test_data.platelet_distribution_width,
        mean_corpuscular_haemoglobin=test_data.mean_corpuscular_haemoglobin,
        platelet_crit=test_data.platelet_crit,
        apolipoprotein_a=test_data.apolipoprotein_a,
    )
    session.add(test_record)
    await session.commit()
    await session.refresh(test_record)

    return BloodMarketBAEstimationTestResponse(
        user_id=current_user.id if current_user else None,
        result=test_record.result,
        created_at=test_record.created_at,
    )
