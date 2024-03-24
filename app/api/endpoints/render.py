from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session


router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/test", response_class=HTMLResponse)
async def render_test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})


@router.get("/kit", response_class=HTMLResponse)
async def render_kit(request: Request):
    return templates.TemplateResponse("kit.html", {"request": request})
