# -*- coding: utf-8 -*-
"""Compõe as equações do manual em tipografia matemática.

O manual escreve a equação em notação corrente, legível no Markdown:

    V_cap,t = P_ef,t × A × C

e este módulo a traduz para a notação do TeX e a compõe com o mecanismo
matemático do matplotlib, que implementa um subconjunto amplo do TeX e usa a
família Computer Modern — a mesma dos artigos compostos em LaTeX. O resultado
é uma imagem, embutida no PDF no lugar do texto monoespaçado.

A alternativa seria escrever TeX direto no Markdown. Foi descartada porque
tornaria o texto-fonte do manual ilegível para quem o edita sem conhecer TeX, e
porque a tradução automática cobre a notação que o manual de fato usa.

Quando a tradução não der conta de uma equação, escreva o TeX à mão no próprio
bloco, prefixando a linha com `tex:`.
"""

from __future__ import annotations

import hashlib
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "figuras", "equacoes")
os.makedirs(SAIDA, exist_ok=True)

matplotlib.rcParams["mathtext.fontset"] = "cm"

#: Símbolos que o manual escreve em Unicode e o TeX escreve por nome.
SIMBOLOS = [
    # O sinal de subtração não entra aqui: dentro de um índice ele é parte
    # do nome, como em `V_res,t−1`, e o tradutor o resolve token a token.
    ("×", r" \times "), ("÷", r" \div "), ("·", r" \cdot "),
    ("≥", r" \geq "), ("≤", r" \leq "), ("≠", r" \neq "), ("≈", r" \approx "),
    ("Σ", r" \sum "), ("Δ", r" \Delta "), ("η", r" \eta "), ("ρ", r" \rho "),
    ("⌊", r" \lfloor "), ("⌋", r" \rfloor "), ("′", "'"),
    ("₂", "_2"), ("²", "^2"), ("³", "^3"), ("∞", r" \infty "),
]

#: Palavras que aparecem dentro da equação e são texto, não variável.
#: Só entram aqui palavras de duas letras ou mais que não podem ser confundidas
#: com uma variável: «a», «de» e «em» saíram da lista porque «A» é a área de
#: captação e «C» é o coeficiente de escoamento.
PALAVRAS = (
    "para", "quando", "caso", "contrário", "toda", "sequência", "úmidos",
    "pleno", "parcial", "nulo", "min", "max",
)

#: Nomes compostos que precisam sair em romano, e não em itálico de variável.
NOMES = (
    "PRCPTOT", "R95p", "RX1day", "RX5day", "SDII", "R20mm", "CDD", "CWD", "SI",
    "CAPEX", "VPL", "TMA", "pleno", "parcial", "nulo",
)


def _variavel(token):
    """Traduz `V_cap,t` para `V_{cap,t}`, com o índice em romano."""
    if "_" not in token:
        if len(token) > 1 and token not in NOMES:
            return r"\mathrm{" + token + "}"
        return token
    base, _, indice = token.partition("_")
    indice = indice.replace("−", "-")
    # A base de várias letras é um nome, e não um produto de variáveis: sai em
    # romano, como manda a convenção tipográfica da ABNT NBR 14724.
    if len(base) > 1:
        base = r"\mathrm{" + base + "}"
    return base + "_{" + r"\mathrm{" + indice + "}}"


#: Um símbolo é uma letra, com índice opcional depois do sublinhado; o resto
#: são números, comandos de TeX já prontos, e pontuação de um caractere só.
TOKEN = re.compile(
    r"\\[A-Za-z]+"                      # comando de TeX
    r"|[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9]*(?:_[A-Za-zÀ-ÿ0-9,′\-−]+)?"  # símbolo
    r"|[\d]+(?:[.,][\d]+)?"               # número
    r"|\S"                                # qualquer outro caractere
)

#: Pontuação que passa direto para o TeX.
DIRETO = set("+-=<>()[]|:,;'/.")


def para_tex(linha):
    """Traduz a notação do manual para a notação do TeX."""
    t = linha.strip()
    if t.startswith("tex:"):
        return t[4:].strip()

    for de, para in SIMBOLOS:
        t = t.replace(de, para)

    saida = []
    for token in TOKEN.findall(t):
        if token.startswith("\\"):
            saida.append(token)
        elif token in "{}":
            saida.append("\\" + token)
        elif token == "−":
            saida.append("-")
        elif token in DIRETO:
            saida.append(token)
        elif token == "#":
            saida.append(r"\#")
        elif re.fullmatch(r"[\d]+(?:[.,][\d]+)?", token):
            saida.append(token)
        elif token in NOMES:
            saida.append(r"\mathrm{" + token + "}")
        elif token.lower() in PALAVRAS:
            saida.append(r"\;\mathrm{" + token + r"}\;")
        else:
            saida.append(_variavel(token))
    return " ".join(saida)


def compor(fonte, nome):
    """Compõe a equação e devolve o caminho da imagem e a altura em pontos."""
    tex = " ".join(para_tex(l) for l in fonte.strip().split(chr(10)) if l.strip())
    chave = hashlib.md5((tex + "|v2").encode("utf-8")).hexdigest()[:10]
    caminho = os.path.join(SAIDA, f"{nome}_{chave}.png")
    if os.path.exists(caminho):
        return caminho

    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0, 0, "$" + tex + "$", fontsize=15, color="#14171a")
    try:
        fig.savefig(caminho, dpi=320, bbox_inches="tight", pad_inches=0.03,
                    transparent=True)
    except Exception as erro:
        plt.close(fig)
        raise ValueError(f"equação «{nome}» não compõe: {erro}{chr(10)}{tex}")
    plt.close(fig)
    return caminho


def compor_do_manual(caminho_do_manual):
    """Compõe todas as equações do manual montado e devolve {nome: imagem}."""
    texto = open(caminho_do_manual, encoding="utf-8").read()
    imagens = {}
    for m in re.finditer(r"^```equacao:([^:\n]+):(\d+)\s*$(.*?)^```\s*$",
                         texto, flags=re.M | re.S):
        nome, _numero, corpo = m.group(1), m.group(2), m.group(3)
        imagens[nome] = compor(corpo, nome)
    return imagens


if __name__ == "__main__":
    alvo = os.path.join(AQUI, "Manual-Netuno-5.md")
    if not os.path.exists(alvo):
        print("monte o manual antes: python manual/gerar.py")
        raise SystemExit(1)
    feitas = compor_do_manual(alvo)
    print(f"{len(feitas)} equações compostas em figuras/equacoes/")
