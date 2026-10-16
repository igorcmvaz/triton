# -*- coding: utf-8 -*-
"""Tabelas e figuras do capítulo «Modulação probabilística», calculadas pelo programa.

Roda a ferramenta 13 no projeto do tutorial — o mesmo núcleo da interface e do comando
`triton probabilistic-study` — e grava:

- `partes/_tabelas/cap40_catalogo.md`: o catálogo de variáveis, lido do código, com a
  distribuição de triagem de cada uma;
- `partes/_tabelas/cap43_*.md`: as tabelas do exemplo (entradas sorteadas, resultados no
  volume escolhido, frequência de escolha, sensibilidade);
- `figuras/fig52…fig55`: as figuras do exemplo, desenhadas pelas mesmas classes da tela;
- `partes/_tabelas/cap43_modulacao.json`: o resultado inteiro, para os testes conferirem.

O manual em inglês traduz as tabelas (`manual/en/traduzir_tabelas.py`) e usa as mesmas
figuras. Com o mesmo projeto, a mesma semente e o mesmo número de realizações, os números
se repetem exatamente.

    python manual/gerar_modulacao.py
"""

from __future__ import annotations

import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

from triton.cli import _get_precipitation, _load_bundle  # noqa: E402
from triton.core import modulacao_estocastica as M  # noqa: E402

#: Os dois exemplos do capítulo são arquivos de caso (`manual/gerar_casos.py`), com a
#: modulação gravada: o leitor abre o mesmo arquivo e reproduz as tabelas.
CASO = os.path.join(AQUI, "casos", "10_modulacao_tutorial.triton")
CASO_CLIMBRA = os.path.join(AQUI, "casos", "11_modulacao_climbra.triton")
TABELAS = os.path.join(AQUI, "partes", "_tabelas")
FIGURAS = os.path.join(AQUI, "figuras")
NL = chr(10)
#: O exemplo do capítulo: as três de consumo, a chuva, a tarifa e o investimento.
VARIAVEIS_DO_EXEMPLO = ("per_capita_l_dia", "pessoas", "fracao_nao_potavel_pct", "fator_chuva", "fator_tarifa",
                        "fator_investimento")
REALIZACOES, SEMENTE = 1000, 42
#: O segundo exemplo: o mesmo projeto com a chuva da base CLIMBra, cenário SSP2-4.5, trinta
#: anos à frente, os 19 modelos sorteados junto com as três variáveis de consumo.
CIDADE_DO_EXEMPLO, CENARIO_DO_EXEMPLO = "Florianópolis", "SSP245"
INICIO_DO_EXEMPLO, FIM_DO_EXEMPLO = "01/01/2025", "31/12/2054"


def br(v, casas=1):
    if v is None:
        return "—"
    texto = f"{float(v):,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def _triagem(chave: str) -> str:
    """A distribuição de triagem dita em palavras, relativa ao valor do projeto."""
    return {
        "per_capita_l_dia": "lognormal, média do projeto, CV de 20%",
        "pessoas": "normal, média do projeto, desvio de 1 pessoa; inteiro de 1 ao dobro",
        "fracao_nao_potavel_pct": "normal, média do projeto, desvio de 5 pontos; 0 a 100%",
        "demanda_externa_l_dia": "normal, média do projeto, CV de 30%",
        "area_m2": "normal, média do projeto, CV de 5%",
        "coef_escoamento": "triangular, do projeto −0,10 ao projeto +0,05; 0 a 1",
        "descarte_mm": "uniforme, do projeto −1 mm ao projeto +1 mm",
        "fator_chuva": "normal, média 1, desvio de 0,10",
        "fator_tarifa": "normal, média 1, desvio de 0,10",
        "fator_esgoto": "normal, média 1, desvio de 0,10",
        "reajuste_tarifa_pct": "normal, média do projeto, desvio de 2 pontos",
        "tarifa_energia": "normal, média do projeto, CV de 10%",
        "reajuste_energia_pct": "normal, média do projeto, desvio de 2 pontos",
        "fator_investimento": "lognormal, média 1, desvio de 0,15",
        "fator_cisterna": "lognormal, média 1, desvio de 0,15",
        "fator_om": "lognormal, média 1, desvio de 0,25",
        "inflacao_om_pct_mes": "normal, média do projeto, desvio de 0,10 ponto",
        "tma_pct_mes": "normal, média do projeto, desvio de 0,25 ponto",
        "periodo_analise_anos": "triangular, do projeto −5 ao projeto +5 anos; inteiro, ao menos 1",
        "fator_emissao_agua": "normal, média 1, desvio de 0,20",
        "fator_emissao_rede": "normal, média 1, desvio de 0,20",
    }[chave]


def tabela_catalogo() -> str:
    linhas = ["<!-- tabela: As variáveis que a modulação probabilística pode sortear, com a distribuição de triagem "
              "que a tela propõe -->",
              "| Grupo | Variável | Unidade | Distribuição de triagem | Marcada ao abrir |",
              "| :--- | :--- | :--- | :--- | :--- |"]
    for v in M.CATALOGO.values():
        linhas.append(f"| {v.grupo} | {v.rotulo} | {v.unidade} | {_triagem(v.chave)} | "
                      f"{'sim' if v.padrao else 'não'} |")
    return NL.join(linhas)


def _rotulo(chave):
    v = M.CATALOGO[chave]
    return f"{v.rotulo} ({v.unidade})"


def _casas(chave):
    return 2 if M.CATALOGO[chave].unidade in ("×", "—") else M.CATALOGO[chave].casas


def _distribuicao(d, casas):
    tipo = d["tipo"]
    if tipo in ("normal", "lognormal"):
        return f"{tipo} ({br(d['media'], casas)}; {br(d['desvio'], casas)})"
    if tipo == "triangular":
        return f"{tipo} ({br(d['minimo'], casas)}; {br(d['moda'], casas)}; {br(d['maximo'], casas)})"
    return f"{tipo} ({br(d['minimo'], casas)}; {br(d['maximo'], casas)})"


def tabelas_do_exemplo(cfg, r) -> dict:
    ent = ["<!-- tabela: As variáveis sorteadas no exemplo do tutorial: distribuição declarada e estatísticas das "
           "realizações -->",
           "| Variável | No estudo | Distribuição | Média | Desvio-padrão | P5 | P95 |",
           "| :--- | ---: | :--- | ---: | ---: | ---: | ---: |"]
    for k in r["variaveis_ativas"]:
        c = _casas(k)
        e = r["entradas"][k]
        m = max(c, 1)  # média e desvio de um inteiro (pessoas) pedem uma casa
        ent.append(f"| {_rotulo(k)} | {br(M.valor_do_projeto(cfg, k), c)} | "
                   f"{_distribuicao(r['parametros']['variaveis'][k], c)} | {br(e['media'], m)} | "
                   f"{br(e['desvio'], m)} | {br(e['p5'], c)} | {br(e['p95'], c)} |")

    ref = r["referencia"]
    res = ["<!-- tabela: Resultados no volume escolhido pelo estudo do tutorial: estudo determinístico e estatísticas "
           "das realizações -->",
           "| Grandeza | Estudo determinístico | Média | Desvio-padrão | CV (%) | P5 | P50 | P95 |",
           "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for c, rot, casas in (("potencial_pct", "Economia de água potável (%)", 1), ("vpl_brl", "VPL (R$)", 0),
                          ("payback_anos", "Payback descontado (anos)", 1),
                          ("co2_kg", "Saldo de CO₂ no ciclo de vida (kg)", 0)):
        e = ref[c]
        res.append(f"| {rot} | {br(ref['base'][c], casas)} | {br(e['media'], casas)} | {br(e['desvio'], casas)} | "
                   f"{br(e['cv_pct'], 1)} | {br(e['p5'], casas)} | {br(e['p50'], casas)} | {br(e['p95'], casas)} |")
    pv, pc = ref["prob_vpl_positivo"], ref["prob_co2_positivo"]
    pr = ["<!-- tabela: Probabilidades no volume escolhido, com o intervalo de confiança de 95% de Wilson -->",
          "| Evento | Probabilidade (%) | IC 95%, limite inferior (%) | IC 95%, limite superior (%) |",
          "| :--- | ---: | ---: | ---: |",
          f"| o investimento se paga (VPL > 0) | {br(pv['pct'], 1)} | {br(pv['ic95_inf'], 1)} | {br(pv['ic95_sup'], 1)} |",
          f"| o saldo de CO₂ no ciclo de vida é positivo | {br(pc['pct'], 1)} | {br(pc['ic95_inf'], 1)} | "
          f"{br(pc['ic95_sup'], 1)} |"]

    freq = r["frequencia_pct"]
    rotulos = sorted({k for c in freq.values() for k in c},
                     key=lambda k: (k == "nenhum", float(k) if k != "nenhum" else 0.0))
    fr = ["<!-- tabela: Frequência com que cada volume é escolhido nas realizações do exemplo, por critério (%) -->",
          "| Volume (m³) | Ideal técnico | Ótimo econômico (payback) | Vencedor TOPSIS |",
          "| :--- | ---: | ---: | ---: |"]
    for k in rotulos:
        nome = "nenhum se paga" if k == "nenhum" else br(float(k) / 1000.0, 1 if float(k) % 1000 else 0)
        fr.append(f"| {nome} | {br(freq['ideal_tecnico'].get(k, 0.0), 0)} | "
                  f"{br(freq['otimo_economico'].get(k, 0.0), 0)} | {br(freq['vencedor_topsis'].get(k, 0.0), 0)} |")

    sens = r["sensibilidade_spearman"]
    ordem = sorted(sens, key=lambda n: -abs(sens[n]["vpl_brl"] or 0.0))
    se = ["<!-- tabela: Sensibilidade no volume escolhido: força e sentido da influência de cada variável sorteada "
          "sobre os resultados do tutorial -->",
          "| Variável | ρ com a economia | ρ com o VPL | ρ com o saldo de CO₂ |",
          "| :--- | ---: | ---: | ---: |"]
    for n in ordem:
        s = sens[n]
        se.append(f"| {M.CATALOGO[n].rotulo} | {br(s['potencial_pct'], 2)} | {br(s['vpl_brl'], 2)} | "
                  f"{br(s['co2_kg'], 2)} |")
    return {"cap43_entradas.md": NL.join(ent), "cap43_referencia.md": NL.join(res),
            "cap43_probabilidades.md": NL.join(pr),
            "cap43_frequencia.md": NL.join(fr), "cap43_sensibilidade.md": NL.join(se),
            "cap43_variancia.md": tabela_de_variancia(
                r, "Parte da variância do resultado explicada por cada variável sorteada no exemplo do tutorial, "
                   "no volume escolhido (η²; as variáveis contínuas agrupadas em decis)")}


def tabela_de_variancia(r, legenda: str) -> str:
    """η² de cada fonte de incerteza, da maior para a menor parte da variância do VPL, e a soma."""
    ve = r["variancia_explicada_eta2"]
    ordem = sorted(ve, key=lambda k: -(ve[k]["vpl_brl"] or 0.0))
    linhas = [f"<!-- tabela: {legenda} -->",
              "| Fonte de incerteza | η² da economia | η² do VPL | η² do saldo de CO₂ |",
              "| :--- | ---: | ---: | ---: |"]
    for n in ordem:
        nome = "Modelo climático" if n == "modelo_climatico" else M.CATALOGO[n].rotulo
        linhas.append(f"| {nome} | {br(ve[n]['potencial_pct'], 2)} | {br(ve[n]['vpl_brl'], 2)} | "
                      f"{br(ve[n]['co2_kg'], 2)} |")
    soma = [br(sum(ve[n][c] or 0.0 for n in ordem), 2) for c in ("potencial_pct", "vpl_brl", "co2_kg")]
    linhas.append(f"| Soma | {soma[0]} | {soma[1]} | {soma[2]} |")
    return NL.join(linhas)


def _modulacao_gravada(bundle):
    """As distribuições, os modelos, o N e a semente gravados no arquivo de caso."""
    estado = (bundle.get("ui_state") or {})["modulacao_estocastica"]
    return M.ParametrosIncertos.de_dict(estado["parametros"]), int(estado["amostras"]), int(estado["semente"])


def exemplo_dos_modelos():
    """O tutorial com a chuva da CLIMBra: o consumo e o modelo climático sorteados juntos."""
    bundle = _load_bundle(CASO_CLIMBRA)
    cfg = bundle["config"]
    par, n, semente = _modulacao_gravada(bundle)
    series = M.series_dos_modelos_climaticos(cfg, par.modelos_climaticos)
    analise = bundle.get("analysis") or {}
    r = M.simular(cfg, _get_precipitation(bundle), par, amostras=n, semente=semente,
                  pesos=analise.get("topsis_weights"), ambiental=analise.get("environmental"),
                  series_dos_modelos=series)
    anos = {m: len(s) / 365.25 for m, s in series.items()}
    linhas = [f"<!-- tabela: Resultados no volume escolhido ({br(r['volume_de_referencia_l'] / 1000.0, 0)} m³) "
              f"por modelo climático sorteado, em {CIDADE_DO_EXEMPLO} no cenário SSP2-4.5 de 2025 a 2054, com as três "
              f"variáveis de consumo também sorteadas -->",
              "| Modelo | Realizações | Chuva média (mm/ano) | Economia média (%) | VPL médio (R$) | P(VPL > 0) (%) |",
              "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    for m in sorted(r["por_modelo"], key=lambda x: -float(series[x["modelo"]].sum()) / anos[x["modelo"]]):
        pv = m["prob_vpl_positivo"] or {}
        linhas.append(f"| {m['modelo']} | {m['realizacoes']} | {br(series[m['modelo']].sum() / anos[m['modelo']], 0)} | "
                      f"{br(m['potencial_pct']['media'], 1)} | {br(m['vpl_brl']['media'], 0)} | "
                      f"{br(pv.get('pct'), 0)} |")
    return r, {"cap43_modelos.md": NL.join(linhas), "cap43_modelos_variancia.md": tabela_de_variancia(
        r, "Parte da variância do resultado explicada por cada fonte de incerteza no exemplo dos modelos "
           "climáticos, no volume escolhido (η²; as variáveis contínuas agrupadas em decis)")}


def figuras(r):
    """As figuras do exemplo, pelas mesmas classes da tela (sem título interno)."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    QApplication.instance() or QApplication(sys.argv)
    from triton.ui import tab_modulacao_estocastica as T
    graficos = {
        "fig52_modulacao_economia.png": T._GraficoLeque("x", "potencial_pct", "Economia de água potável (%)", 1),
        "fig53_modulacao_vpl.png": T._GraficoLeque("x", "vpl_brl", "VPL (R$)", 0),
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


def main():
    bundle = _load_bundle(CASO)
    cfg = bundle["config"]
    precip = _get_precipitation(bundle)
    par, n, semente = _modulacao_gravada(bundle)
    analise = bundle.get("analysis") or {}
    r = M.simular(cfg, precip, par, amostras=n, semente=semente,
                  pesos=analise.get("topsis_weights"), ambiental=analise.get("environmental"))
    os.makedirs(TABELAS, exist_ok=True)
    r_modelos, tabelas_modelos = exemplo_dos_modelos()
    arquivos = {"cap40_catalogo.md": tabela_catalogo(), **tabelas_do_exemplo(cfg, r), **tabelas_modelos}
    for nome, conteudo in arquivos.items():
        with open(os.path.join(TABELAS, nome), "w", encoding="utf-8", newline="\n") as f:
            f.write(conteudo + NL)
        print(f"  partes/_tabelas/{nome}")
    with open(os.path.join(TABELAS, "cap43_modulacao.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({k: v for k, v in r.items() if k != "amostras"}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(TABELAS, "cap43_modelos.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({k: v for k, v in r_modelos.items() if k != "amostras"}, f, ensure_ascii=False, indent=1)
    figuras(r)
    return r


if __name__ == "__main__":
    print("modulação probabilística:")
    main()
