from fastapi import APIRouter, Cookie, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.usuario import Usuario

router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db),
    session_token: str | None = Cookie(default=None),
):
    if session_token:
        try:
            get_current_user(db, session_token)
            return RedirectResponse("/dashboard", status_code=303)
        except Exception:
            pass
    return RedirectResponse("/login", status_code=303)


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/cadastro")
def cadastro_page(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro.html")


@router.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")
