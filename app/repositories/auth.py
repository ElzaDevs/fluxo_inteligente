from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.models.sessao import Sessao
from app.models.usuario import Usuario
from app.security import generate_token, hash_password, hash_token, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def criar_empresa_com_admin(
        self,
        empresa_nome: str,
        cnpj: str | None,
        nome_usuario: str,
        email: str,
        senha: str,
    ) -> tuple[Empresa, Usuario, str, str]:
        if self.db.query(Usuario).filter(Usuario.email == email).first():
            raise ValueError("E-mail já cadastrado.")

        if cnpj and self.db.query(Empresa).filter(Empresa.cnpj == cnpj).first():
            raise ValueError("CNPJ já cadastrado.")

        agora = datetime.now(timezone.utc)
        empresa = Empresa(nome=empresa_nome, cnpj=cnpj, created_at=agora)
        usuario = Usuario(
            nome=nome_usuario,
            email=email,
            senha_hash=hash_password(senha),
            perfil="ADMIN",
            ativo=True,
            created_at=agora,
        )
        empresa.usuarios.append(usuario)
        self.db.add(empresa)
        self.db.flush()

        return (*self._criar_sessao(usuario, agora),)[0:4]

    def autenticar(self, email: str, senha: str) -> tuple[Usuario, str, str] | None:
        usuario = self.db.query(Usuario).filter(Usuario.email == email).first()
        if not usuario or not usuario.ativo:
            return None
        if not verify_password(senha, usuario.senha_hash):
            return None

        agora = datetime.now(timezone.utc)
        token, csrf = self._criar_sessao(usuario, agora)
        self.db.commit()
        return usuario, token, csrf

    def _criar_sessao(self, usuario: Usuario, agora: datetime) -> tuple[Empresa, Usuario, str, str]:
        token = generate_token()
        csrf = generate_token()
        sessao = Sessao(
            usuario=usuario,
            token_hash=hash_token(token),
            csrf_hash=hash_token(csrf),
            expires_at=agora.replace(microsecond=0) + __import__("datetime").timedelta(hours=8),
            created_at=agora,
        )
        self.db.add(sessao)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario.empresa, usuario, token, csrf

    def encerrar_sessao(self, token: str) -> None:
        sessao = self.db.query(Sessao).filter(
            Sessao.token_hash == hash_token(token),
            Sessao.revoked_at.is_(None),
        ).first()
        if sessao:
            sessao.revoked_at = datetime.now(timezone.utc)
            self.db.commit()
