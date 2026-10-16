# -*- coding: utf-8 -*-
"""Tabelas e figuras do capítulo «Modulação probabilística» da Edição Portugal, calculadas pelo programa.

Executa a ferramenta 12 (modulação probabilística) nos dois casos de ``manual/gerar_casos.py``, que o leitor
pode abrir e reproduzir:

- ``casos/09_modulacao_tutorial.triton``: o tutorial de Lisboa com as três variáveis de consumo, a chuva,
  a tarifa e o investimento sorteados (mil realizações, semente 42);
- ``casos/10_modulacao_captacao.triton``: o mesmo projeto com a incerteza sobre a captação (área,
  escoamento, descarte), a chuva, a tarifa e o investimento.

Grava em ``partes/_tabelas``:

- ``cap40_catalogo.md``: o catálogo de variáveis, lido do código, com a distribuição de triagem de cada uma;
- ``cap43_*.md``: as tabelas do exemplo do tutorial (entradas sorteadas, resultados no volume escolhido,
  probabilidades, frequência de escolha, sensibilidade, variância) e, do exemplo da captação,
  ``cap43_captacao*.md``;
- ``figuras/fig52…fig55``: as figuras do exemplo do tutorial, desenhadas pelas mesmas classes do ecrã;
- ``partes/_tabelas/cap43_modulacao.json`` e ``cap43_captacao.json``: os resultados inteiros, para os testes.

Os valores em dinheiro são em euros ilustrativos (a edição não traz preços de obra: ``manual/gerar_tabelas.py``).
Com o mesmo projeto, a mesma semente e o mesmo número de realizações, os números repetem-se exatamente.

    python manual/gerar_modulacao.py
"""

from __future__ import annotations

import os
os.environ["TRITON_EDITION"] = "PRT"

import json
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

from triton.cli import _get_precipitation, _load_bundle  # noqa: E402
from triton.core import modulacao_estocastica as M  # noqa: E402
from triton.ui.portugues_de_portugal import para_portugal  # noqa: E402

#: Os dois exemplos do capítulo são ficheiros de caso (`manual/gerar_casos.py`), com a modulação gravada:
#: o leitor abre o mesmo ficheiro e reproduz as tabelas.
CASO = os.path.join(AQUI, "casos", "09_modulacao_tutorial.triton")
CASO_CAPTACAO = os.path.join(AQUI, "casos", "10_modulacao_captacao.triton")
TABELAS = os.path.join(AQUI, "partes", "_tabelas")
FIGURAS = os.path.join(AQUI, "figuras")
NL = chr(10)
NBSP = chr(160)
MENOS = "−"
ILUSTRATIVO = "ilustrativo, não é preço de mercado"

#: Os rótulos do núcleo em português europeu: (grupo, rótulo, unidade).
NOMES = {
    "per_capita_l_dia": ("Procura", "Consumo per capita", "L/hab.dia"),
    "pessoas": ("Procura", "Número de pessoas", "pessoas"),
    "fracao_nao_potavel_pct": ("Procura", "Fração não potável interior", "%"),
    "demanda_externa_l_dia": ("Procura", "Procura exterior", "L/dia"),
    "area_m2": ("Captação", "Área de captação", "m²"),
    "coef_escoamento": ("Captação", "Coeficiente de escoamento", "—"),
    "descarte_mm": ("Captação", "Lâmina de descarte", "mm"),
    "fator_chuva": ("Chuva", "Fator da chuva", "×"),
    "fator_tarifa": ("Tarifas", "Fator das tarifas de água e saneamento", "×"),
    "fator_esgoto": ("Tarifas", "Fator do saneamento", "×"),
    "reajuste_tarifa_pct": ("Tarifas", "Atualização tarifária", "% por período"),
    "tarifa_energia": ("Tarifas", "Tarifa de energia", "€/kWh"),
    "reajuste_energia_pct": ("Tarifas", "Atualização da energia", "% por período"),
    "fator_investimento": ("Custos", "Fator do investimento", "×"),
    "fator_cisterna": ("Custos", "Fator do preço da cisterna", "×"),
    "fator_om": ("Custos", "Fator do custo de exploração (O&M)", "×"),
    "inflacao_om_pct_mes": ("Custos", "Inflação do custo de exploração", "% por mês"),
    "tma_pct_mes": ("Fluxo de caixa", "Taxa de atualização", "% por mês"),
    "periodo_analise_anos": ("Fluxo de caixa", "Período de análise", "anos"),
    "fator_emissao_agua": ("Ambiente", "Fator da emissão da água potável", "×"),
    "fator_emissao_rede": ("Ambiente", "Fator da emissão da rede elétrica", "×"),
}


def br(v, casas=1):
    """Número no padrão português: 1 234,5 (espaço inseparável no milhar, sem «-0»)."""
    if v is None:
        return "—"
    v = round(float(v), casas)
    if v == 0:
        v = 0.0
    texto = f"{abs(v):,.{casas}f}".replace(",", NBSP).replace(".", ",")
    return (MENOS if v < 0 else "") + texto


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
        "periodo_analise_anos": "triangular, do projeto −5 ao projeto +5 anos; inteiro, pelo menos 1",
        "fator_emissao_agua": "normal, média 1, desvio de 0,20",
        "fator_emissao_rede": "normal, média 1, desvio de 0,20",
    }[chave]


def tabela_catalogo() -> str:
    linhas = ["<!-- tabela: As variáveis que a modulação probabilística pode sortear, com a distribuição de triagem "
              "que o ecrã propõe -->",
              "| Grupo | Variável | Unidade | Distribuição de triagem | Marcada ao abrir |",
              "| :--- | :--- | :--- | :--- | :--- |"]
    for v in M.CATALOGO.values():
        grupo, rotulo, unidade = NOMES[v.chave]
        linhas.append(f"| {grupo} | {rotulo} | {unidade} | {_triagem(v.chave)} | "
                      f"{'sim' if v.padrao else 'não'} |")
    return para_portugal(NL.join(linhas))


def _rotulo(chave):
    _, rotulo, unidade = NOMES[chave]
    return f"{rotulo} ({unidade})"


def _casas(chave):
    return 2 if M.CATALOGO[chave].unidade in ("×", "—") else M.CATALOGO[chave].casas


def _distribuicao(d, casas):
    tipo = d["tipo"]
    if tipo in ("normal", "lognormal"):
        return f"{tipo} ({br(d['media'], casas)}; {br(d['desvio'], casas)})"
    if tipo == "triangular":
        return f"{tipo} ({br(d['minimo'], casas)}; {br(d['moda'], casas)}; {br(d['maximo'], casas)})"
    return f"{tipo} ({br(d['minimo'], casas)}; {br(d['maximo'], casas)})"


def tabela_de_entradas(cfg, r, legenda: str) -> str:
    ent = [f"<!-- tabela: {legenda} -->",
           "| Variável | No estudo | Distribuição | Média | Desvio-padrão | P5 | P95 |",
           "| :--- | ---: | :--- | ---: | ---: | ---: | ---: |"]
    for k in r["variaveis_ativas"]:
        c = _casas(k)
        e = r["entradas"][k]
        m = max(c, 1)  # média e desvio de um inteiro (pessoas) pedem uma casa
        ent.append(f"| {_rotulo(k)} | {br(M.valor_do_projeto(cfg, k), c)} | "
                   f"{_distribuicao(r['parametros']['variaveis'][k], c)} | {br(e['media'], m)} | "
                   f"{br(e['desvio'], m)} | {br(e['p5'], c)} | {br(e['p95'], c)} |")
    return para_portugal(NL.join(ent))


def tabela_de_referencia(r, legenda: str) -> str:
    ref = r["referencia"]
    res = [f"<!-- tabela: {legenda} -->",
           "| Grandeza | Estudo determinístico | Média | Desvio-padrão | CV (%) | P5 | P50 | P95 |",
           "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for c, rot, casas in (("potencial_pct", "Poupança de água potável (%)", 1),
                          ("vpl_brl", f"VAL (€, {ILUSTRATIVO})", 0),
                          ("payback_anos", "Período de recuperação descontado (anos)", 1),
                          ("co2_kg", "Saldo de CO₂ no ciclo de vida (kg)", 0)):
        e = ref[c]
        res.append(f"| {rot} | {br(ref['base'][c], casas)} | {br(e['media'], casas)} | {br(e['desvio'], casas)} | "
                   f"{br(e['cv_pct'], 1)} | {br(e['p5'], casas)} | {br(e['p50'], casas)} | {br(e['p95'], casas)} |")
    return para_portugal(NL.join(res))


def tabelas_do_exemplo(cfg, r) -> dict:
    ent = tabela_de_entradas(
        cfg, r, "As variáveis sorteadas no exemplo do tutorial: distribuição declarada e estatísticas das "
                "realizações")
    res = tabela_de_referencia(
        r, "Resultados no volume escolhido pelo estudo do tutorial: estudo determinístico e estatísticas das "
           "realizações (valores em €, ilustrativos, não são preços de mercado)")
    ref = r["referencia"]
    pv, pc = ref["prob_vpl_positivo"], ref["prob_co2_positivo"]
    pr = ["<!-- tabela: Probabilidades no volume escolhido, com o intervalo de confiança de 95% de Wilson -->",
          "| Evento | Probabilidade (%) | IC 95%, limite inferior (%) | IC 95%, limite superior (%) |",
          "| :--- | ---: | ---: | ---: |",
          f"| o investimento recupera-se (VAL > 0) | {br(pv['pct'], 1)} | {br(pv['ic95_inf'], 1)} | {br(pv['ic95_sup'], 1)} |",
          f"| o saldo de CO₂ no ciclo de vida é positivo | {br(pc['pct'], 1)} | {br(pc['ic95_inf'], 1)} | "
          f"{br(pc['ic95_sup'], 1)} |"]

    freq = r["frequencia_pct"]
    rotulos = sorted({k for c in freq.values() for k in c},
                     key=lambda k: (k == "nenhum", float(k) if k != "nenhum" else 0.0))
    fr = ["<!-- tabela: Frequência com que cada volume é escolhido nas realizações do exemplo, por critério (%) -->",
          "| Volume (m³) | Ideal técnico | Ótimo económico (recuperação) | Vencedor TOPSIS |",
          "| :--- | ---: | ---: | ---: |"]
    for k in rotulos:
        nome = "nenhum se paga" if k == "nenhum" else br(float(k) / 1000.0, 1 if float(k) % 1000 else 0)
        fr.append(f"| {nome} | {br(freq['ideal_tecnico'].get(k, 0.0), 0)} | "
                  f"{br(freq['otimo_economico'].get(k, 0.0), 0)} | {br(freq['vencedor_topsis'].get(k, 0.0), 0)} |")

    sens = r["sensibilidade_spearman"]
    ordem = sorted(sens, key=lambda n: -abs(sens[n]["vpl_brl"] or 0.0))
    se = ["<!-- tabela: Sensibilidade no volume escolhido: força e sentido da influência de cada variável sorteada "
          "sobre os resultados do tutorial -->",
          "| Variável | ρ com a poupança | ρ com o VAL | ρ com o saldo de CO₂ |",
          "| :--- | ---: | ---: | ---: |"]
    for n in ordem:
        s = sens[n]
        se.append(f"| {NOMES[n][1]} | {br(s['potencial_pct'], 2)} | {br(s['vpl_brl'], 2)} | "
                  f"{br(s['co2_kg'], 2)} |")
    return {"cap43_entradas.md": ent, "cap43_referencia.md": res,
            "cap43_probabilidades.md": para_portugal(NL.join(pr)),
            "cap43_frequencia.md": para_portugal(NL.join(fr)),
            "cap43_sensibilidade.md": para_portugal(NL.join(se)),
            "cap43_variancia.md": tabela_de_variancia(
                r, "Parte da variância do resultado explicada por cada variável sorteada no exemplo do tutorial, "
                   "no volume escolhido (η²; as variáveis contínuas agrupadas em decis)")}


def tabelas_da_captacao(cfg, r) -> dict:
    """O exemplo da captação: o que foi sorteado, o resultado no volume escolhido e a variância explicada."""
    return {
        "cap43_captacao_entradas.md": tabela_de_entradas(
            cfg, r, "As variáveis sorteadas no exemplo da captação: distribuição declarada e estatísticas das "
                    "realizações"),
        "cap43_captacao.md": tabela_de_referencia(
            r, "Resultados no volume escolhido pelo estudo no exemplo da captação: estudo determinístico e "
               "estatísticas das realizações (valores em €, ilustrativos, não são preços de mercado)"),
        "cap43_captacao_variancia.md": tabela_de_variancia(
            r, "Parte da variância do resultado explicada por cada variável sorteada no exemplo da captação, "
               "no volume escolhido (η²; as variáveis contínuas agrupadas em decis)"),
    }


def tabela_de_variancia(r, legenda: str) -> str:
    """η² de cada fonte de incerteza, da maior para a menor parte da variância do VAL, e a soma."""
    ve = r["variancia_explicada_eta2"]
    ordem = sorted(ve, key=lambda k: -(ve[k]["vpl_brl"] or 0.0))
    linhas = [f"<!-- tabela: {legenda} -->",
              "| Fonte de incerteza | η² da poupança | η² do VAL | η² do saldo de CO₂ |",
              "| :--- | ---: | ---: | ---: |"]
    for n in ordem:
        nome = "Modelo climático" if n == "modelo_climatico" else NOMES[n][1]
        linhas.append(f"| {nome} | {br(ve[n]['potencial_pct'], 2)} | {br(ve[n]['vpl_brl'], 2)} | "
                      f"{br(ve[n]['co2_kg'], 2)} |")
    soma = [br(sum(ve[n][c] or 0.0 for n in ordem), 2) for c in ("potencial_pct", "vpl_brl", "co2_kg")]
    linhas.append(f"| Soma | {soma[0]} | {soma[1]} | {soma[2]} |")
    return para_portugal(NL.join(linhas))


def _modulacao_gravada(bundle):
    """As distribuições, os modelos, o N e a semente gravados no ficheiro de caso."""
    estado = (bundle.get("ui_state") or {})["modulacao_estocastica"]
    return M.ParametrosIncertos.de_dict(estado["parametros"]), int(estado["amostras"]), int(estado["semente"])


def _simular(caminho):
    """Executa a modulação gravada num ficheiro de caso: devolve a configuração e o resultado."""
    bundle = _load_bundle(caminho)
    cfg = bundle["config"]
    par, n, semente = _modulacao_gravada(bundle)
    analise = bundle.get("analysis") or {}
    r = M.simular(cfg, _get_precipitation(bundle), par, amostras=n, semente=semente,
                  pesos=analise.get("topsis_weights"), ambiental=analise.get("environmental"))
    return cfg, r


def figuras(r):
    """As figuras do exemplo, pelas mesmas classes do ecrã (sem título interno)."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    QApplication.instance() or QApplication(sys.argv)
    from triton.ui.translation import set_current_lang
    set_current_lang("pt")
    from triton.ui import tab_modulacao_estocastica as T
    graficos = {
        "fig52_modulacao_economia.png": T._GraficoLeque("x", "potencial_pct", "Poupança de água potável (%)", 1),
        "fig53_modulacao_vpl.png": T._GraficoLeque("x", "vpl_brl", "VAL (€, ilustrativo)", 0),
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


def _apagar_do_rastro_antigo():
    """Retira as tabelas por modelo climático, que eram do exemplo da base CLIMBra (Brasil)."""
    for nome in ("cap43_modelos.md", "cap43_modelos.json", "cap43_modelos_variancia.md"):
        caminho = os.path.join(TABELAS, nome)
        if os.path.exists(caminho):
            os.remove(caminho)
            print(f"  removido: {os.path.relpath(caminho, AQUI)}")


def main():
    cfg, r = _simular(CASO)
    figuras(r)
    os.makedirs(TABELAS, exist_ok=True)
    arquivos = {"cap40_catalogo.md": tabela_catalogo(), **tabelas_do_exemplo(cfg, r)}
    cfg_c, r_c = _simular(CASO_CAPTACAO)
    arquivos.update(tabelas_da_captacao(cfg_c, r_c))
    for nome, conteudo in arquivos.items():
        with open(os.path.join(TABELAS, nome), "w", encoding="utf-8", newline="\n") as f:
            f.write(conteudo + NL)
        print(f"  partes/_tabelas/{nome}")
    _apagar_do_rastro_antigo()
    for nome, res in (("cap43_modulacao.json", r), ("cap43_captacao.json", r_c)):
        with open(os.path.join(TABELAS, nome), "w", encoding="utf-8", newline="\n") as f:
            json.dump({k: v for k, v in res.items() if k != "amostras"}, f, ensure_ascii=False, indent=1)
        print(f"  partes/_tabelas/{nome}")
    return r


if __name__ == "__main__":
    print("modulação probabilística:")
    main()
