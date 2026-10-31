# -*- coding: utf-8 -*-
"""Gera os projetos de exemplo da Edição Ibérica: Lisboa, Porto e Funchal (Portugal), Madrid e Palma (Espanha).

A edificação é a do tutorial do manual (150 m² de telhado, quatro residentes, 150 L/hab·dia,
28% não potável), igual em todas as cidades, para que os resultados se comparem. Muda o local:

- chuva: **Iberia01 v1.0 (ODbL, uso comercial permitido)**, normal 1986-2015, por município e pelo código
  (``Nome [código]``, decisão 9 de ``auditoria/iberia/DECISOES_ASSUMIDAS.md``). Lisboa, Porto, Madrid e Palma
  vêm do Iberia01; o **Funchal** vem da reanálise **ERA5** de 0,25° (CC BY 4.0, ``data/chuva_ilhas_era5.db``),
  nível de qualidade C, com aviso (o Funchal está fora do domínio do Iberia01). O ficheiro guarda a referência
  da série (município, fonte, recorte e SHA-256) e o programa recompõe-na da base ao abrir;
- tarifário: Portugal, o transcrito em ``triton/data/portugal_tarifarios.json`` (Lisboa: EPAL e Câmara; Porto:
  Águas e Energia do Porto; Funchal: Câmara Municipal), com vigência e fontes. Espanha, o de
  ``triton/data/espanha_tarifarios.json``: **Madrid** com a tarifa do Canal de Isabel II (camada 1, transcrita
  e **ainda não conferida**: segunda leitura pendente) e **Palma** com a média regional do INE (camada 3, só
  indicativa, um preço total por m³);
- eletricidade: só no Funchal, a Tarifa Base da EEM (0,1673 €/kWh, sem IVA), fonte secundária;
- custos de obra, bomba e manutenção: **não** se inventam; ficam a zero, e o projeto diz-o.
  O utilizador introduz os seus (etapa 5); sem eles a análise mostra só a poupança na fatura.

    python scripts/gerar_exemplos_prt.py            # os cinco
    python scripts/gerar_exemplos_prt.py lisboa     # só os indicados

Os exemplos de Portugal ficam em ``examples/portugal/`` e os de Espanha em ``examples/espanha/``. Os números do
tutorial estão copiados abaixo (não depende do manual-fonte).
"""

from __future__ import annotations

import os
import sys

os.environ["TRITON_EDITION"] = "IBE"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from triton.core import base_climatica_iberica as ib  # noqa: E402
from triton.core import tarifarios_espanha as tarifas_es  # noqa: E402
from triton.core import tarifarios_portugal as tarifas  # noqa: E402
from triton.core.edition import configuracao_da_edicao  # noqa: E402
from triton.core.parser import export_triton_json, serie_da_climbra  # noqa: E402

PASTA_EXEMPLOS = os.path.join(RAIZ, "examples", "portugal")
PASTA_EXEMPLOS_ES = os.path.join(RAIZ, "examples", "espanha")

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


def _caso(pasta, codigo, nome, concelho, eletricidade=None, pais="PT", obs=""):
    return dict(pasta=pasta, arquivo=f"{pasta}.triton", codigo=codigo, concelho=concelho, pais=pais,
                nome=nome, eletricidade=eletricidade, obs=obs)


def _lisboa():
    return _caso("lisboa", "PT-1106", "Exemplo - moradia do tutorial em Lisboa (Iberia01 1986-2015) "
                 "[custos a informar pelo utilizador]", "Lisboa")


def _porto():
    return _caso("porto", "PT-1312", "Exemplo - moradia do tutorial no Porto (Iberia01 1986-2015) "
                 "[custos a informar pelo utilizador]", "Porto")


def _funchal():
    return _caso("funchal", "PT-3103", "Exemplo - moradia do tutorial no Funchal (ERA5 1986-2015, nível C) "
                 "[custos a informar pelo utilizador]", "Funchal", ELETRICIDADE_FUNCHAL)


def _madrid():
    return _caso("madrid", "ES-28079", "Exemplo - moradia do tutorial em Madrid (Iberia01 1986-2015) "
                 "[custos a informar pelo utilizador]", "Madrid", pais="ES",
                 obs=("Tarifa de Madrid: transcrita do Canal de Isabel II (camada 1), AINDA NÃO CONFERIDA (segunda "
                      "leitura pendente); confirme-a numa fatura."))


def _palma():
    return _caso("palma", "ES-07040", "Exemplo - moradia do tutorial em Palma (Baleares, Iberia01 1986-2015) "
                 "[custos a informar pelo utilizador]", "Palma", pais="ES",
                 obs=("Tarifa de Palma: apenas a média regional do INE para as Baleares (camada 3), um preço total "
                      "por m³ e sem parte fixa; é indicativa, não é a tarifa da entidade gestora. Introduza a da sua fatura."))


CIDADES = (_lisboa, _porto, _funchal)
CIDADES_ES = (_madrid, _palma)


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
    cfg.start_date = ib.INICIO_PADRAO
    estado = {"stage3": {"currency_code": "EUR"}}
    # Chuva: referência ao Iberia01 (ou à ERA5 das ilhas) pelo código do município.
    u = ib.unidade(c["codigo"])
    cfg.climate_source_mode = "national_db"
    cfg.climate_city_uf = f"{u['pais']}|{u['regiao']}"
    cfg.climate_city_name = ib.rotulo(u)
    cfg.climate_model, cfg.climate_scenario = ib.MODELO_IBERIA01, ib.CENARIO_IBERIA01
    cfg.climate_start_date, cfg.climate_end_date = ib.INICIO_PADRAO, ib.FIM_PADRAO
    cfg.precip_file = ""
    estado["project"] = {
        "source_mode": "national_db", "climate_uf": cfg.climate_city_uf, "climate_city": cfg.climate_city_name,
        "climate_model": cfg.climate_model, "climate_scenario": cfg.climate_scenario,
        "start_date": ib.INICIO_PADRAO, "end_date": ib.FIM_PADRAO}
    chuva = serie_da_climbra(cfg)
    if ib.fonte_da_unidade(c["codigo"]) == "era5":
        origem = (f"{c['concelho']} [{c['codigo']}]: reanálise ERA5 de 0,25° (Copernicus / Open-Meteo, CC BY 4.0), "
                  f"1986-2015, nó mais próximo do município (data/chuva_ilhas_era5.db). Nível de qualidade C: "
                  f"fora do domínio do Iberia01 e sem validação local; para um projeto real, use a série da estação.")
    else:
        origem = (f"{c['concelho']} [{c['codigo']}]: Iberia01 v1.0 (ODbL 1.0), 1986-2015, nível de qualidade "
                  f"{u['nivel']} (data/chuva_iberia01_p*.db). " + ib.CITACAO)
    # Tarifário transcrito do município.
    if c["pais"] == "PT":
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
    else:
        assert tarifas_es.aplicar(c["codigo"], cfg), c["codigo"]
        cfg.elec_city_uf, cfg.elec_city_name = cfg.tariff_city_uf, cfg.tariff_city_name
        camada = tarifas_es.camada(c["codigo"])
        notas = {
            "exemplo": c["nome"],
            "custos": AVISO_DE_CUSTOS,
            "entidades_tarifarias": ("Canal de Isabel II" if camada == 1 else "média regional do INE (Illes Balears)"),
            "vigencia_tarifaria": cfg.tariff_vigencia,
            "fontes_tarifarias": [tarifas_es.procedencia(c["codigo"])],
            "hipoteses_tarifarias": [c["obs"], tarifas_es.aviso(c["codigo"])],
            "chuva": origem,
            "camada_tarifaria": camada,
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


def gerar(destino: str = PASTA_EXEMPLOS, destino_es: str = PASTA_EXEMPLOS_ES, so=None):
    feitos = []
    for fabrica in CIDADES + CIDADES_ES:
        c = fabrica()
        if so and c["pasta"] not in so:
            continue
        pasta = destino if c["pais"] == "PT" else destino_es
        os.makedirs(pasta, exist_ok=True)
        cfg, chuva, estado, notas = projeto(c)
        caminho = os.path.join(pasta, c["arquivo"])
        export_triton_json(cfg, caminho, precip_data=chuva, ui_state=estado, analysis=notas)
        print(f"{_curto(caminho)}: {len(chuva)} dias, {chuva.sum() / 30:.0f} mm/ano")
        feitos.append(caminho)
    return feitos


if __name__ == "__main__":
    gerar(so=[a for a in sys.argv[1:] if not a.startswith("-")] or None)
