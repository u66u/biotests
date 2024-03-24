from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pypayment import YooMoneyPayment, YooMoneyPaymentType, ChargeCommission
from starlette.responses import RedirectResponse

from app.core import config


router = APIRouter()


@router.get("/kit")
async def buy_kit(request: Request):
    YooMoneyPayment.authorize(
        access_token=config.settings.YOOMONEY_ACCESS_TOKEN,
        payment_type=YooMoneyPaymentType.CARD,
        charge_commission=ChargeCommission.FROM_SELLER,
        success_url="127.0.0.1:8000/pay/success",
    )

    payment = YooMoneyPayment(
        amount=2,
        description="Venera BIO biological age test kit",
        payment_type=YooMoneyPaymentType.CARD,
        charge_commission=ChargeCommission.FROM_SELLER,
        success_url="127.0.0.1:8000/pay/success",
    )

    return RedirectResponse(payment.url)
