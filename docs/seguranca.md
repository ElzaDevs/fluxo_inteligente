# Segurança e autenticação

## Fluxo

```text
Cadastro da empresa
      ↓
Usuário administrador
      ↓
Senha → hash Argon2
      ↓
Sessão aleatória armazenada como hash
      ↓
Cookie HttpOnly
      ↓
X-CSRF-Token nas operações de escrita
```

Senhas não são armazenadas em texto puro.

As sessões possuem expiração de 8 horas e podem ser revogadas no logout.

O cookie utiliza `SameSite=Lax` e, em ambiente de produção, pode ser marcado como `Secure` através da variável `ENVIRONMENT=production`.

## Limites do projeto

Para produção real ainda devem ser adicionados, conforme contexto:

- rate limiting no login;
- MFA;
- gerenciamento de recuperação de senha;
- política de retenção de sessões;
- gestão granular de permissões;
- auditoria de segurança;
- HTTPS terminando no ambiente de deploy;
- gestão de segredos por secret manager.

A implementação atual é apropriada para demonstração e evolução de um produto, não como sistema financeiro corporativo pronto para dados reais sem essas camadas adicionais.
