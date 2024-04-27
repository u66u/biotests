from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import FastAPI, Request, Depends, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.schemas.data import (
    tests,
    ba_estimation_test_fields,
    dnam_pheno_age_levine2018_test_fields,
)
from app.api import deps


router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "tests": tests}
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


@router.get("/profile", response_class=HTMLResponse)
async def render_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@router.get("/tests", response_class=HTMLResponse)
async def render_tests(request: Request):
    return templates.TemplateResponse(
        "tests/index.html", {"request": request, "tests": tests}
    )


@router.get("/tests/phenoage-2018", response_class=HTMLResponse)
async def render_test_phenoage2018(request: Request):
    return templates.TemplateResponse(
        "tests/phenoage-2018.html",
        {"request": request, "model_fields": dnam_pheno_age_levine2018_test_fields},
    )


@router.get("/tests/ba-estimation", response_class=HTMLResponse)
async def render_test_ba_estimation(request: Request):
    return templates.TemplateResponse(
        "tests/ba_estimation.html",
        {
            "request": request,
            "model_fields": ba_estimation_test_fields,
        },
    )


@router.get("/logout", response_class=HTMLResponse)
def logout(request: Request, response: Response):
    """Logs out a user by setting their access_token and refresh_token to expire immediately. Warning: this is not secure on its own, we also need to invalidate the tokens server-side, e.g. delete them from valid tokens from database, or add to list of blacklisted tokens"""
    
    response = templates.TemplateResponse("login.html", {"request": request})
    response.set_cookie(key="access_token", value="", expires=0)
    response.set_cookie(key="refresh_token", value="", expires=0)
    return response