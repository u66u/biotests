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


@router.get("/kit", response_class=HTMLResponse)
async def render_kit(request: Request):
    return templates.TemplateResponse("kit.html", {"request": request})
