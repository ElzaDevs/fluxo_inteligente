from datetime import datetime, timezone

from fastapi import Cookie, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.models.sessao import Sessao
from app.models.usuario import Usuario
from app.security import hash_token


def get_current_user(
    db: Session,
    session_token: str | None,
) -> Usuario:
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária.",
        )

    sessao = db.query(Sessao).filter(
        Sessao.token_hash == hash_token(session_token),
        Sessao.revoked_at.is_(None),
    ).first()

    if not sessao or sessao.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão expirada ou inválida.",
        )

    if not sessao.usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo.",
        )

    return sessao.usuario


def require_user(
    db: Session,
    session_token: str | None,
) -> Usuario:
    return get_current_user(db, session_token)


def require_csrf(
    db: Session,
    session_token: str | None,
    csrf_token: str | None,
) -> Usuario:
    user = get_current_user(db, session_token)

    sessao = db.query(Sessao).filter(
        Sessao.token_hash == hash_token(session_token),
        Sessao.revoked_at.is_(None),
    ).first()

    if not sessao or not csrf_token or sessao.csrf_hash != hash_token(csrf_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token CSRF inválido.",
        )

    return user
