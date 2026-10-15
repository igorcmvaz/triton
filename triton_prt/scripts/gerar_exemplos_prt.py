# -*- coding: utf-8 -*-
"""Gera os três projetos de exemplo da Edição Portugal: Lisboa, Porto e Funchal.

A edificação é a do tutorial do manual (150 m² de telhado, quatro residentes, 150 L/hab·dia,
28% não potável), igual nas três cidades, para que os resultados se comparem. Muda o local:

- chuva: Lisboa e Porto usam a base E-OBS por concelho (normal 1991–2020; o ficheiro guarda a
  referência da série, e o programa recompõe-na da base ao abrir). O Funchal usa a série ERA5
  de ``data/rainfall/Funchal.csv`` (a E-OBS não cobre o Funchal: 22% de dias sem dados);
- tarifário: o transcrito em ``triton/data/portugal_tarifarios.json`` (Lisboa: EPAL e Câmara;
  Porto: Águas e Energia do Porto; Funchal: Câmara Municipal), com vigência e fontes;
- eletricidade: só no Funchal, a Tarifa Base da EEM (0,1673 €/kWh, sem IVA), fonte secundária;
- custos de obra, bomba e manutenção: **não** se inventam; ficam a zero, e o projeto diz-o.
  O utilizador introduz os seus (etapa 5); sem eles a análise mostra só a poupança na fatura.

    python scripts/gerar_exemplos_prt.py

Não depende do manual-fonte (``manual/gerar_tabelas.py``, fora do Git): os números do tutorial
estão copiados abaixo.
"""

from __future__ import annotations

import os
import sys

os.environ["TRITON_EDITION"] = "PRT"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from triton.core import base_climatica_portugal as pt  # noqa: E402
from triton.core import tarifarios_portugal as tarifas  # noqa: E402
from triton.core.edition import configuracao_da_edicao  # noqa: E402
from triton.core.parser import export_triton_json, load_precipitation, serie_da_climbra  # noqa: E402

PASTA_EXEMPLOS = os.path.join(RAIZ, "examples", "portugal")
PASTA_CHUVA = os.path.join(RAIZ, "data", "rainfall")

#: A casa do tutorial do manual (``manual/gerar_tabelas.py``, TUTORIAL).
TUTORIAL = {
    "area": 150.0,            # m² de cobertura, projeção horizontal
    "runoff_coeff": 0.85,     # telha cerâmica
    "discard_mm": 2.0,
    "discard_mode": 1,        # todo o evento de chuva
    "moradores": 4,
    "per_capita": 150.0,      # L/hab·dia
    "rainwater_share": 0.28,  # autoclismos e usos exteriores
}

AVISO_DE_CUSTOS = ("Os custos de obra, de bomba e de manutenção não estão definidos: introduza os seus "
                   "(etapa 5). Até lá, a análise mostra apenas a poupança na fatura.")

#: Eletricidade da Madeira: Tarifa Base da EEM, 6,90 kVA. A fonte é um comparador (secundária).
ELETRICIDADE_FUNCHAL = {
    "preco_kwh": 0.1673,
    "potencia_dia": 0.3386,
    "fonte": ("Comparador luzegas.pt, «Tarifas da eletricidade da Madeira», Tarifa Base da EEM "
              "(Empresa de Eletricidade da Madeira), 6,90 kVA, sem IVA, atualizada em 20/02/2025. "
              "FONTE SECUNDÁRIA (não é o tarifário da entidade)."),
}


def virg(x: float) -> str:
    """Número com vírgula decimal e quatro casas (0,1673)."""
    return f"{x:.4f}".replace(".", ",")


def _lisboa():
    return dict(
        pasta="lisboa", arquivo="lisboa.triton", concelho="Lisboa", serie=None,
        nome="Exemplo - moradia do tutorial em Lisboa (E-OBS 1991-2020) [custos a informar pelo utilizador]",
        eletricidade=None)


def _porto():
    return dict(
        pasta="porto", arquivo="porto.triton", concelho="Porto", serie=None,
        nome="Exemplo - moradia do tutorial no Porto (E-OBS 1991-2020) [custos a informar pelo utilizador]",
        eletricidade=None)


def _funchal():
    return dict(
        pasta="funchal", arquivo="funchal.triton", concelho="Funchal", serie="Funchal.csv",
        nome="Exemplo - moradia do tutorial no Funchal (ERA5 1991-2020) [custos a informar pelo utilizador]",
        eletricidade=ELETRICIDADE_FUNCHAL)


CIDADES = (_lisboa, _porto, _funchal)


def projeto(c: dict):
    """A configuração, a série de chuva, o estado da interface e as notas de uma cidade."""
    cfg = configuracao_da_edicao()
    t = TUTORIAL
    cfg.project_name = c["nome"]
    cfg.area = t["area"]
    cfg.runoff_coeff = t["runoff_coeff"]
    cfg.discard = t["discard_mm"]
    cfg.discard_mode = t["discard_mode"]
    cfg.residents_count = t["moradores"]
    cfg.demand_value = t["per_capita"]
    cfg.rainwater_share = t["rainwater_share"]
    cfg.first_flush_system_enabled = True
    # Varredura de volumes, como no capítulo do tutorial: a curva é o que se mostra.
    cfg.lower_tank_mode = 1
    cfg.lower_tank_max = 20000.0
    cfg.lower_tank_step = 1000.0
    cfg.delta_ideal = 1.0
    cfg.supply_arrangement = "pressurizacao"
    cfg.pressurizer_model = "personalizado"   # sem marca: o utilizador introduz os dados do sobrepressor
    cfg.upper_tank_used = 0
    cfg.upper_tank_vol = 0.0
    cfg.pump_count = 1
    cfg.start_date = pt.INICIO_PADRAO
    estado = {"stage3": {"currency_code": "EUR"}}
    if c["serie"] is None:
        # Chuva: referência à base E-OBS.
        cfg.climate_source_mode = "national_db"
        cfg.climate_city_uf, cfg.climate_city_name = pt.distrito_do_concelho(c["concelho"]), c["concelho"]
        cfg.climate_model, cfg.climate_scenario = pt.MODELO_EOBS, pt.CENARIO_EOBS
        cfg.climate_start_date, cfg.climate_end_date = pt.INICIO_PADRAO, pt.FIM_PADRAO
        cfg.precip_file = ""
        estado["project"] = {
            "source_mode": "national_db", "climate_uf": cfg.climate_city_uf,
            "climate_city": c["concelho"], "climate_model": pt.MODELO_EOBS,
            "climate_scenario": pt.CENARIO_EOBS, "start_date": pt.INICIO_PADRAO,
            "end_date": pt.FIM_PADRAO}
        chuva = serie_da_climbra(cfg)
        origem = f"E-OBS v33.0e, concelho de {c['concelho']}, 1991-2020 (data/portugal_eobs.db)."
    else:
        # Chuva: ficheiro da edição (reanálise ERA5), incorporado no projeto.
        cfg.climate_source_mode = "custom_file"
        cfg.climate_city_uf, cfg.climate_city_name = "Madeira", c["concelho"]
        cfg.climate_model, cfg.climate_scenario = "ERA5 (Open-Meteo)", "Reanálise"
        cfg.climate_start_date, cfg.climate_end_date = pt.INICIO_PADRAO, pt.FIM_PADRAO
        cfg.precip_file = c["serie"]
        estado["project"] = {"source_mode": "custom_file", "start_date": pt.INICIO_PADRAO,
                             "end_date": pt.FIM_PADRAO}
        chuva = load_precipitation(os.path.join(PASTA_CHUVA, c["serie"]))
        origem = f"{c['serie']}: Open-Meteo / reanálise ERA5, 1991-2020 (data/rainfall/LEIA.md)."
    # Tarifário transcrito do concelho.
    assert tarifas.aplicar(c["concelho"], cfg), c["concelho"]
    cfg.elec_city_uf, cfg.elec_city_name = cfg.tariff_city_uf, cfg.tariff_city_name
    dados = tarifas.carregar()[c["concelho"]]
    notas = {
        "exemplo": c["nome"],
        "custos": AVISO_DE_CUSTOS,
        "entidades_tarifarias": dados["entidades"],
        "vigencia_tarifaria": dados["vigencia"],
        "fontes_tarifarias": dados["fontes"],
        "hipoteses_tarifarias": dados.get("notas", []),
        "chuva": origem,
    }
    el = c["eletricidade"]
    if el:
        cfg.elec_tariff = el["preco_kwh"]
        cfg.elec_tax_var = 0.0
        cfg.elec_tax_fixed = 0.0
        notas["eletricidade"] = (
            f"{virg(el['preco_kwh'])} €/kWh (Tarifa Base da EEM, sem IVA). {el['fonte']} A potência "
            f"contratada ({virg(el['potencia_dia'])} €/dia a 6,90 kVA) paga-se com ou sem o sistema, "
            "por isso não entra na poupança.")
    else:
        notas["eletricidade"] = ("Tarifa de eletricidade não definida neste exemplo: introduza a sua "
                                 "(o custo de bombagem fica a zero até lá).")
    cfg.data_base_estudo = "15/10/2026"
    cfg.created_at = "15/10/2026 00:00"
    return cfg, chuva, estado, notas


def _curto(caminho: str) -> str:
    """O caminho relativo à raiz, ou o absoluto se estiver noutra unidade (pasta temporária)."""
    try:
        return os.path.relpath(caminho, RAIZ)
    except ValueError:
        return caminho


def gerar(destino: str = PASTA_EXEMPLOS):
    os.makedirs(destino, exist_ok=True)
    feitos = []
    for fabrica in CIDADES:
        c = fabrica()
        cfg, chuva, estado, notas = projeto(c)
        caminho = os.path.join(destino, c["arquivo"])
        export_triton_json(cfg, caminho, precip_data=chuva, ui_state=estado, analysis=notas)
        print(f"{_curto(caminho)}: {len(chuva)} dias, {chuva.sum() / 30:.0f} mm/ano")
        feitos.append(caminho)
    return feitos


if __name__ == "__main__":
    gerar()
