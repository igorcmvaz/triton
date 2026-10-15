"""Edições do Triton: Brasil (BRL), Internacional (INT) e Portugal (PRT).

As três edições partem do mesmo código. A Brasil traz os dados brasileiros
auditados: base climática CLIMBra, tarifas de 652 municípios, energia da ANEEL,
custos em reais, fator de emissão da rede do MCTI e as certificações e incentivos
nacionais (Casa Azul, AQUA-HQE, IPTU Verde). A Internacional é o núcleo neutro:
abre em inglês, com moeda escolhida pelo usuário, tarifas, custos e fator de
emissão informados por ele, e só as certificações internacionais (LEED, EDGE).
`usa_dados_do_brasil` é a pergunta que cada tela faz antes de oferecer um dado
brasileiro.

A Portugal parte do núcleo neutro e fala português de Portugal, em euros; os dados
portugueses (precipitação E-OBS por concelho, tarifários das entidades gestoras) entram
por `usa_dados_de_portugal`, à medida que são coletados e conferidos.
"""

from __future__ import annotations

import os

EDITION_BRL = "BRL"
EDITION_INT = "INT"
EDITION_PRT = "PRT"
EDICOES = (EDITION_BRL, EDITION_INT, EDITION_PRT)

ENV_VAR_EDITION = "TRITON_EDITION"

#: «POR» foi o código da Edição Portugal antes de ela passar a PRT; projetos e scripts antigos ainda o usam.
_SINONIMOS = {"POR": EDITION_PRT}


def _normalizar(codigo) -> str:
    cod = str(codigo).strip().upper()
    return _SINONIMOS.get(cod, cod)


def get_current_edition() -> str:
    """Retorna o código da edição ativa ('BRL', 'INT' ou 'PRT'). Padrão: 'BRL'."""
    val = _normalizar(os.environ.get(ENV_VAR_EDITION, EDITION_BRL))
    if val in EDICOES:
        return val
    return EDITION_BRL


def set_current_edition(edition: str) -> None:
    """Define a edição ativa ('BRL', 'INT' ou 'PRT')."""
    ed = _normalizar(edition)
    if ed not in EDICOES:
        raise ValueError(f"Edição inválida: {edition}. Escolha 'BRL', 'INT' ou 'PRT' (aceita também 'POR', o código antigo).")
    os.environ[ENV_VAR_EDITION] = ed


def is_brl_edition() -> bool:
    """Verifica se a edição Brasil está ativa."""
    return get_current_edition() == EDITION_BRL


def is_int_edition() -> bool:
    """Verifica se a edição Internacional está ativa."""
    return get_current_edition() == EDITION_INT


def is_prt_edition() -> bool:
    """Verifica se a edição Portugal está ativa."""
    return get_current_edition() == EDITION_PRT


def usa_dados_do_brasil() -> bool:
    """Tarifas, custos, clima, fator de rede e certificações brasileiros aparecem só na BRL."""
    return is_brl_edition()


def usa_dados_de_portugal() -> bool:
    """Precipitação por concelho e tarifários portugueses aparecem só na PRT."""
    return is_prt_edition()


#: O manual completo em cada língua, relativo à raiz do programa.
MANUAL_PT = "manual/Manual-Triton.pdf"
MANUAL_EN = "manual/en/Triton-User-Manual.pdf"


def manual_do_usuario(idioma: str) -> str:
    """O manual completo que o programa abre: o inglês na Internacional ou fora do português.

    A Internacional abre em inglês e não traz dados brasileiros; o manual dela é o
    inglês, qualquer que seja a língua escolhida. Na Brasil, segue a língua da interface:
    espanhol e chinês não têm manual próprio, e o inglês lhes serve melhor que o português.
    Na Portugal, o português de Portugal lê o manual em português.
    """
    if is_int_edition() or idioma not in ("pt", "pt_pt"):
        return MANUAL_EN
    return MANUAL_PT


def rotulo_da_edicao(curto: bool = False) -> str:
    """«Edição Brasil (BRL)», «International Edition (INT)» ou «Edição Portugal (PRT)»."""
    if is_int_edition():
        return "INT" if curto else "International Edition (INT)"
    if is_prt_edition():
        return "PRT" if curto else "Edição Portugal (PRT)"
    return "BRL" if curto else "Edição Brasil (BRL)"


def neutralizar_para_a_internacional(config) -> None:
    """Projeto novo da Internacional: nenhum preço, tarifa ou incentivo brasileiro.

    Os padrões do TritonConfig são os de um projeto em Florianópolis (tarifa da
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
    # A ETAP continua dimensionada, mas os preços de catálogo dela são em reais.
    config.precos_de_catalogo = False
    config.op_costs = [(nome, meses, 0.0, 0.0) for nome, meses, *_ in (config.op_costs or [])]


def get_edition_title() -> str:
    """Título da janela principal: o título do programa e a edição ativa."""
    from triton import APP_TITLE

    return f"{APP_TITLE} — {rotulo_da_edicao()}"


def get_edition_default_language() -> str:
    """Retorna o idioma padrão da edição."""
    if is_int_edition():
        return "en_US"
    if is_prt_edition():
        return "pt_PT"
    return "pt_BR"


#: A International fala com a União Europeia: o euro é a sua moeda padrão (as demais
#: continuam à escolha na Etapa 4).
MOEDA_DA_INTERNACIONAL = "\u20ac"


def get_edition_currency_symbol() -> str:
    """Retorna o símbolo monetário padrão da edição: real na Brasil, euro na International e na Portugal."""
    if is_int_edition() or is_prt_edition():
        return MOEDA_DA_INTERNACIONAL
    return "R$"


#: Nome antigo de ``is_prt_edition``, mantido para quem ainda o chama.
is_por_edition = is_prt_edition
