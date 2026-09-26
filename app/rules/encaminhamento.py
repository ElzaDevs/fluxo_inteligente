import unicodedata


SETOR_FINANCEIRO = "Setor Financeiro"
SETOR_TI = "Tecnologia da Informação"
SETOR_SUPORTE = "Analistas de Suporte"
SETOR_ECONOMIA = "Gestão da Economia"


def _normalizar(valor: str) -> str:
    valor = unicodedata.normalize("NFKD", valor.lower())
    return "".join(c for c in valor if not unicodedata.combining(c)).strip()


def determinar_setor(categoria: str) -> str | None:
    categoria_normalizada = _normalizar(categoria)

    if any(
        termo in categoria_normalizada
        for termo in ("financeiro", "financas", "pagamento", "faturamento")
    ):
        return SETOR_FINANCEIRO

    if any(
        termo in categoria_normalizada
        for termo in ("ti", "tecnologia", "sistema", "software", "infra")
    ):
        return SETOR_TI

    if any(termo in categoria_normalizada for termo in ("suporte", "atendimento")):
        return SETOR_SUPORTE

    if any(
        termo in categoria_normalizada
        for termo in ("economia", "gestao economica", "gestao da economia")
    ):
        return SETOR_ECONOMIA

    return None
