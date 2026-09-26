import os

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_csrf
from app.models.usuario import Usuario
from app.schemas.auth import (
    CsrfResponse,
    EmpresaCadastro,
    LoginRequest,
    MeResponse,
    EmpresaResponse,
    UsuarioResponse,
)
from app.security import generate_token, hash_token
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])

COOKIE_NAME = "session_token"
COOKIE_KWARGS = {
    "httponly": True,
    "samesite": "lax",
    "secure": os.getenv("ENVIRONMENT", "development").lower() == "production",
    "max_age": 8 * 60 * 60,
    "path": "/",
}


def _usuario_response(user: Usuario) -> UsuarioResponse:
    return UsuarioResponse(
        id=user.id,
        nome=user.nome,
        email=user.email,
        perfil=user.perfil,
        empresa_id=user.empresa_id,
    )


@router.post("/register", response_model=MeResponse, status_code=status.HTTP_201_CREATED)
def register(
    dados: EmpresaCadastro,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        empresa, usuario, token, csrf = AuthService(db).registrar_empresa(
            dados.empresa,
            dados.cnpj,
            dados.nome,
            str(dados.email),
            dados.senha,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    response.set_cookie(COOKIE_NAME, token, **COOKIE_KWARGS)
    response.headers["X-CSRF-Token"] = csrf

    return MeResponse(
        usuario=_usuario_response(usuario),
        empresa=EmpresaResponse(
            id=empresa.id,
            nome=empresa.nome,
            cnpj=empresa.cnpj,
        ),
    )


@router.post("/login", response_model=MeResponse)
def login(
    dados: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    resultado = AuthService(db).autenticar(str(dados.email), dados.senha)

    if not resultado:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos.",
        )

    usuario, token, csrf = resultado
    response.set_cookie(COOKIE_NAME, token, **COOKIE_KWARGS)
    response.headers["X-CSRF-Token"] = csrf

    return MeResponse(
        usuario=_usuario_response(usuario),
        empresa=EmpresaResponse(
            id=usuario.empresa.id,
            nome=usuario.empresa.nome,
            cnpj=usuario.empresa.cnpj,
        ),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    user: Usuario = Depends(require_csrf),
    db: Session = Depends(get_db),
    session_token: str | None = Cookie(default=None),
):
    if session_token:
        AuthService(db).encerrar_sessao(session_token)

    response.delete_cookie(COOKIE_NAME, path="/")


@router.get("/me", response_model=MeResponse)
def me(user: Usuario = Depends(get_current_user)):
    return MeResponse(
        usuario=_usuario_response(user),
        empresa=EmpresaResponse(
            id=user.empresa.id,
            nome=user.empresa.nome,
            cnpj=user.empresa.cnpj,
        ),
    )


@router.get("/csrf", response_model=CsrfResponse)
def csrf(
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
    session_token: str | None = Cookie(default=None),
):
    from app.models.sessao import Sessao
    sessao = db.query(Sessao).filter(
        Sessao.token_hash == hash_token(session_token),
        Sessao.revoked_at.is_(None),
    ).first()

    if not sessao:
        raise HTTPException(status_code=401, detail="Sessão inválida.")

    token = generate_token()
    sessao.csrf_hash = hash_token(token)
    db.commit()
    return CsrfResponse(csrf_token=token)
