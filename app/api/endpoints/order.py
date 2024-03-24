from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.order import Order
from app.models.user import User
from app.schemas.requests import OrderCreateRequest
from app.schemas.responses import OrderResponse
from app.api import deps
from datetime import datetime

router = APIRouter()


@router.post("/new", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreateRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Create a new order for the current user"""
    order = Order(
        user_id=current_user.id,  # Assign user_id to the current user's ID
        test_id=order_data.test_id,
        comments=order_data.comments,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: str,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Delete an order if the current user owns it"""
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this order",
        )

    await session.delete(order)
    await session.commit()
