from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.schemas.data import tests
import app.api.deps as deps

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "tests": tests}
    )


@router.get("/tests", response_class=HTMLResponse)
async def render_test(request: Request):
    return templates.TemplateResponse(
        "tests.html",
        {"request": request, "tests": tests, "user": deps.get_current_user},
    )


@router.get("/about", response_class=HTMLResponse)
async def render_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def render_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/forgot-password", response_class=HTMLResponse)
async def render_forgot_password(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def render_logout(request: Request):
    return templates.TemplateResponse("logout.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse)
async def render_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})
