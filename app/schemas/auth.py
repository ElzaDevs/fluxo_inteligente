from pydantic import BaseModel, EmailStr, Field


class EmpresaCadastro(BaseModel):
    empresa: str = Field(min_length=2, max_length=160)
    cnpj: str | None = Field(default=None, min_length=11, max_length=18)
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1, max_length=128)


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str
    empresa_id: int


class EmpresaResponse(BaseModel):
    id: int
    nome: str
    cnpj: str | None


class MeResponse(BaseModel):
    usuario: UsuarioResponse
    empresa: EmpresaResponse


class CsrfResponse(BaseModel):
    csrf_token: str
