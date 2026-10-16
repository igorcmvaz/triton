# -*- coding: utf-8 -*-
"""Tabelas e figuras do capítulo «Modulação probabilística» da Edição Internacional, calculadas pelo programa.

Roda a ferramenta 12 (modulação probabilística) nos dois casos de ``manual/gerar_casos.py``, que o leitor
pode abrir e reproduzir:

- ``casos/09_modulation_tutorial.triton``: o tutorial de Nova York com as três variáveis de consumo, a chuva,
  a tarifa e o investimento sorteados (mil realizações, semente 42);
- ``casos/10_modulation_catchment.triton``: o mesmo projeto com a incerteza sobre a captação (área,
  escoamento, descarte), a chuva, a tarifa e o investimento.

Grava, em inglês e no formato inglês (milhar com vírgula, ponto decimal), em ``en/partes/_tabelas`` e, igual,
em ``partes/_tabelas`` (o rastro da edição Brasil, que a INT não lê):

- ``cap40_catalogo.md``: o catálogo de variáveis, lido do código, com a distribuição de triagem de cada uma;
- ``cap43_*.md``: as tabelas do exemplo do tutorial (entradas sorteadas, resultados no volume escolhido,
  probabilidades, frequência de escolha, sensibilidade, variância) e, do exemplo da captação,
  ``cap43_captacao*.md``;
- ``figuras/fig52…fig55``: as figuras do exemplo do tutorial, desenhadas pelas mesmas classes da tela;
- ``partes/_tabelas/cap43_modulacao.json`` e ``cap43_captacao.json``: os resultados inteiros, para os testes.

Os valores em dinheiro são US$ ilustrativos (a edição não traz preços de obra: ``manual/gerar_tabelas.py``).
Com o mesmo projeto, a mesma semente e o mesmo número de realizações, os números se repetem exatamente.

    python manual/gerar_modulacao.py
"""

from __future__ import annotations

import os
os.environ["TRITON_EDITION"] = "INT"

import json
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

from triton.cli import _get_precipitation, _load_bundle  # noqa: E402
from triton.core import modulacao_estocastica as M  # noqa: E402

#: Os dois exemplos do capítulo são arquivos de caso (`manual/gerar_casos.py`), com a modulação gravada:
#: o leitor abre o mesmo arquivo e reproduz as tabelas.
CASO = os.path.join(AQUI, "casos", "09_modulation_tutorial.triton")
CASO_CAPTACAO = os.path.join(AQUI, "casos", "10_modulation_catchment.triton")
#: A INT lê ``en/partes/_tabelas``; ``partes/_tabelas`` fica igual, como rastro da edição Brasil.
SAIDAS = (os.path.join(AQUI, "en", "partes", "_tabelas"), os.path.join(AQUI, "partes", "_tabelas"))
FIGURAS = os.path.join(AQUI, "figuras")
NL = chr(10)
ILUSTRATIVO = "illustrative, not a market price"

#: Os rótulos do núcleo estão em português; as tabelas e os gráficos do manual em inglês levam estes.
#: Por chave da variável: (grupo, rótulo, unidade).
NOMES = {
    "per_capita_l_dia": ("Demand", "Per capita consumption", "L/person/day"),
    "pessoas": ("Demand", "Number of occupants", "occupants"),
    "fracao_nao_potavel_pct": ("Demand", "Indoor non-potable fraction", "%"),
    "demanda_externa_l_dia": ("Demand", "Outdoor demand", "L/day"),
    "area_m2": ("Catchment", "Catchment area", "m²"),
    "coef_escoamento": ("Catchment", "Runoff coefficient", "—"),
    "descarte_mm": ("Catchment", "First-flush depth", "mm"),
    "fator_chuva": ("Rain", "Rainfall factor", "×"),
    "fator_tarifa": ("Tariffs", "Water and sewerage tariff factor", "×"),
    "fator_esgoto": ("Tariffs", "Sewerage factor", "×"),
    "reajuste_tarifa_pct": ("Tariffs", "Tariff escalation", "% per period"),
    "tarifa_energia": ("Tariffs", "Energy tariff", "currency units/kWh"),
    "reajuste_energia_pct": ("Tariffs", "Electricity escalation", "% per period"),
    "fator_investimento": ("Costs", "Investment factor", "×"),
    "fator_cisterna": ("Costs", "Cistern price factor", "×"),
    "fator_om": ("Costs", "Running cost factor (O&M)", "×"),
    "inflacao_om_pct_mes": ("Costs", "Running cost inflation", "% per month"),
    "tma_pct_mes": ("Cash flow", "Minimum attractive rate of return", "% per month"),
    "periodo_analise_anos": ("Cash flow", "Analysis period", "years"),
    "fator_emissao_agua": ("Environment", "Potable water emission factor", "×"),
    "fator_emissao_rede": ("Environment", "Grid electricity emission factor", "×"),
}


def num(v, casas=1):
    """O número no formato do manual em inglês: vírgula de milhar, ponto decimal, sinal «−»."""
    if v is None:
        return "—"
    return f"{float(v):,.{casas}f}".replace("-", "−")


def _triagem(chave: str) -> str:
    """A distribuição de triagem dita em palavras, relativa ao valor do projeto."""
    return {
        "per_capita_l_dia": "lognormal, project mean, CV of 20%",
        "pessoas": "normal, project mean, deviation of 1 occupant; integer from 1 to double",
        "fracao_nao_potavel_pct": "normal, project mean, deviation of 5 points; 0 to 100%",
        "demanda_externa_l_dia": "normal, project mean, CV of 30%",
        "area_m2": "normal, project mean, CV of 5%",
        "coef_escoamento": "triangular, from project −0.10 to project +0.05; 0 to 1",
        "descarte_mm": "uniform, from project −1 mm to project +1 mm",
        "fator_chuva": "normal, mean 1, deviation of 0.10",
        "fator_tarifa": "normal, mean 1, deviation of 0.10",
        "fator_esgoto": "normal, mean 1, deviation of 0.10",
        "reajuste_tarifa_pct": "normal, project mean, deviation of 2 points",
        "tarifa_energia": "normal, project mean, CV of 10%",
        "reajuste_energia_pct": "normal, project mean, deviation of 2 points",
        "fator_investimento": "lognormal, mean 1, deviation of 0.15",
        "fator_cisterna": "lognormal, mean 1, deviation of 0.15",
        "fator_om": "lognormal, mean 1, deviation of 0.25",
        "inflacao_om_pct_mes": "normal, project mean, deviation of 0.10 point",
        "tma_pct_mes": "normal, project mean, deviation of 0.25 point",
        "periodo_analise_anos": "triangular, from project −5 to project +5 years; integer, at least 1",
        "fator_emissao_agua": "normal, mean 1, deviation of 0.20",
        "fator_emissao_rede": "normal, mean 1, deviation of 0.20",
    }[chave]


def tabela_catalogo() -> str:
    linhas = ["<!-- tabela: The variables that probabilistic modulation can draw, with the screening distribution "
              "the screen proposes -->",
              "| Group | Variable | Unit | Screening distribution | Ticked on opening |",
              "| :--- | :--- | :--- | :--- | :--- |"]
    for v in M.CATALOGO.values():
        grupo, rotulo, unidade = NOMES[v.chave]
        linhas.append(f"| {grupo} | {rotulo} | {unidade} | {_triagem(v.chave)} | {'yes' if v.padrao else 'no'} |")
    return NL.join(linhas)


def _rotulo(chave):
    _, rotulo, unidade = NOMES[chave]
    return f"{rotulo} ({unidade})"


def _casas(chave):
    return 2 if M.CATALOGO[chave].unidade in ("×", "—") else M.CATALOGO[chave].casas


def _distribuicao(d, casas):
    tipo = d["tipo"]
    if tipo in ("normal", "lognormal"):
        return f"{tipo} ({num(d['media'], casas)}; {num(d['desvio'], casas)})"
    if tipo == "triangular":
        return f"{tipo} ({num(d['minimo'], casas)}; {num(d['moda'], casas)}; {num(d['maximo'], casas)})"
    return f"{tipo} ({num(d['minimo'], casas)}; {num(d['maximo'], casas)})"


def tabela_de_entradas(cfg, r, legenda: str) -> str:
    ent = [f"<!-- tabela: {legenda} -->",
           "| Variable | In the study | Distribution | Mean | Standard deviation | P5 | P95 |",
           "| :--- | ---: | :--- | ---: | ---: | ---: | ---: |"]
    for k in r["variaveis_ativas"]:
        c = _casas(k)
        e = r["entradas"][k]
        m = max(c, 1)  # média e desvio de um inteiro (pessoas) pedem uma casa
        ent.append(f"| {_rotulo(k)} | {num(M.valor_do_projeto(cfg, k), c)} | "
                   f"{_distribuicao(r['parametros']['variaveis'][k], c)} | {num(e['media'], m)} | "
                   f"{num(e['desvio'], m)} | {num(e['p5'], c)} | {num(e['p95'], c)} |")
    return NL.join(ent)


def tabela_de_referencia(r, legenda: str) -> str:
    ref = r["referencia"]
    res = [f"<!-- tabela: {legenda} -->",
           "| Quantity | Deterministic study | Mean | Standard deviation | CV (%) | P5 | P50 | P95 |",
           "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for c, rot, casas in (("potencial_pct", "Potable water savings (%)", 1),
                          ("vpl_brl", f"NPV (US$, {ILUSTRATIVO})", 0),
                          ("payback_anos", "Discounted payback (years)", 1),
                          ("co2_kg", "Life-cycle CO₂ balance (kg)", 0)):
        e = ref[c]
        res.append(f"| {rot} | {num(ref['base'][c], casas)} | {num(e['media'], casas)} | "
                   f"{num(e['desvio'], casas)} | {num(e['cv_pct'], 1)} | {num(e['p5'], casas)} | "
                   f"{num(e['p50'], casas)} | {num(e['p95'], casas)} |")
    return NL.join(res)


def tabelas_do_exemplo(cfg, r) -> dict:
    ent = tabela_de_entradas(
        cfg, r, "The variables drawn in the tutorial example: declared distribution and statistics of the "
                "realisations")
    res = tabela_de_referencia(
        r, "Results at the volume chosen by the tutorial study: deterministic study and statistics of the "
           "realisations (money in US$, illustrative, not a market price)")
    ref = r["referencia"]
    pv, pc = ref["prob_vpl_positivo"], ref["prob_co2_positivo"]
    pr = ["<!-- tabela: Probabilities at the chosen volume, with the Wilson 95% confidence interval -->",
          "| Event | Probability (%) | 95% CI, lower bound (%) | 95% CI, upper bound (%) |",
          "| :--- | ---: | ---: | ---: |",
          f"| the investment pays back (NPV > 0) | {num(pv['pct'], 1)} | {num(pv['ic95_inf'], 1)} | "
          f"{num(pv['ic95_sup'], 1)} |",
          f"| the life-cycle CO₂ balance is positive | {num(pc['pct'], 1)} | {num(pc['ic95_inf'], 1)} | "
          f"{num(pc['ic95_sup'], 1)} |"]

    freq = r["frequencia_pct"]
    rotulos = sorted({k for c in freq.values() for k in c},
                     key=lambda k: (k == "nenhum", float(k) if k != "nenhum" else 0.0))
    fr = ["<!-- tabela: Frequency with which each volume is chosen in the realisations of the example, by "
          "criterion (%) -->",
          "| Volume (m³) | Technical ideal | Economic optimum (payback) | TOPSIS winner |",
          "| :--- | ---: | ---: | ---: |"]
    for k in rotulos:
        nome = "none pays back" if k == "nenhum" else num(float(k) / 1000.0, 1 if float(k) % 1000 else 0)
        fr.append(f"| {nome} | {num(freq['ideal_tecnico'].get(k, 0.0), 0)} | "
                  f"{num(freq['otimo_economico'].get(k, 0.0), 0)} | "
                  f"{num(freq['vencedor_topsis'].get(k, 0.0), 0)} |")

    sens = r["sensibilidade_spearman"]
    ordem = sorted(sens, key=lambda n: -abs(sens[n]["vpl_brl"] or 0.0))
    se = ["<!-- tabela: Sensitivity at the chosen volume: strength and direction of the influence of each "
          "drawn variable on the tutorial results -->",
          "| Variable | ρ with savings | ρ with NPV | ρ with CO₂ balance |",
          "| :--- | ---: | ---: | ---: |"]
    for n in ordem:
        s = sens[n]
        se.append(f"| {NOMES[n][1]} | {num(s['potencial_pct'], 2)} | {num(s['vpl_brl'], 2)} | "
                  f"{num(s['co2_kg'], 2)} |")
    return {"cap43_entradas.md": ent, "cap43_referencia.md": res,
            "cap43_probabilidades.md": NL.join(pr),
            "cap43_frequencia.md": NL.join(fr), "cap43_sensibilidade.md": NL.join(se),
            "cap43_variancia.md": tabela_de_variancia(
                r, "Share of the variance of the result explained by each drawn variable in the tutorial "
                   "example, at the chosen volume (η²; continuous variables grouped in deciles)")}


def tabelas_da_captacao(cfg, r) -> dict:
    """O exemplo da captação: o que foi sorteado, o resultado no volume escolhido e a variância explicada."""
    return {
        "cap43_captacao_entradas.md": tabela_de_entradas(
            cfg, r, "The variables drawn in the catchment example: declared distribution and statistics of "
                    "the realisations"),
        "cap43_captacao.md": tabela_de_referencia(
            r, "Results at the volume chosen by the study in the catchment example: deterministic study and "
               "statistics of the realisations (money in US$, illustrative, not a market price)"),
        "cap43_captacao_variancia.md": tabela_de_variancia(
            r, "Share of the variance of the result explained by each drawn variable in the catchment "
               "example, at the chosen volume (η²; continuous variables grouped in deciles)"),
    }


def tabela_de_variancia(r, legenda: str) -> str:
    """η² de cada fonte de incerteza, da maior para a menor parte da variância do VPL, e a soma."""
    ve = r["variancia_explicada_eta2"]
    ordem = sorted(ve, key=lambda k: -(ve[k]["vpl_brl"] or 0.0))
    linhas = [f"<!-- tabela: {legenda} -->",
              "| Source of uncertainty | η² of savings | η² of NPV | η² of CO₂ balance |",
              "| :--- | ---: | ---: | ---: |"]
    for n in ordem:
        nome = "Climate model" if n == "modelo_climatico" else NOMES[n][1]
        linhas.append(f"| {nome} | {num(ve[n]['potencial_pct'], 2)} | {num(ve[n]['vpl_brl'], 2)} | "
                      f"{num(ve[n]['co2_kg'], 2)} |")
    soma = [num(sum(ve[n][c] or 0.0 for n in ordem), 2) for c in ("potencial_pct", "vpl_brl", "co2_kg")]
    linhas.append(f"| Sum | {soma[0]} | {soma[1]} | {soma[2]} |")
    return NL.join(linhas)


def _modulacao_gravada(bundle):
    """As distribuições, os modelos, o N e a semente gravados no arquivo de caso."""
    estado = (bundle.get("ui_state") or {})["modulacao_estocastica"]
    return M.ParametrosIncertos.de_dict(estado["parametros"]), int(estado["amostras"]), int(estado["semente"])


def _simular(caminho):
    """Roda a modulação gravada num arquivo de caso: devolve a configuração e o resultado."""
    bundle = _load_bundle(caminho)
    cfg = bundle["config"]
    par, n, semente = _modulacao_gravada(bundle)
    analise = bundle.get("analysis") or {}
    r = M.simular(cfg, _get_precipitation(bundle), par, amostras=n, semente=semente,
                  pesos=analise.get("topsis_weights"), ambiental=analise.get("environmental"))
    return cfg, r


def figuras(r):
    """As figuras do exemplo, pelas mesmas classes da tela (sem título interno)."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    QApplication.instance() or QApplication(sys.argv)
    from triton.ui.translation import set_current_lang
    set_current_lang("en")
    from triton.ui import tab_modulacao_estocastica as T
    graficos = {
        "fig52_modulacao_economia.png": T._GraficoLeque("x", "potencial_pct", "Potable water savings (%)", 1),
        "fig53_modulacao_vpl.png": T._GraficoLeque("x", "vpl_brl", "NPV (US$, illustrative)", 0),
        "fig54_modulacao_frequencia.png": T._GraficoFrequencia("x"),
        "fig55_modulacao_sensibilidade.png": T._GraficoSensibilidade("x"),
    }
    for nome, g in graficos.items():
        g.figure.set_size_inches(8.0, 4.6)
        g.desenhar(r)
        g.figure.set_size_inches(8.0, 4.6)
        g.figure.tight_layout(pad=0.6)
        g.figure.savefig(os.path.join(FIGURAS, nome), dpi=200)
        print(f"  figuras/{nome}")


def _gravar(nome, conteudo, pastas=SAIDAS):
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
        with open(os.path.join(pasta, nome), "w", encoding="utf-8", newline="\n") as f:
            f.write(conteudo + NL)
        print(f"  {os.path.relpath(os.path.join(pasta, nome), AQUI)}")


def _apagar_do_rastro_antigo():
    """Retira as tabelas por modelo climático, que eram do exemplo da base CLIMBra (Brasil)."""
    for pasta in SAIDAS:
        for nome in ("cap43_modelos.md", "cap43_modelos.json", "cap43_modelos_variancia.md"):
            caminho = os.path.join(pasta, nome)
            if os.path.exists(caminho):
                os.remove(caminho)
                print(f"  removido: {os.path.relpath(caminho, AQUI)}")


def main():
    cfg, r = _simular(CASO)
    figuras(r)
    arquivos = {"cap40_catalogo.md": tabela_catalogo(), **tabelas_do_exemplo(cfg, r)}
    cfg_c, r_c = _simular(CASO_CAPTACAO)
    arquivos.update(tabelas_da_captacao(cfg_c, r_c))
    for nome, conteudo in arquivos.items():
        _gravar(nome, conteudo)
    _apagar_do_rastro_antigo()
    # Os resultados inteiros, para os testes conferirem (só no rastro: a INT lê só os .md).
    for nome, res in (("cap43_modulacao.json", r), ("cap43_captacao.json", r_c)):
        with open(os.path.join(SAIDAS[1], nome), "w", encoding="utf-8", newline="\n") as f:
            json.dump({k: v for k, v in res.items() if k != "amostras"}, f, ensure_ascii=False, indent=1)
        print(f"  partes/_tabelas/{nome}")
    return r


if __name__ == "__main__":
    print("modulação probabilística:")
    main()
