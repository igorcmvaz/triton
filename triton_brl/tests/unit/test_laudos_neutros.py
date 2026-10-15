# -*- coding: utf-8 -*-
"""Os três laudos (executivo, auditoria ambiental, dossiê técnico) e as exportações por edição.

- BRL: o laudo em português sai exatamente como saía antes da neutralização (impressão digital do
  texto, calculada no commit ce458c3, a BRL anterior ao WIP de neutralização).
- INT e PRT: nenhum termo do Brasil em nenhum idioma, a partir de projeto neutro, gerado em memória.
- Laudo em inglês: sem palavras-guia em português, nas três edições.
- PRT: português de Portugal. INT sem moeda escolhida: sem «R$», «BRL» nem símbolo inventado.
- DXF, SVG e planilhas sem NBR, ABNT, CELESC nem «R$» fora da Brasil.
"""

from __future__ import annotations

import copy
import hashlib
import html as _html
import re

import pytest

pytest.importorskip("PySide6")

from triton.core.edition import usa_dados_do_brasil  # noqa: E402

#: Os dados do Brasil (fatores da rede, tarifas) só existem na pasta da BRL: os testes que exigem a BRL
#: de verdade rodam só lá.
so_na_brl = pytest.mark.skipif(not usa_dados_do_brasil(), reason="exige os dados da Edição Brasil")

EDICOES = ("INT", "PRT")
TIPOS = ("economic", "environmental", "research")
IDIOMAS = ("pt", "en", "es", "zh")

#: Termos do Brasil que não podem aparecer fora da BRL (a lista da ESPECIFICACAO_DE_NEUTRALIDADE).
BRASIL = re.compile(
    r"NBR|ABNT|MCTI|SIRENE|Dancor|Amanco|(?-i:\bCREA\b|\bCAU\b|\bCRQ\b|\bCAIXA\b)|SINAPI|SNIS|IPTU|ANEEL|oncession[aá]ri|R\$|BRL|"
    r"CELESC|CASAN|Florian|Brasil|Brazil|Netuno|AQUA-HQE|Casa Azul|Fortlev|SIDAC|"
    r"Vanzolini|brasileir|Komeco|Schneider|Lepono|Inmetro|INMETRO", re.I)

#: Palavras-guia do português que não podem sobrar num laudo em inglês.
PORTUGUES = re.compile(
    r"\b(Laudo|Reservat\w+|Substitui\w+|Pot[aá]vel|Economia|Edifica\w+|Empreendimento|Concession\w+|"
    r"Respons[aá]vel|Termo|Parecer|anos|Horizonte|[AÁ]gua|Cisterna|Resultado|Premissas|Fatores|Tubula\w+|"
    r"Motobomba|Estágios|Dimensionamento|acumulados|empreendimento|certifica\w+|categoria|pontos|limiar|"
    r"descarte|rendimento|dosagem|Reserva|Principal)\b|[ãõç]")


def _dados(moeda: str = "", capex: float = 9500.0) -> dict:
    return {
        "ref_code": "TST-001", "project_name": "Test project", "rain_file": "series.csv",
        "area": 250.0, "runoff": 0.85, "discard": 2.0, "residents": 5, "demand": 150.0, "share": 0.40,
        "lower_vol": 5000.0, "potential_pct": 35.5, "pluv_day": 120.0, "potable_day": 180.0, "spill_day": 40.0,
        "sat_full": 80.0, "sat_null": 10.0, "capex": capex, "annual_gross": 3200.0, "vpl": 28500.0, "tir": 26.5,
        "payback_s": 4.1, "payback_d": 5.5, **({"moeda": moeda} if moeda else {}),
        "audit_context": {"analysis_period_years": 20, "climate_location": "Test site",
                          "climate_basis": "Observed series", "climate_period": "1991-2020", "tariff_location": "Test site"},
        "system_design": {"upper_used": True, "upper_volume_l": 500.0, "pump_power_cv": "1/2", "pump_power_kw": 0.37,
                          "pump_flow_l_h": 3000.0, "pump_count": 1, "pump_threshold_pct": "50"},
        "optima": {k: {"volume": v, "water_saved": 140.0, "vpl": 40000.0, "co2": 300.0, "capex": 12000.0}
                   for k, v in (("technical", 8000.0), ("economic", 6000.0), ("environmental", 5000.0), ("balanced", 6500.0))},
        "topsis_criterion_labels": ["Potencial máximo", "Maior VPL", "Menor CO2"],
        "topsis_criterion_weights": [0.34, 0.33, 0.33],
        "topsis_candidates": [
            {"volume": 5000.0, "saving": 44.0, "water_m3": 136.0, "potable_m3": 140.0, "overflow_m3": 52.0, "capex": 11800.0,
             "vpl": 48000.0, "co2": 340.0, "score": 0.78, "rank": 2, "discounted_payback": 5.2, "irr": 28.0},
            {"volume": 6500.0, "saving": 47.0, "water_m3": 145.0, "potable_m3": 131.0, "overflow_m3": 43.0, "capex": 14000.0,
             "vpl": 53500.0, "co2": 325.0, "score": 0.91, "rank": 1, "discounted_payback": 5.0, "irr": 30.5, "is_best": True}],
        "sweep_points": [
            {"volume": 5000.0, "saving": 44.0, "pluvial_m3": 136.0, "potable_m3": 140.0, "spill_m3": 52.0, "sat_full": 78.0},
            {"volume": 6500.0, "saving": 47.0, "pluvial_m3": 145.0, "potable_m3": 131.0, "spill_m3": 43.0, "sat_full": 83.0}],
    }


def _laudo(tipo: str, lang: str, dados: dict | None = None) -> str:
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    from triton.core.report_service import generate_report_html
    dados = copy.deepcopy(_dados() if dados is None else dados)
    kw = {}
    if tipo != "economic":
        kw["lca_result"] = calculate_lca(10000.0, 160.0, EnvironmentalConfig(material_key="PEAD"))
    return generate_report_html(tipo, dados, lang=lang, **kw)


def _texto(html: str) -> str:
    """O texto visível: sem CSS, sem SVG, sem imagens embutidas, sem tags."""
    html = re.sub(r"<style.*?</style>|<svg.*?</svg>|data:image[^\"']*", "", html, flags=re.S)
    return _html.unescape(re.sub(r"<[^>]+>", " ", html))


@pytest.fixture(autouse=True)
def _idioma_restaurado():
    from triton.ui.translation import get_current_lang, set_current_lang
    antes = get_current_lang()
    yield
    set_current_lang(antes)


# ── BRL inalterada ───────────────────────────────────────────────────────────────────────────

#: SHA-256 do texto normalizado de cada laudo em português da BRL, gerado a partir de ``_dados()``
#: no commit ce458c3. Se uma mudança intencional na BRL mexer num laudo, recalcule e justifique.
IMPRESSAO_DIGITAL_BRL_PT = {
    "economic": "9541d31d4ea2be1dd4f881517132f6889f64f8ecd1566907ed21410393a0be31",
    "environmental": "ab45e8788fe49bfb8aa646ed974fdc0182dc125f1565461362901f36efe437e5",
    "research": "cdecde922de69f1d59c2de58e517820233b149a0368d4ffa9f7ab28a0b22f8a1",
}


def _normalizado(html: str) -> str:
    from datetime import datetime
    html = re.sub(r"\d{2}/\d{2}/\d{4}", "DATA", html)
    return html.replace(str(datetime.now().year), "ANO")


def impressao_digital(tipo: str) -> str:
    return hashlib.sha256(_normalizado(_laudo(tipo, "pt")).encode("utf-8")).hexdigest()


@so_na_brl
def test_laudos_em_portugues_da_brl_continuam_iguais(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    for tipo in TIPOS:
        assert impressao_digital(tipo) == IMPRESSAO_DIGITAL_BRL_PT[tipo], (
            f"o laudo «{tipo}» em português da BRL mudou; a BRL não pode mudar")


@so_na_brl
def test_brl_mantem_normas_e_entidades_do_brasil(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    texto = _texto(_laudo("economic", "pt")) + _texto(_laudo("environmental", "pt")) + _texto(_laudo("research", "pt"))
    for termo in ("ABNT NBR 15527", "CREA", "MCTI/SIRENE", "Concessionária", "R$"):
        assert termo in texto, termo


# ── INT e PRT sem o Brasil ───────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("edicao", EDICOES)
@pytest.mark.parametrize("lang", IDIOMAS)
@pytest.mark.parametrize("tipo", TIPOS)
def test_laudo_sem_termo_do_brasil(monkeypatch, edicao, lang, tipo):
    monkeypatch.setenv("TRITON_EDITION", edicao)
    for dados in (_dados(moeda="€"), _dados(), {}):
        texto = _texto(_laudo(tipo, lang, dados))
        achados = sorted({m.group(0) for m in BRASIL.finditer(texto)})
        assert not achados, f"{edicao}/{lang}/{tipo}: {achados}"


@pytest.mark.parametrize("edicao", EDICOES)
def test_justificativas_de_acv_sem_termo_do_brasil(monkeypatch, edicao):
    monkeypatch.setenv("TRITON_EDITION", edicao)
    from triton.core import environmental_justifications as j
    texto = "\n".join(_texto(f()) for f in (
        j.generate_html_justifications_materials, j.generate_html_justifications_pipes,
        j.generate_html_justifications_pumps, j.generate_html_justifications_operational))
    assert not sorted({m.group(0) for m in BRASIL.finditer(texto)})


# ── Laudo em inglês de verdade ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("edicao", ("BRL", "INT", "PRT"))
@pytest.mark.parametrize("tipo", TIPOS)
def test_laudo_em_ingles_sem_palavras_em_portugues(monkeypatch, edicao, tipo):
    if edicao == "BRL" and not usa_dados_do_brasil():
        pytest.skip("exige os dados da Edição Brasil")
    monkeypatch.setenv("TRITON_EDITION", edicao)
    for dados in (_dados(moeda="€"), {}):
        texto = _texto(_laudo(tipo, "en", dados))
        # a lista do TOPSIS vem do projeto (rótulos do usuário) e o dossiê cita o nome de uma planilha
        texto = texto.replace("Potencial máximo", "").replace("Maior VPL", "").replace("Menor CO2", "")
        texto = texto.replace("Florianópolis", "").replace("Fundação Vanzolini", "")  # nomes próprios da BRL
        achados = sorted({m.group(0) for m in PORTUGUES.finditer(texto)})
        assert not achados, f"{edicao}/{tipo}: {achados}"


def test_laudo_executivo_em_ingles_tem_o_corpo_em_ingles(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "INT")
    texto = _texto(_laudo("economic", "en"))
    for frase in ("Executive Technical Report", "Lower Cistern", "Potable-Water Savings", "Simple Payback"):
        assert frase in texto, frase


# ── Edição, moeda, normas ────────────────────────────────────────────────────────────────────

def test_int_sem_moeda_escolhida_nao_inventa_simbolo(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "INT")
    for tipo in ("economic", "research"):
        texto = _texto(_laudo(tipo, "en"))
        assert "currency" in texto.lower() and "not set" in texto, tipo
        assert "¤" not in texto and "€" not in texto and "R$" not in texto, tipo


def test_int_com_moeda_escolhida_usa_a_do_projeto(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "INT")
    texto = _texto(_laudo("economic", "en", _dados(moeda="£")))
    assert "£ 28,500.00" in texto and "not set" not in texto


def test_norma_da_internacional_e_generica_e_a_de_portugal_e_en_16941(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "INT")
    texto = _texto(_laudo("economic", "en"))
    assert "applicable at the project site, to be stated by the responsible engineer" in texto
    assert not re.search(r"\b(EN|ISO|NP)\s*\d{3,}", texto)
    monkeypatch.setenv("TRITON_EDITION", "PRT")
    assert "EN 16941-1" in _texto(_laudo("economic", "pt"))


def test_portugal_em_portugues_de_portugal(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "PRT")
    for tipo in TIPOS:
        html = _laudo(tipo, "pt", _dados(moeda="€"))
        texto = _texto(html)
        assert re.search(r"lang=[\"']pt-PT", html), tipo
        for brasileiro in ("Laudo", "laudo", "Edificação", "Concessionária", "usuário", "Premissas", "Economia Potável"):
            assert brasileiro not in texto, (tipo, brasileiro)
    assert "Relatório Técnico Executivo" in _texto(_laudo("economic", "pt", _dados(moeda="€")))
    assert "Portugal Edition (PRT)" in _texto(_laudo("economic", "en", _dados(moeda="€")))


def test_data_do_laudo_em_ingles_fora_da_brasil_e_iso(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "INT")
    assert re.search(r"Issued:\s*\d{4}-\d{2}-\d{2}", _texto(_laudo("economic", "en")))


# ── Custos em branco (exemplos de INT e PRT não trazem custos locais) ─────────────────────────

@pytest.mark.parametrize("edicao,lang,frase", (
    ("INT", "en", "Investment, maintenance and electricity costs were not informed: the economic result shows only the "
                  "savings on the water bill; payback and NPV are not meaningful until costs are entered"),
    ("PRT", "pt", "Os custos de investimento, manutenção e eletricidade não foram indicados"),
))
@pytest.mark.parametrize("tipo", ("economic", "research", "environmental"))
def test_custos_em_branco_sao_avisados_e_nao_viram_resultado(monkeypatch, edicao, lang, frase, tipo):
    monkeypatch.setenv("TRITON_EDITION", edicao)
    dados = _dados(moeda="€", capex=0)
    dados.update(vpl=0.0, tir=0.0, payback_s=0.0, payback_d=0.0, fator_rede_nao_informado=True)
    texto = _texto(_laudo(tipo, lang, dados))
    assert re.sub(r"\s+", " ", frase) in re.sub(r"\s+", " ", texto)
    if tipo == "economic":
        assert not re.search(r"(?<![\d.,])0[.,]0 (years|anos)", texto)
        assert not re.search(r"€\s*0[.,]00(?!\d)", texto)
        assert "Not calculated" in texto or "Não calculado" in texto
    assert ("grid emission factor" in texto) or ("fator de emissão da rede" in texto)


@so_na_brl
def test_brl_nunca_mostra_o_aviso_de_custos(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    dados = _dados(capex=0)
    dados.update(fator_rede_nao_informado=True, custos_nao_informados=True)
    texto = _texto(_laudo("economic", "pt", dados)) + _texto(_laudo("environmental", "pt", dados))
    assert "não foram informados" not in texto and "não foi informado" not in texto


# ── Exportações ──────────────────────────────────────────────────────────────────────────────

EXPORT_BRASIL = re.compile(r"NBR|ABNT|CELESC|CASAN|R\$|MUNIC[IÍ]PIO|IPTU|SINAPI|Florian|Amanco|Dancor|MCTI", re.I)


@pytest.mark.parametrize("edicao", EDICOES)
@pytest.mark.parametrize("modo", ("technical_a3", "simple"))
def test_dxf_e_svg_sem_norma_do_brasil(monkeypatch, tmp_path, edicao, modo):
    monkeypatch.setenv("TRITON_EDITION", edicao)
    import ezdxf
    from triton.core.cad_exporter import generate_project_dxf, generate_project_svg_diagram
    dados = {"project_name": "P", "ref_code": "T-1", "area": 120.0, "residents": 4, "demand": 150.0, "share": 0.5,
             "lower_vol": 5000.0, "audit_context": {"climate_location": "Site"}}
    destino = tmp_path / f"{modo}.dxf"
    generate_project_dxf(dados, str(destino), mode=modo)
    doc = ezdxf.readfile(str(destino))
    textos = [e.dxf.text for e in doc.modelspace().query("TEXT")] + [e.text for e in doc.modelspace().query("MTEXT")]
    nomes = [s.dxf.name for s in doc.dimstyles]
    achados = {m.group(0) for m in EXPORT_BRASIL.finditer("\n".join(textos + nomes))}
    assert not achados, achados
    svg = generate_project_svg_diagram(dados, str(tmp_path / f"{modo}.svg"), mode=modo)
    assert not {m.group(0) for m in EXPORT_BRASIL.finditer(svg)}


@so_na_brl
def test_dxf_da_brl_continua_com_a_norma(monkeypatch, tmp_path):
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    import ezdxf
    from triton.core.cad_exporter import generate_project_dxf
    destino = tmp_path / "a3.dxf"
    generate_project_dxf({"project_name": "P"}, str(destino), mode="technical_a3")
    doc = ezdxf.readfile(str(destino))
    texto = " ".join(e.dxf.text for e in doc.modelspace().query("TEXT"))
    assert "NBR 15527" in texto and "MUNICÍPIO" in texto
    assert "ABNT_TRITON" in [s.dxf.name for s in doc.dimstyles]


@pytest.mark.parametrize("edicao", EDICOES)
def test_planilha_de_auditoria_sem_marca_do_brasil(monkeypatch, tmp_path, edicao):
    monkeypatch.setenv("TRITON_EDITION", edicao)
    import numpy as np
    import openpyxl
    from triton.core.economic import run_economic_analysis
    from triton.core.edition import configuracao_da_edicao
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    from triton.core.exportar_tudo import exportar_tudo
    from triton.core.simulation import run_single_simulation
    from triton.core.study_layout import generate_study_layout
    rng = np.random.default_rng(7)
    chuva = np.where(rng.random(730) < 0.35, rng.exponential(12, 730), 0.0)
    cfg = configuracao_da_edicao()
    cfg.water_tariffs = [(0.0, 0.0, 12.0, -1), (0.0, 10.0, 4.0, 1), (10.0, 20.0, 6.0, 1), (20.0, 999999.0, 8.0, 1)]
    cfg.sewage_mode, cfg.sewage_rate = 1, 80.0
    sim = run_single_simulation(chuva, 5000.0, area=150, total_demand_per_day=400, rainwater_share=0.4, store_daily_details=True)
    m3 = sim.avg_pluvial_consumed_l_day * 0.365
    dados = {"project_name": "Audit", "lower_vol": 5000, "upper_vol": 1000, "area": 150}
    dados.update(generate_study_layout(dados))
    caminho = tmp_path / "audit.xlsx"
    exportar_tudo(str(caminho), config=cfg, project_data=dados, single_result=sim,
                  economic_result=run_economic_analysis(cfg, sim),
                  environmental_result=calculate_lca(5000.0, m3, EnvironmentalConfig(annual_water_saved_m3=m3)))
    wb = openpyxl.load_workbook(caminho)
    # os nomes de campo da configuração (iptu_*, *_brl) são identificadores do arquivo de projeto
    pat = re.compile(r"NBR|ABNT|CELESC|CASAN|R\$|IPTU|SINAPI|Florian|Amanco|Dancor|MCTI|SIRENE|oncession")
    achados = {(ws.title, c.value[:60]) for ws in wb for linha in ws.iter_rows() for c in linha
               if isinstance(c.value, str) and pat.search(c.value)}
    assert not achados, sorted(achados)[:5]


# ── Nomes de arquivo sugeridos ───────────────────────────────────────────────────────────────

def test_nomes_sugeridos_levam_a_edicao_e_nao_ficam_em_portugues(monkeypatch):
    from triton.ui.translation import set_current_lang
    set_current_lang("en")
    from triton.ui.tab_export import nome_sugerido
    monkeypatch.setenv("TRITON_EDITION", "INT")
    assert nome_sugerido("projeto_triton") == "triton_project_INT"
    assert nome_sugerido("_Dados_Simulados") == "_Simulated_Data_INT"
    monkeypatch.setenv("TRITON_EDITION", "BRL")
    assert nome_sugerido("projeto_triton") == "projeto_triton"
