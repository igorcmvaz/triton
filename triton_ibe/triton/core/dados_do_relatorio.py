"""Os resultados que o relatório (PDF/HTML), o JSON e o CAD mostram para um volume.

Antes da 0.1.0 a aba de relatórios lia a economia por ``tab_economic.last_econ_res``,
atributo que a aba econômica não define: o laudo saía com investimento, VPL e TIR
iguais a zero, como se calculados. Para volumes fora da varredura, interpolava
potencial, VPL e investimento entre os volumes vizinhos. E escolhia o volume do
otimizador depois de já ter lido os indicadores hídricos de outro.

A regra aqui é a do programa todo: o que aparece vem do cálculo, para o volume do
relatório; o que não foi calculado fica ``None``, e o documento diz «Não calculado».
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, Optional

#: Texto dos documentos quando o indicador não foi calculado para o volume.
NAO_CALCULADO = "Não calculado"
NAO_CALCULADO_EN = "Not calculated"

#: Indicadores hídricos que o relatório mostra; ``None`` quando não simulados.
CHAVES_HIDRICAS = ("potential_pct", "pluv_day", "potable_day", "spill_day", "sat_full", "sat_null")
#: Indicadores econômicos que o relatório mostra; ``None`` quando não calculados.
CHAVES_ECONOMICAS = ("capex", "annual_gross", "vpl", "tir", "payback_s", "payback_d")

_TOLERANCIA_L = 0.5


def _mesmo_volume(a: Any, b: Any) -> bool:
    try:
        return abs(float(a) - float(b)) < _TOLERANCIA_L
    except (TypeError, ValueError):
        return False


def _numero(valor: Any) -> Optional[float]:
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return None
    return v if v == v and v not in (float("inf"), float("-inf")) else None


def volume_do_relatorio(
    selecionado: Optional[float] = None,
    tipo: str = "economic",
    topsis: Any = None,
    otimo_economico: Optional[float] = None,
    otimo_ambiental: Optional[float] = None,
    single: Any = None,
    sweep: Any = None,
) -> Optional[float]:
    """O volume que o relatório documenta, decidido antes de ler qualquer indicador.

    Ordem: o escolhido pelo usuário; o ótimo do tipo de laudo (ambiental no laudo
    ambiental, econômico nos demais) pelo otimizador ou pela aba que o calculou; a
    simulação única; o ótimo técnico da varredura. Sem nada disso, ``None``: o laudo
    não inventa um volume.
    """
    if selecionado is not None:
        return float(selecionado)
    candidatos = list(getattr(topsis, "candidates", None) or [])
    if candidatos:
        indice = getattr(topsis, "environmental_best_index" if tipo == "environmental"
                         else "financial_best_index", None)
        if indice is not None and 0 <= int(indice) < len(candidatos):
            return float(candidatos[int(indice)].lower_tank_vol)
    otimo = otimo_ambiental if tipo == "environmental" else otimo_economico
    if otimo is not None and float(otimo) > 0:
        return float(otimo)
    if single is not None:
        return float(single.lower_tank_vol)
    if sweep is not None:
        otimo_tecnico = getattr(sweep, "optimal_lower_tank_vol", None)
        if otimo_tecnico:
            return float(otimo_tecnico)
        positivos = [r.lower_tank_vol for r in (getattr(sweep, "results_by_volume", None) or [])
                     if r.lower_tank_vol > 0]
        if positivos:
            return float(positivos[0])
    return None


def indicadores_hidricos(volume: Optional[float], sweep: Any = None, single: Any = None) -> Dict[str, Optional[float]]:
    """Potencial, consumos e atendimento do volume, como a simulação os calculou.

    Procura o volume na varredura e na simulação única. Fora delas, nada é
    interpolado: os indicadores ficam ``None``.
    """
    vazio: Dict[str, Optional[float]] = {k: None for k in CHAVES_HIDRICAS}
    if volume is None:
        return vazio
    linhas: Iterable[Any] = list(getattr(sweep, "results_by_volume", None) or [])
    if single is not None:
        linhas = list(linhas) + [single]
    r = next((r for r in linhas if _mesmo_volume(r.lower_tank_vol, volume)), None)
    if r is None:
        return vazio
    return {
        "potential_pct": _numero(getattr(r, "potential_potable_savings_pct", None)),
        "pluv_day": _numero(getattr(r, "avg_pluvial_consumed_l_day", None)),
        "potable_day": _numero(getattr(r, "avg_potable_consumed_l_day", None)),
        "spill_day": _numero(getattr(r, "avg_spilled_l_day", None)),
        "sat_full": _numero(getattr(r, "pct_days_full_satisfaction", None)),
        "sat_null": _numero(getattr(r, "pct_days_null_satisfaction", None)),
    }


def indicadores_economicos(
    volume: Optional[float],
    varredura_economica: Optional[Dict[Any, Dict[str, Any]]] = None,
    ultimo: Any = None,
    volume_do_ultimo: Optional[float] = None,
    topsis: Any = None,
    cenarios: Optional[Iterable[Dict[str, Any]]] = None,
) -> Dict[str, Optional[float]]:
    """Investimento, economia do 1º ano, VPL, TIR e paybacks do volume.

    Fontes, na ordem: o resultado da análise do volume ativo (``last_result``), se for
    este volume, que é o que a Etapa 5 mostra nos indicadores; a varredura econômica
    da Etapa 5 (``last_sweep_econ_results``); a linha do otimizador
    (``last_scenario_results``) e, por fim, o candidato TOPSIS com o mesmo volume. As
    duas últimas não trazem o payback simples (o «payback» do otimizador é o
    descontado, ou o simples quando aquele não existe). Fora delas, ``None``.
    """
    vazio: Dict[str, Optional[float]] = {k: None for k in CHAVES_ECONOMICAS}
    if volume is None:
        return vazio
    if ultimo is not None and volume_do_ultimo is not None and _mesmo_volume(volume_do_ultimo, volume):
        fluxos = list(getattr(ultimo, "annual_cash_flows", None) or [])
        bruto = _numero(getattr(fluxos[1], "total_gross_savings_brl", None)) if len(fluxos) > 1 else None
        return {
            "capex": _numero(getattr(ultimo, "total_investment", None)),
            "annual_gross": bruto,
            "vpl": _numero(getattr(ultimo, "vpl", None)),
            "tir": _numero(getattr(ultimo, "tir_pct", None)),
            "payback_s": _numero(getattr(ultimo, "payback_simple_years", None)),
            "payback_d": _numero(getattr(ultimo, "payback_discounted_years", None)),
        }
    for linha in (varredura_economica or {}).values():
        if isinstance(linha, dict) and _mesmo_volume(linha.get("volume_l"), volume):
            bruto_mensal = _numero(linha.get("gross_monthly"))
            return {
                "capex": _numero(linha.get("capex")),
                "annual_gross": bruto_mensal * 12.0 if bruto_mensal is not None else None,
                "vpl": _numero(linha.get("vpl")),
                "tir": _numero(linha.get("tir")),
                "payback_s": _numero(linha.get("payback_simple")),
                "payback_d": _numero(linha.get("payback_discounted")),
            }
    for linha in list(cenarios or []):
        if isinstance(linha, dict) and _mesmo_volume(linha.get("vol"), volume):
            bruto_mensal = _numero(linha.get("gross_m"))
            return {
                "capex": _numero(linha.get("capex")),
                "annual_gross": bruto_mensal * 12.0 if bruto_mensal is not None else None,
                "vpl": _numero(linha.get("vpl")),
                "tir": _numero(linha.get("tir")),
                "payback_s": None,
                "payback_d": _numero(linha.get("payback_discounted")),
            }
    for c in list(getattr(topsis, "candidates", None) or []):
        if _mesmo_volume(c.lower_tank_vol, volume):
            return {
                "capex": _numero(getattr(c, "capex_brl", None)),
                "annual_gross": None,
                "vpl": _numero(getattr(c, "vpl_brl", None)),
                "tir": _numero(getattr(c, "irr_pct", None)),
                "payback_s": None,
                "payback_d": _numero(getattr(c, "discounted_payback_years", None)),
            }
    return vazio


def demanda_total_diaria(config: Any) -> Optional[float]:
    """Demanda total da edificação em L/dia, pelo projeto: per capita × moradores ou total.

    ``None`` quando o projeto não a declara; o desenho não supõe 1.000 L/dia.
    """
    if config is None:
        return None
    try:
        valor = float(getattr(config, "demand_value", 0.0) or 0.0)
    except (TypeError, ValueError):
        return None
    if valor <= 0:
        return None
    # demand_type 0: per capita (L/hab/dia); 1: total da edificação (L/dia).
    if int(getattr(config, "demand_type", 0) or 0) == 0:
        moradores = float(getattr(config, "residents_count", 0) or 0)
        return valor * moradores if moradores > 0 else None
    return valor


# ── Texto das exportações (DXF, SVG, planilhas) fora da Edição Brasil ──────────────────────
#
# As pranchas e os diagramas citam normas brasileiras (ABNT NBR 15527, 5626, 6492, 12214) em
# títulos, quadros e notas. Fora da Brasil, a citação sai e a frase continua inteira; onde a
# frase só existia para citar a norma, o texto fica genérico («normas aplicáveis»). Nenhum
# número de norma é posto no lugar.

_NBR = r"(?:ABNT\s+)?NBR\s*\d{3,5}(?::\d{4})?"
_NBR_LISTA = _NBR + r"(?:\s*(?:/|,|E|e|and)\s*" + _NBR + r")*"
_REGRAS_DE_EXPORTACAO = (
    (re.compile(r"e\s+" + _NBR + r"\s*\(suc[cç][aã]o\)"), "e por limite de velocidade (sucção)"),
    # «CONFORME ABNT NBR 15527:2019 E NBR 5626 | ESCALA INDICADA»
    (re.compile(r"CONFORME\s+" + _NBR_LISTA), "CONFORME AS NORMAS APLICÁVEIS"),
    (re.compile(r"conforme\s+" + _NBR_LISTA), "conforme as normas aplicáveis"),
    # «(NBR 15527)», «(ABNT NBR 15527 / NBR 5626)», «(NBR 15527:2019)» inteiros
    (re.compile(r"\s*\(\s*" + _NBR_LISTA + r"\s*\)"), ""),
    # «(NBR 5626, D_suc > D_rec)» -> «(D_suc > D_rec)»
    (re.compile(r"\(\s*" + _NBR_LISTA + r"\s*,\s*"), "("),
    # «(Sucção — NBR 5626)» -> «(Sucção)»
    (re.compile(r"\s*[—–-]\s*" + _NBR_LISTA + r"(?=\s*\))"), ""),
    # «ESCALA 1:10 | NBR 15527», «ESCALA 1:15 | NBR 5626 E NBR 15527»
    (re.compile(r"\s*\|\s*" + _NBR_LISTA), ""),
    # «e NBR 5626 (sucção)» numa nota
    (re.compile(r"\s+e\s+" + _NBR_LISTA), ""),
    # «Norma de referência: ABNT NBR 5626:2020 item 4.4»
    (re.compile(r"Normas? de refer[eê]ncia:\s*" + _NBR_LISTA + r"(?:\s*item\s*[\d.]+)?(?:\s*\([^)]*\))?(?:\s*e\s*" + _NBR + r"(?:\s*item\s*[\d.]+)?)?"), "Norma de referência: a do local do projeto"),
    (re.compile(_NBR_LISTA), "norma de referência"),
    (re.compile(r"\bABNT\b"), ""),
    (re.compile(r"MUNICÍPIO:"), "LOCAL:"),
    (re.compile(r"CELESC|CASAN"), "entidade local"),
)


def texto_de_exportacao(texto: str) -> str:
    """O texto de uma exportação sem as normas e entidades do Brasil, fora da Edição Brasil.

    Na Brasil o texto volta como veio (as exportações da BRL não mudam).
    """
    if not texto or not isinstance(texto, str):
        return texto
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        return texto
    for padrao, alvo in _REGRAS_DE_EXPORTACAO:
        texto = padrao.sub(alvo, texto)
    return re.sub(r"[ \t]{2,}", " ", texto).replace(" )", ")").replace("( ", "(")


def simbolo_da_moeda(dados: Optional[Dict[str, Any]]) -> str:
    """O símbolo de moeda das exportações: o do projeto; senão o da edição («R$» na Brasil, «€» na Portugal).

    Na Internacional, sem moeda escolhida, devolve ``""``: o chamador escreve «moeda não definida»
    (nunca «R$» nem «BRL»). O sinal «¤» da tela vale como «não escolhida».
    """
    simbolo = str((dados or {}).get("moeda") or "").replace("¤", "").strip()
    if simbolo:
        return simbolo
    from triton.core.edition import get_edition_currency_symbol
    return get_edition_currency_symbol() or ""


#: Texto que o núcleo escreve com entidades do Brasil e que as planilhas repetem (fora da Brasil).
_REGRAS_DE_PLANILHA = (
    (re.compile(r"\((?:[Tt]arifa [^)]*)?CELESC[^)]*\)"), "(tarifa de eletricidade do local)"),
    (re.compile(r"IPTU Verde"), "incentivo municipal ao imposto predial"),
    (re.compile(r"IPTU"), "imposto predial"),
    (re.compile(r"\(SINAPI\)"), "(catálogo de preços de referência)"),
    (re.compile(r"SINAPI"), "catálogo de preços de referência"),
    (re.compile(r"Florianópolis"), "o local do projeto"),
    (re.compile(r"ANEEL"), "regulador de energia"),
)


def texto_de_planilha(texto: Any, moeda: str = "") -> Any:
    """O texto de uma célula sem marcas do Brasil, fora da Edição Brasil (na Brasil volta como veio).

    ``moeda`` é o símbolo do projeto; vazio, «R$» vira «moeda» (a Internacional não tem moeda
    predefinida).
    """
    if not isinstance(texto, str) or not texto:
        return texto
    from triton.core.edition import sem_marcas_do_brasil, usa_dados_do_brasil
    if usa_dados_do_brasil():
        return texto
    from triton.core.environmental_justifications import _sem_residuos_do_brasil
    texto = _sem_residuos_do_brasil(sem_marcas_do_brasil(texto, "pt"))
    texto = texto_de_exportacao(texto)
    for padrao, alvo in _REGRAS_DE_PLANILHA:
        texto = padrao.sub(alvo, texto)
    return texto.replace("R$", moeda or "moeda")


def planilha_de_exportacao(wb: Any, moeda: str = "") -> None:
    """Aplica ``texto_de_planilha`` a toda célula de texto da pasta de trabalho (fora da Edição Brasil)."""
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        return
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for celula in linha:
                if isinstance(celula.value, str):
                    celula.value = texto_de_planilha(celula.value, moeda)


def svg_de_exportacao(svg: str) -> str:
    """O SVG sem as normas do Brasil (e sem os comentários do gerador), fora da Edição Brasil."""
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil() or not svg:
        return svg
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    return texto_de_exportacao(svg)


def documento_dxf_de_exportacao(doc: Any) -> None:
    """Tira as normas do Brasil dos textos de um desenho ezdxf antes de gravá-lo (fora da Brasil)."""
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        return
    espacos = [doc.modelspace()] + [bloco for bloco in doc.blocks if not bloco.name.startswith("*")]
    for espaco in espacos:
        for entidade in espaco.query("TEXT MTEXT ATTDEF"):
            if entidade.dxftype() == "MTEXT":
                entidade.text = texto_de_exportacao(entidade.text)
            else:
                entidade.dxf.text = texto_de_exportacao(entidade.dxf.text)
        for entidade in espaco.query("INSERT"):
            for atributo in entidade.attribs:
                atributo.dxf.text = texto_de_exportacao(atributo.dxf.text)


#: As moedas que a Etapa 3 oferece, na ordem da lista antiga (o índice ``currency``): as cinco
#: primeiras não mudam de lugar, para que os arquivos antigos continuem lidos. ``XXX`` é o
#: código ISO 4217 de «sem moeda»: a Internacional não tem moeda predefinida (decisão U-21) e
#: mostra o sinal genérico de moeda («¤») até o usuário escolher a sua.
MOEDAS = (("BRL", "R$"), ("USD", "$"), ("EUR", "€"), ("GBP", "£"), ("CNY", "¥"),
          ("XXX", "¤"), ("ZAR", "R"), ("INR", "₹"), ("AUD", "A$"), ("CAD", "C$"), ("CHF", "CHF"))
#: A ordem em que a Internacional as oferece: primeiro «sem moeda definida». O real não entra.
MOEDAS_DA_INTERNACIONAL = ("XXX", "USD", "EUR", "GBP", "CNY", "ZAR", "INR", "AUD", "CAD", "CHF")


def moeda_do_projeto(ui_state: Optional[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    """O código e o símbolo da moeda gravados no projeto (``ui_state.stage3``).

    ``None`` quando o arquivo não a declara (CSV legado, projeto da CLI): a saída
    diz «moeda do projeto», e não supõe o real.
    """
    etapa3 = dict((ui_state or {}).get("stage3") or {})
    codigo = etapa3.get("currency_code")
    if not codigo and etapa3.get("currency") is not None:
        try:
            indice = int(etapa3.get("currency"))
        except (TypeError, ValueError):
            indice = -1
        codigo = MOEDAS[indice][0] if 0 <= indice < len(MOEDAS) else None
    simbolo = dict(MOEDAS).get(str(codigo or ""))
    return {"code": str(codigo), "symbol": simbolo} if simbolo else None


def resultados_para_csv_legado(sweep: Any = None, single: Any = None) -> list:
    """As linhas de resultado do CSV do Netuno 4: a varredura, ou a simulação única.

    Sem varredura, o CSV saía sem nenhuma linha de resultado, mesmo com a
    simulação de um volume feita.
    """
    linhas = list(getattr(sweep, "results_by_volume", None) or [])
    if not linhas and single is not None:
        linhas = [single]
    return linhas
