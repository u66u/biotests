import time
from collections.abc import AsyncGenerator
from typing import Optional
import jwt
import os
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config, security
from app.core.session import async_session
from app.models.user import User
from app.schemas.responses import AccessTokenResponse

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token,
            config.settings.SECRET_KEY,
            algorithms=[security.JWT_ALGORITHM],
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )
    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = security.JWTTokenPayload(**payload)

    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use refresh token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


async def get_current_user_cookies(
    request: Request, session: AsyncSession = Depends(get_session)
) -> User:
    """Reads auth token from cookies, throws an error if not found"""
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token"
        )

    try:
        payload = jwt.decode(
            token,
            config.settings.SECRET_KEY,
            algorithms=[security.JWT_ALGORITHM],
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )
    token_data = security.JWTTokenPayload(**payload)

    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use refresh token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


async def get_current_user_cookies_optional(
    request: Request, session: AsyncSession = Depends(get_session)
) -> Optional[User]:
    """Reads auth token from cookies, returns None if not found, doesn't throw an error"""
    token = request.cookies.get("access_token")

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            config.settings.SECRET_KEY,
            algorithms=[security.JWT_ALGORITHM],
        )
    except jwt.DecodeError:
        return None

    token_data = security.JWTTokenPayload(**payload)

    if token_data.refresh:
        return None

    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        return None

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user = result.scalars().first()

    return user


def set_token_cookies(response: Response, token: AccessTokenResponse):
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        max_age=token.expires_at - token.issued_at,
        expires=token.expires_at,
        secure=True
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        max_age=token.refresh_token_expires_at - token.refresh_token_issued_at,
        expires=token.refresh_token_expires_at,
        secure=True
    )
