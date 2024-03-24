from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.models.user import User
from app.models.order import Order
from app.models.biological_test import BloodTest, DNATest
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.requests import BloodTestCreateRequest, DNATestCreateRequest
from app.schemas.responses import BloodTestResponse, DNATestResponse, OrderResponse
from app.api import deps
from datetime import datetime

router = APIRouter()


@router.post("/new-blood-test", response_model=BloodTestResponse)
async def create_blood_test(
    test_data: BloodTestCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    blood_test = BloodTest(
        name=test_data.name,
        description=test_data.description,
        price=test_data.price,
        glucose=test_data.glucose,
        cholesterol=test_data.cholesterol,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(blood_test)
    await session.commit()
    await session.refresh(blood_test)
    return blood_test


@router.post("/dna-tests", response_model=DNATestResponse)
async def create_dna_test(
    test_data: DNATestCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    dna_test = DNATest(**test_data.dict())
    session.add(dna_test)
    await session.commit()
    await session.refresh(dna_test)
    return dna_test
