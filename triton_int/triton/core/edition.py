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
import re

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
    """Projeto novo fora da Brasil: nenhum preço, tarifa ou incentivo brasileiro.

    Os padrões do TritonConfig são os de um projeto em Florianópolis (tarifa da
    CASAN, energia da CELESC, motobomba, cloro e manutenções em reais). Fora da Brasil,
    ficam zerados para o usuário informar os da sua obra, na moeda escolhida; os nomes
    das manutenções continuam, como roteiro. A localidade climática também sai de
    Florianópolis: na Internacional fica vazia (o usuário carrega a série do seu local) e na
    Portugal parte do concelho padrão da base E-OBS.

    Faz a mesma coisa nas duas edições; é chamada por ``configuracao_da_edicao`` e
    ``projeto_novo_da_edicao``, que são o caminho recomendado. O nome é antigo.
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
    if is_prt_edition():
        from triton.core import base_climatica_portugal as _pt
        config.climate_source_mode = "national_db"
        config.climate_city_uf = _pt.DISTRITO_PADRAO
        config.climate_city_name = _pt.CONCELHO_PADRAO
        config.climate_model = _pt.MODELO_EOBS
        config.climate_scenario = _pt.CENARIO_EOBS
        config.climate_start_date = _pt.INICIO_PADRAO
        config.climate_end_date = _pt.FIM_PADRAO
    else:
        config.climate_source_mode = "custom_file"
        config.climate_city_uf = ""
        config.climate_city_name = ""
        config.climate_model = ""
        config.climate_scenario = ""


#: CASAN residencial (Florianópolis), vigente a partir de 01/04/2026: a tarifa de reserva da Brasil.
#: (início m³, fim m³, tarifa, tipo): tipo -1 é a tarifa fixa mensal; 1, a faixa de consumo.
_TARIFA_DE_RESERVA_BRL = (
    (0.0, 0.0, 46.34, -1),
    (0.0, 10.0, 3.08, 1),
    (10.0, 25.0, 14.31, 1),
    (25.0, 50.0, 19.14, 1),
    (50.0, 999999.0, 24.08, 1),
)


def valor_de_partida_da_edicao(historico: float) -> float:
    """Valor inicial de um parâmetro que é dado do Brasil: o histórico na BRL, zero nas demais.

    Serve onde o motor precisa de um número de partida (por exemplo, a emissão da água potável da
    rede, que é a de uma rota do Brasil) e o usuário de outra edição deve informar o dele.
    """
    return float(historico) if usa_dados_do_brasil() else 0.0


def tarifa_de_agua_de_reserva():
    """Faixas de água que o motor usa quando o projeto chega sem tarifa nenhuma.

    Na Brasil, a CASAN residencial (o comportamento histórico, que não muda). Nas outras
    edições, nenhuma: a conta de água sai zero até o usuário informar a tarifa da sua obra, em
    vez de cobrar, calado, a tarifa de uma concessionária brasileira.
    """
    return [tuple(f) for f in _TARIFA_DE_RESERVA_BRL] if usa_dados_do_brasil() else []


def configuracao_da_edicao():
    """``TritonConfig`` com os padrões da edição ativa.

    É a fábrica que a interface, a linha de comando e os leitores de projeto usam. Na Brasil
    devolve o ``TritonConfig()`` histórico, sem nenhuma diferença; na Internacional e na
    Portugal, o mesmo objeto sem os preços, tarifas e localidade de Florianópolis
    (``neutralizar_para_a_internacional``). O ``TritonConfig()`` cru continua devolvendo os
    padrões históricos em qualquer edição, e é o que os testes do motor usam: o motor não
    conhece edição.
    """
    from triton.core.parser import TritonConfig
    config = TritonConfig()
    if not usa_dados_do_brasil():
        neutralizar_para_a_internacional(config)
    return config


def projeto_novo_da_edicao():
    """O projeto novo da edição: ``configuracao_da_edicao`` mais o que o projeto novo liga.

    CAPEX e mão de obra do arranjo só na Brasil (catálogos em reais). Na Portugal, o
    tarifário de Lisboa (EPAL e Câmara Municipal), se estiver transcrito nesta instalação.
    """
    config = configuracao_da_edicao()
    config.capex_do_arranjo = usa_dados_do_brasil()
    config.mao_de_obra_automatica = usa_dados_do_brasil()
    if usa_dados_de_portugal():
        from triton.core import tarifarios_portugal as _tp
        _tp.aplicar("Lisboa", config)
    return config


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


#: Na Edição Portugal a moeda oficial é o euro; na Internacional não há moeda predefinida (decisão U-21).
MOEDA_DE_PORTUGAL = "\u20ac"
MOEDA_DA_INTERNACIONAL = ""


def get_edition_currency_symbol() -> str:
    """Retorna o símbolo monetário padrão da edição: real na Brasil, euro na Portugal e neutro na International (U-21)."""
    if is_prt_edition():
        return MOEDA_DE_PORTUGAL
    if is_int_edition():
        return MOEDA_DA_INTERNACIONAL
    return "R$"


#: Nome antigo de ``is_prt_edition``, mantido para quem ainda o chama.
is_por_edition = is_prt_edition


def serie_de_exemplo_da_edicao() -> str:
    """Nome do arquivo CSV de precipitação de exemplo para a edição ativa."""
    if is_prt_edition():
        return "Funchal.csv"
    if is_int_edition():
        return "NewYork.csv"
    return "Florianopolis1.csv"


def cenarios_de_exemplo_da_edicao() -> list:
    """Linhas do modelo de planilha de cenários (``excel_scenarios.generate_sample_scenario_excel``).

    Cada edição cita só séries de chuva que ela distribui em ``data/rainfall``. Chaves: as
    colunas da planilha, sem o que é igual em todas (descarte, escoamento e reservatórios).
    """
    if is_int_edition():
        return [
            {"nome": "Residence New York, 3 residents", "serie": "NewYork.csv", "area": 100, "moradores": 3, "demanda": 100, "percentual": 40},
            {"nome": "Residence London, 4 residents", "serie": "London.csv", "area": 150, "moradores": 4, "demanda": 120, "percentual": 50},
            {"nome": "School Cape Town", "serie": "CapeTown.csv", "area": 300, "moradores": 10, "demanda": 50, "percentual": 30},
        ]
    if is_prt_edition():
        return [
            {"nome": "Moradia no Funchal, 3 residentes", "serie": "Funchal.csv", "area": 100, "moradores": 3, "demanda": 100, "percentual": 40},
        ]
    return [
        {"nome": "Residência Florianópolis 3 hab", "serie": "Florianopolis1.csv", "area": 100, "moradores": 3, "demanda": 100, "percentual": 40},
        {"nome": "Residência São Paulo 4 hab", "serie": "SaoPaulo1.csv", "area": 150, "moradores": 4, "demanda": 120, "percentual": 50},
        {"nome": "Escola Brasília", "serie": "Brasilia1.csv", "area": 300, "moradores": 10, "demanda": 50, "percentual": 30},
    ]


def cidade_de_exemplo_da_edicao() -> str:
    """Nome legível da localidade da série de exemplo."""
    if is_prt_edition():
        return "Funchal, Portugal"
    if is_int_edition():
        return "New York, USA"
    return "Florianópolis, Brasil"


# ── Neutralidade de textos e marcas da Edição Brasil ─────────────────────────────

_NORMA_NBR = re.compile(
    r"(?:ABNT\s+)?NBR\s*\d{3,5}(?::\d{4})?(?:\s*(?:/|e|and|y)\s*(?:ABNT\s+)?NBR\s*\d{3,5}(?::\d{4})?)*",
    re.IGNORECASE)
_NORMA_DE_REFERENCIA = {
    "pt": "norma de referência", "en": "the reference standard",
    "es": "la norma de referencia", "zh": "参考标准",
}


_NORMA_LINHA = re.compile(
    r"^Normas? de refer[eê]ncia:\s*(?:ABNT\s+)?NBR.*$",
    re.IGNORECASE | re.MULTILINE)
_NORMA_PARENS = re.compile(
    r"\s*\((?:conforme\s+)?(?:ABNT\s+)?NBR[^\)]*\)",
    re.IGNORECASE)


def sem_norma_do_brasil(texto: str, idioma: str | None = None) -> str:
    """Troca «ABNT NBR n» por «norma de referência» em textos do núcleo."""
    if not texto or usa_dados_do_brasil() or not isinstance(texto, str):
        return texto
    lingua = idioma or ("en" if is_int_edition() else "pt")
    if _NORMA_LINHA.match(texto):
        return "Reference standard: local project standard" if lingua == "en" else "Norma de referência: a do local do projeto"
    texto = _NORMA_PARENS.sub("", texto)
    ref = _NORMA_DE_REFERENCIA.get(lingua, _NORMA_DE_REFERENCIA["pt"])
    texto = _NORMA_NBR.sub(ref, texto)
    return re.sub(r"\bABNT\b\s*", "", texto).rstrip()


_MARCAS_DO_BRASIL = (
    ("Ressalva de escopo: a resina consumida no Brasil tem matriz eletrica e cadeia de materia-prima diferentes das norte-americanas.",
     "Ressalva de escopo: a resina consumida no local do projeto pode ter matriz eletrica e cadeia de materia-prima diferentes das norte-americanas."),
    ("O SIDAC, inventário brasileiro da construção, publica para concreto dosado em central cerca de",
     "Inventários públicos da construção publicam, para concreto dosado em central, cerca de"),
    ("SIDAC (Sistema de Informação do Desempenho Ambiental da Construção): concreto dosado em central, 310 a 480 kg CO2/m³ entre 20 e 40 MPa",
     "Inventário público da construção: concreto dosado em central, 310 a 480 kg CO2/m³ entre 20 e 40 MPa (valor de triagem; prefira o inventário do seu país)"),
    ("Faixa do SIDAC por resistência", "Faixa do inventário por resistência"),
    ("a 40 MPa o SIDAC chega a", "a 40 MPa o inventário chega a"),
    ("no catálogo técnico da Fortlev (reservatórios conforme ABNT NBR 13210):", "no catálogo técnico de um fabricante de reservatórios em PRFV:"),
    ("massa por capacidade do catálogo Fortlev;", "massa por capacidade do catálogo de um fabricante;"),
    ("Catálogo técnico Fortlev, «Caixa d'água em fibra de vidro», peso da caixa vazia por capacidade",
     "Catálogo técnico de fabricante, caixa em fibra de vidro, peso da caixa vazia por capacidade"),
    ("Massa linear: Amanco Wavin FTC000021 (out/2025) ou geometria das ABNT NBR 5648 e 5688.",
     "Massa linear: ficha técnica de fabricante (2025) ou geometria normalizada do tubo."),
    ("Amanco Wavin FTC000021 (out/2025), tubo soldável", "Ficha técnica de fabricante (2025), tubo soldável"),
    ("ABNT NBR 5688:2018 Tab. 1, série reforçada:", "Geometria normalizada do tubo, série reforçada:"),
    ("(catálogo geral 60 Hz da Dancor, séries CAM W-4C e CAM W-10, motor monofásico de 2 polos)",
     "(catálogo geral 60 Hz de fabricante de motobombas, motor monofásico de 2 polos)"),
    ("(catálogo geral 60 Hz da Dancor, séries CAM W-4C e CAM W-10)", "(catálogo geral 60 Hz de fabricante de motobombas)"),
    ("Massa de catálogo Dancor (60 Hz)", "Massa de catálogo de fabricante (60 Hz)"),
    ("e não uma centrífuga brasileira", "e não uma centrífuga convencional"),
    ("ABNT NBR 15527:2019, item 4.6.5: cloro residual livre de 0,5 a 2,0 mg/L", "Faixa usual de cloro residual livre de 0,5 a 2,0 mg/L"),
    ("ABNT NBR 15527:2019 (Descarte inicial) / Inventário de Polímeros & Inox", "Descarte inicial / Inventário de Polímeros & Inox"),
    ("Fator de rede editável; usar a série MCTI/SIRENE do período do estudo", "Fator de rede editável; usar o fator do local e do período do estudo"),
    ("Fator de água potável editável; substituir pelo inventário da concessionária", "Fator de água potável editável; substituir pelo inventário da entidade que abastece o local"),
    ("Prefira o inventário da concessionária, quando existir", "Prefira o inventário da entidade que abastece o local, quando existir"),
    ("da concessionária", "da entidade que abastece o local"),
    ("matriz regional da concessionária", "matriz regional do local"),
)


def sem_marcas_do_brasil(texto: str, idioma: str | None = None) -> str:
    """O texto de ACV sem fabricantes, normas e inventários do Brasil (só fora da Edição Brasil)."""
    if not texto or usa_dados_do_brasil() or not isinstance(texto, str):
        return texto
    for fonte, alvo in _MARCAS_DO_BRASIL:
        if fonte in texto:
            texto = texto.replace(fonte, alvo)
    return sem_norma_do_brasil(texto, idioma or "pt")


TERMOS_DO_BRASIL = (
    r"Florian[oó]polis", r"Bras[ií]lia", r"Manaus", r"S[aã]o Paulo", r"Santa Catarina",
    r"R\$", r"\bBRL\b", r"\breais\b", r"\breal brasileiro",
    r"\bCASAN\b", r"\bCELESC\b", r"\bSABESP\b", r"\bCOPASA\b", r"\bCORSAN\b", r"\bSANEPAR\b",
    r"\bANEEL\b", r"bandeira tarif", r"tariff flag",
    r"\bCLIMBra\b", r"\bCMIP6\b", r"\bINMET\b", r"\bIBGE\b", r"\bMCTI\b", r"\bSIRENE\b",
    r"\bSINAPI\b", r"\bSNIS\b", r"\bSIDAC\b", r"\bABNT\b", r"\bNBR\b", r"\bCREA\b",
    r"\bIPTU\b", r"\bSelic\b", r"\bIPCA\b", r"\bINPC\b", r"\bIGP-?(?:DI|M)\b",
    r"Casa Azul", r"AQUA-?HQE", r"GBC Brasil",
    r"\bSchneider\b", r"\bDancor\b", r"\bLepono\b", r"\bKomeco\b", r"\bAmanco\b", r"\bFortlev\b",
    r"Netuno\s*4", r"\b652\b", r"Brasil\b", r"Brazil", r"Brasileir", r"Brazilian",
    r"\bUF\b", r"concession[aá]ri", r"\bconcessionaire", r"\bTFDI\b",
)
PADRAO_DO_BRASIL = re.compile("|".join(f"(?:{t})" for t in TERMOS_DO_BRASIL), re.IGNORECASE)

_AUTORIA = re.compile(
    r"UFSC|Universidade Federal de Santa Catarina|Grupo de Pesquisa em Ambientes Sustent"
    r"|Sustainable Environments Research Group", re.IGNORECASE)


def cita_o_brasil(texto: str) -> bool:
    """O texto (puro) cita algum termo do Brasil fora da autoria institucional."""
    return bool(PADRAO_DO_BRASIL.search(_AUTORIA.sub("", texto)))

