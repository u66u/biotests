from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime

from app.models.order import Order
from app.models.user import User
from app.schemas.requests import OrderCreateRequest
from app.schemas.responses import OrderResponse
from app.api import deps

router = APIRouter()


@router.get("/my", response_model=Optional[List[OrderResponse]])
async def get_user_orders(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Get all orders for the current user"""
    stmt = select(Order).where(Order.user_id == current_user.id)
    orders = await session.execute(stmt)
    return orders.scalars().all()


@router.get("/{order_id}", response_model=Optional[OrderResponse])
async def get_order_by_id(
    order_id: str,
    session: AsyncSession = Depends(deps.get_session),
):
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/new", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreateRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Create a new order for the current user"""
    order = Order(
        user_id=current_user.id,
        test_id=order_data.test_id,
        comments=order_data.comments,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    session.add(order)
    await session.commit()
    await session.refresh(order)
    await session.refresh(current_user)
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


# Maybe faster but don't know how to make it work
# @router.get("/my", response_model=Optional[List[OrderResponse]])
# async def get_user_orders(
#     current_user: User = Depends(deps.get_current_user),
#     session: AsyncSession = Depends(deps.get_session),
# ):
#     """Get all orders for the current user, along with polymorphic test data"""
#     biological_test_polymorphic = with_polymorphic(
#         BiologicalTest, [BloodTest, DNATest], aliased=True
#     )
#
#     stmt = (
#         select(Order)
#         .options(joinedload(Order.test.of_type(biological_test_polymorphic)))
#         .where(Order.user_id == current_user.id)
#     )
#
#     result = await session.execute(stmt)
#     orders = result.scalars().all()
#
#     if not orders:
#         raise HTTPException(status_code=404, detail="No orders found for the user.")
#
#     order_responses = [OrderResponse.model_validate(order) for order in orders]
#     return order_responses
