from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import EmailStr
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.requests import UserCreateRequest, UserUpdatePasswordRequest, UserDetailsUpdateRequest, UserEmailUpdateRequest
from app.schemas.responses import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(deps.get_current_user_cookies),
):
    """Get current user"""
    return current_user


@router.delete("/me", status_code=204)
async def delete_current_user(
    current_password: str,
    current_user: User = Depends(deps.get_current_user_cookies),
    session: AsyncSession = Depends(deps.get_session),
):
    """Delete current user, reading user details from cookies, requires entering current password"""
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(status_code=403, detail="Current password is incorrect.")
    try:
        await session.execute(delete(User).where(User.id == current_user.id))
        await session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-details", response_model=UserResponse)
async def update_user_name(
    update_data: UserDetailsUpdateRequest,
    current_user: User = Depends(deps.get_current_user_cookies),
    session: AsyncSession = Depends(deps.get_session),
):
    current_user.name = update_data.name
    try:
        session.add(current_user)
        await session.commit()
        return current_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Failed to update name")


@router.post("/update-email", response_model=UserResponse)
async def update_user_email(
    new_email: EmailStr = Form(...),
    current_user: User = Depends(deps.get_current_user_cookies),
    session: AsyncSession = Depends(deps.get_session),
):
    current_user.email = new_email
    try:
        session.add(current_user)
        await session.commit()
        return current_user
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="Failed to update email")


@router.post("/reset-password", response_model=UserResponse)
async def reset_current_user_password(
    user_update_password: UserUpdatePasswordRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user_cookies)
):
    """Update current user password after verifying the current password"""

    if not verify_password(user_update_password.current_password, current_user.hashed_password):
        raise HTTPException(status_code=403, detail="Current password is incorrect.")

    current_user.hashed_password = get_password_hash(user_update_password.new_password)
    session.add(current_user)
    try:
        await session.commit()
        return current_user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register", response_model=UserResponse)
async def register_new_user(
    new_user: UserCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Create new user"""
    result = await session.execute(select(User).where(User.email == new_user.email))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Cannot use this email address")
    user = User(
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
        name=new_user.name,
    )
    session.add(user)
    await session.commit()
    return user
