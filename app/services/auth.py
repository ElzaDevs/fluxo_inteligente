from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.models.sessao import Sessao
from app.models.usuario import Usuario
from app.security import generate_token, hash_password, hash_token, verify_password


class AuthService:
    SESSION_HOURS = 8

    def __init__(self, db: Session):
        self.db = db

    def registrar_empresa(
        self,
        empresa_nome: str,
        cnpj: str | None,
        nome_usuario: str,
        email: str,
        senha: str,
    ) -> tuple[Empresa, Usuario, str, str]:
        if self.db.query(Usuario).filter(Usuario.email == email.lower()).first():
            raise ValueError("E-mail já cadastrado.")

        if cnpj and self.db.query(Empresa).filter(Empresa.cnpj == cnpj).first():
            raise ValueError("CNPJ já cadastrado.")

        agora = datetime.now(timezone.utc)
        empresa = Empresa(nome=empresa_nome, cnpj=cnpj, created_at=agora)
        usuario = Usuario(
            nome=nome_usuario,
            email=email.lower(),
            senha_hash=hash_password(senha),
            perfil="ADMIN",
            ativo=True,
            created_at=agora,
        )
        empresa.usuarios.append(usuario)
        self.db.add(empresa)
        self.db.flush()

        token, csrf = self._criar_sessao(usuario, agora)
        self.db.commit()
        self.db.refresh(empresa)
        self.db.refresh(usuario)
        return empresa, usuario, token, csrf

    def autenticar(self, email: str, senha: str) -> tuple[Usuario, str, str] | None:
        usuario = self.db.query(Usuario).filter(
            Usuario.email == email.lower()
        ).first()

        if not usuario or not usuario.ativo:
            return None

        if not verify_password(senha, usuario.senha_hash):
            return None

        agora = datetime.now(timezone.utc)
        token, csrf = self._criar_sessao(usuario, agora)
        self.db.commit()
        return usuario, token, csrf

    def encerrar_sessao(self, token: str) -> None:
        sessao = self.db.query(Sessao).filter(
            Sessao.token_hash == hash_token(token),
            Sessao.revoked_at.is_(None),
        ).first()

        if sessao:
            sessao.revoked_at = datetime.now(timezone.utc)
            self.db.commit()

    def _criar_sessao(
        self,
        usuario: Usuario,
        agora: datetime,
    ) -> tuple[str, str]:
        token = generate_token()
        csrf = generate_token()

        sessao = Sessao(
            usuario=usuario,
            token_hash=hash_token(token),
            csrf_hash=hash_token(csrf),
            expires_at=agora + timedelta(hours=self.SESSION_HOURS),
            created_at=agora,
        )
        self.db.add(sessao)
        self.db.flush()
        return token, csrf
