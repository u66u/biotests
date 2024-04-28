import time

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import config, security
from app.models.user import User
from app.schemas.requests import RefreshTokenRequest, UserCreateRequest
from app.schemas.responses import AccessTokenResponse, UserResponse

router = APIRouter()


@router.post("/access-token", response_model=AccessTokenResponse)
async def login_access_token(
    response: Response,
    session: AsyncSession = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """OAuth2 compatible token, get an access token for future requests using username and password"""

    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password, please double-check your credentials or restore password.",
        )

    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password, please double-check your credentials or restore password.",
        )

    # generate access token and store it in cookies
    token = security.generate_access_token_response(str(user.id))
    deps.set_token_cookies(response, token)

    return token


@router.post("/signup", response_model=UserResponse)
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
        hashed_password=security.get_password_hash(new_user.password),
        name=new_user.name,
    )
    session.add(user)
    await session.commit()
    return user


@router.post("/login")
async def login_user(
    response: Response,
    session: AsyncSession = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Log in user in the /login template and redirect to their profile"""

    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password, please double-check your credentials or restore password.",
        )

    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password, please double-check your credentials or restore password.",
        )

    # generate access token and store it in cookies
    token = security.generate_access_token_response(str(user.id))
    deps.set_token_cookies(response, token)

    return "Login successful!"


@router.post("/refresh-token", response_model=AccessTokenResponse)
async def refresh_token(
    input: RefreshTokenRequest,
    response: Response,
    session: AsyncSession = Depends(deps.get_session),
):
    """OAuth2 compatible token, get an access token for future requests using refresh token"""
    try:
        payload = jwt.decode(
            input.refresh_token,
            config.settings.SECRET_KEY,
            algorithms=[security.JWT_ALGORITHM],
        )
    except (jwt.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, unknown error",
        )

    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = security.JWTTokenPayload(**payload)

    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use access token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    token = security.generate_access_token_response(str(user.id))
    deps.set_token_cookies(response, token)

    return token


@router.get("/check-token")
async def check_token(
    request: Request,
    response: Response,
):
    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            payload = jwt.decode(
                access_token,
                config.settings.SECRET_KEY,
                algorithms=[security.JWT_ALGORITHM],
            )
            token_data = security.JWTTokenPayload(**payload)
            expires_at = token_data.expires_at
            current_time = int(time.time())

            if current_time < expires_at - 300:  # 5 minutes
                return {"valid": True}
        except (jwt.DecodeError, ValidationError):
            pass

    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        try:
            payload = jwt.decode(
                refresh_token,
                config.settings.SECRET_KEY,
                algorithms=[security.JWT_ALGORITHM],
            )
            token_data = security.JWTTokenPayload(**payload)
            expires_at = token_data.expires_at
            current_time = int(time.time())

            if current_time < expires_at:
                # Refresh token is valid, generate new tokens
                token = security.generate_access_token_response(str(token_data.sub))
                deps.set_token_cookies(response, token)
                return {"valid": True, "refreshed": True}
        except (jwt.DecodeError, ValidationError):
            pass

    return {"valid": False}
