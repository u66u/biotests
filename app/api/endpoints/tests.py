from fastapi import APIRouter, Depends
from app.logic.tests import calculate_dnam_pheno_age_levine_2018
from app.models.user import User
from app.models.biological_test import DNAmPhenoAgeLevine2018Test
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.requests import (
    BloodTestCreateRequest,
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
    current_user: User = Depends(deps.get_current_user),
):
    result = calculate_dnam_pheno_age_levine_2018(test_data)

    test_record = DNAmPhenoAgeLevine2018Test(
        name="DNAmPhenoAgeLevine2018",
        description="One of the first bioloigcal age tests, used the NHANES III as training data, in which we employed a proportional hazard penalized regression model to narrow 42 biomarkers to 9 biomarkers and chronological age. This measure was then validated in NHANES IV and shown to be a strong predictor of both morbidity and mortality risk",
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


# @router.post("/new-blood-test", response_model=BloodTestResponse)
# async def create_blood_test(
#     test_data: BloodTestCreateRequest,
#     session: AsyncSession = Depends(deps.get_session),
# ):
#     blood_test = BloodTest(
#         name=test_data.name,
#         description=test_data.description,
#         price=test_data.price,
#         glucose=test_data.glucose,
#         cholesterol=test_data.cholesterol,
#         created_at=datetime.now(),
#         updated_at=datetime.now(),
#     )
#     session.add(blood_test)
#     await session.commit()
#     await session.refresh(blood_test)
#     return blood_test
#
#
# @router.post("/dna-tests", response_model=DNATestResponse)
# async def create_dna_test(
#     test_data: DNATestCreateRequest,
#     session: AsyncSession = Depends(deps.get_session),
# ):
#     dna_test = DNATest(**test_data.dict())
#     session.add(dna_test)
#     await session.commit()
#     await session.refresh(dna_test)
#     return dna_test
