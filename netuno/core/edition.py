"""Edições do Netuno 5: Brasil (BRL) e Internacional (INT).

As duas edições partem do mesmo código. A Brasil traz os dados brasileiros
auditados: base climática CLIMBra, tarifas de 652 municípios, energia da ANEEL,
custos em reais, fator de emissão da rede do MCTI e as certificações e incentivos
nacionais (Casa Azul, AQUA-HQE, IPTU Verde). A Internacional é o núcleo neutro:
abre em inglês, com moeda escolhida pelo usuário, tarifas, custos e fator de
emissão informados por ele, e só as certificações internacionais (LEED, EDGE).
`usa_dados_do_brasil` é a pergunta que cada tela faz antes de oferecer um dado
brasileiro.
"""

from __future__ import annotations

import os

EDITION_BRL = "BRL"
EDITION_INT = "INT"

ENV_VAR_EDITION = "NETUNO_EDITION"


def get_current_edition() -> str:
    """Retorna o código da edição ativa ('BRL' ou 'INT'). Padrão: 'BRL'."""
    val = os.environ.get(ENV_VAR_EDITION, EDITION_BRL).strip().upper()
    if val in (EDITION_BRL, EDITION_INT):
        return val
    return EDITION_BRL


def set_current_edition(edition: str) -> None:
    """Define a edição ativa ('BRL' ou 'INT')."""
    ed = str(edition).strip().upper()
    if ed not in (EDITION_BRL, EDITION_INT):
        raise ValueError(f"Edição inválida: {edition}. Escolha 'BRL' ou 'INT'.")
    os.environ[ENV_VAR_EDITION] = ed


def is_brl_edition() -> bool:
    """Verifica se a edição Brasil está ativa."""
    return get_current_edition() == EDITION_BRL


def is_int_edition() -> bool:
    """Verifica se a edição Internacional está ativa."""
    return get_current_edition() == EDITION_INT


def usa_dados_do_brasil() -> bool:
    """Tarifas, custos, clima, fator de rede e certificações brasileiros aparecem só na BRL."""
    return is_brl_edition()


def rotulo_da_edicao(curto: bool = False) -> str:
    """«Edição Brasil (BRL)» ou «International Edition (INT)», para selo, relatórios e exportações."""
    if is_int_edition():
        return "INT" if curto else "International Edition (INT)"
    return "BRL" if curto else "Edição Brasil (BRL)"


def neutralizar_para_a_internacional(config) -> None:
    """Projeto novo da Internacional: nenhum preço, tarifa ou incentivo brasileiro.

    Os padrões do NetunoConfig são os de um projeto em Florianópolis (tarifa da
    CASAN, energia da CELESC, motobomba, cloro e manutenções em reais). Na
    Internacional, ficam zerados para o usuário informar os da sua obra, na moeda
    escolhida; os nomes das manutenções continuam, como roteiro.
    """
    config.water_tariffs = []
    config.tariff_city_uf = config.tariff_city_name = "CUSTOM"
    config.elec_city_uf = config.elec_city_name = "CUSTOM"
    config.elec_tariff = 0.0
    config.pump_unit_cost = 0.0
    config.chlorine_cost_per_kg = 0.0
    config.iptu_green_enabled = False
    config.capex_do_arranjo = False
    config.mao_de_obra_automatica = False
    config.op_costs = [(nome, meses, 0.0, 0.0) for nome, meses, *_ in (config.op_costs or [])]


def get_edition_title() -> str:
    """Título da janela principal: o título do programa e a edição ativa."""
    from netuno import APP_TITLE

    return f"{APP_TITLE} — {rotulo_da_edicao()}"


def get_edition_default_language() -> str:
    """Retorna o idioma padrão da edição."""
    if is_int_edition():
        return "en_US"
    return "pt_BR"


def get_edition_currency_symbol() -> str:
    """Retorna o símbolo monetário padrão da edição."""
    if is_int_edition():
        return "$"
    return "R$"
