from fastapi import APIRouter

from app.api.endpoints import auth, users, render, pay, order, bio

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(render.router, tags=["render"])
api_router.include_router(pay.router, prefix="/pay", tags=["pay"])
api_router.include_router(order.router, prefix="/order", tags=["order"])
api_router.include_router(bio.router, prefix="/bio", tags=["bio"])
