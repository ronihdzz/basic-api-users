# src/api/endpoints.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from settings import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "PROJECT_NAME": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "author": settings.AUTHOR,
        "profile_image_url": settings.PROFILE_IMAGE_URL
    })

@router.get("/healthcheck")
async def healthcheck():
    return {"status": "OK"}
