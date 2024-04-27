from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import FastAPI, Request, Depends, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy.orm import joinedload, with_polymorphic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.data import (
    tests,
    ba_estimation_test_fields,
    dnam_pheno_age_levine2018_test_fields,
)
from app.models.user import User
from app.models.biological_test import TestType, DNAmPhenoAgeLevine2018Test, BiologicalTest, BloodMarketBAEstimationTest 
from app.api import deps
from app.api.endpoints.auth import check_token 


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
async def profile(request: Request, current_user: User = Depends(deps.get_current_user_cookies_optional), session: AsyncSession = Depends(deps.get_session)):
    if current_user:
        polymorphic_query = with_polymorphic(BiologicalTest, [DNAmPhenoAgeLevine2018Test, BloodMarketBAEstimationTest]) # add more types of tests when necessary

        q = await session.execute(select(polymorphic_query).where(BiologicalTest.user_id == current_user.id))

        tests = (i[0] for i in q) # q.all() ?

        template_name = "profile.html"
    else:
        template_name = "auth_error.html"
        tests = None
    return templates.TemplateResponse(template_name, {"request": request, "tests": tests})


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