# -*- coding: utf-8 -*-
"""Monta o manual inteiro num arquivo só, resolvendo as inclusões de tabela.

Um capítulo pede uma tabela gerada assim:

    <!-- inclui: _tabelas/cap13_dez_dias.md -->

e este script troca a linha pelo conteúdo do arquivo. Se o arquivo não existir, o
manual não é montado: número faltando é pior que erro visível.

Uso:
    python manual/gerar_tabelas.py
    python manual/gerar_apendices.py
    python manual/gerar.py
"""

from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
INCLUI = re.compile(r"^<!--\s*inclui:\s*(\S+)\s*-->\s*$")

#: A ordem do manual. Capítulo sem arquivo entra como esqueleto marcado.
SUMARIO = [
    ("Parte I — O programa", [
        (1, "introducao"), (2, "instalacao"), (3, "a_janela"), (4, "arquivos"),
    ]),
    ("Parte II — Entrada de dados", [
        (5, "precipitacao"), (6, "captacao"), (7, "edificacao_e_demanda"),
        (8, "irrigacao"), (9, "qualidade_da_agua"), (10, "reservatorios"),
        (11, "custos_e_tarifas"), (12, "parametros_ambientais"),
    ]),
    ("Parte III — Método de cálculo", [
        (13, "balanco_diario"), (14, "volume_ideal"), (15, "indicadores"),
        (16, "indices_pluviometricos"), (17, "etap"), (18, "energia_de_bombeamento"),
        (19, "analise_economica"), (20, "acv"), (21, "certificacoes"),
        (22, "multicriterio"),
    ]),
    ("Parte IV — Estudos de caso", [
        (23, "caso_residencia"), (24, "caso_recalque"), (25, "caso_varredura"),
        (26, "caso_economico"), (27, "caso_escola"), (28, "caso_tres_cidades"),
        (29, "caso_cenarios_climaticos"), (30, "caso_qualidade"),
        (31, "caso_multicriterio"),
    ]),
    ("Parte V — Verificação e limites", [
        (32, "verificacao"), (33, "comparacao_netuno4"), (34, "limitacoes"),
        (35, "mensagens_de_erro"),
    ]),
    ("Parte VI — Linha de comando", [
        (36, "linha_de_comando"), (37, "lote_e_sensibilidade"),
    ]),
]

APENDICES = [
    ("A", "A_parametros"), ("B", "B_processos"), ("C", "C_fatores_de_emissao"),
    ("D", "D_base_tarifaria"), ("E", "E_base_climatica"), ("F", "F_glossario"),
    ("G", "G_referencias"),
]

TITULOS = {
    1: "Introdução", 2: "Instalação, requisitos e primeira execução",
    3: "A janela: mapa das dezessete abas", 4: "Arquivos do programa",
    5: "Precipitação", 6: "Captação: área, coeficiente e descarte",
    7: "Edificação e demanda", 8: "Irrigação e supressão por chuva",
    9: "Qualidade da água e a ETAP", 10: "Reservatórios e bombeamento",
    11: "Custos, tarifas e parâmetros financeiros", 12: "Parâmetros ambientais",
    13: "O balanço hídrico diário", 14: "Volume ideal e a varredura",
    15: "Indicadores de eficiência", 16: "Índices pluviométricos",
    17: "Dimensionamento da ETAP", 18: "Energia de bombeamento",
    19: "Análise econômica", 20: "Avaliação de ciclo de vida",
    21: "Certificações", 22: "Decisão multicritério",
    23: "Caso 1: residência unifamiliar, volume conhecido",
    24: "Caso 2: com reservatório superior e recalque",
    25: "Caso 3: varredura de volumes",
    26: "Caso 4: análise econômica completa",
    27: "Caso 5: escola pública", 28: "Caso 6: três cidades",
    29: "Caso 7: cenários climáticos", 30: "Caso 8: qualidade da água e ETAP",
    31: "Caso 9: decisão multicritério e certificação",
    32: "Como o programa é verificado", 33: "Comparação com o Netuno 4",
    34: "Limitações conhecidas", 35: "Mensagens de erro e o que fazer",
    36: "Uso pela linha de comando", 37: "Lote, cenários e sensibilidade",
}


def resolver(texto, origem):
    """Troca as linhas de inclusão pelo conteúdo do arquivo referido."""
    saida = []
    for linha in texto.split(NL):
        m = INCLUI.match(linha)
        if not m:
            saida.append(linha)
            continue
        alvo = os.path.join(os.path.dirname(origem), m.group(1))
        if not os.path.exists(alvo):
            raise FileNotFoundError(
                f"{os.path.basename(origem)} pede {m.group(1)}, que não existe. "
                "Rode manual/gerar_tabelas.py antes."
            )
        saida.append(open(alvo, encoding="utf-8").read().rstrip(NL))
    return NL.join(saida)


def esqueleto(num, titulo):
    return NL.join([
        f"# {num}. {titulo}",
        "",
        "> **Capítulo por escrever.** O plano editorial, com o que este capítulo deve",
        "> cobrir e o que já existe escrito no repositório, está em",
        "> `docs/plano_do_manual.md`.",
        "",
    ])


def main():
    partes, faltando, escritos = [], [], []
    for nome_parte, capitulos in SUMARIO:
        partes.append(f"# {nome_parte}" + NL)
        for num, arquivo in capitulos:
            caminho = os.path.join(AQUI, "partes", f"{num:02d}_{arquivo}.md")
            if os.path.exists(caminho):
                texto = resolver(open(caminho, encoding="utf-8").read(), caminho)
                escritos.append(num)
            else:
                texto = esqueleto(num, TITULOS[num])
                faltando.append(num)
            partes.append(texto.rstrip(NL) + NL)

    partes.append("# Apêndices" + NL)
    for letra, arquivo in APENDICES:
        caminho = os.path.join(AQUI, "apendices", f"{arquivo}.md")
        if os.path.exists(caminho):
            partes.append(open(caminho, encoding="utf-8").read().rstrip(NL) + NL)
            escritos.append(letra)
        else:
            partes.append(f"# Apêndice {letra}" + NL + NL
                          + "> **Apêndice por escrever.**" + NL)
            faltando.append(letra)

    destino = os.path.join(AQUI, "Manual-Netuno-5.md")
    corpo = (NL + "---" + NL + NL).join(partes)
    open(destino, "w", encoding="utf-8").write(corpo)

    palavras = len(corpo.split())
    print(f"montado: {os.path.relpath(destino, AQUI)}")
    print(f"  {len(escritos)} de {len(faltando) + len(escritos)} seções escritas")
    print(f"  {palavras:,} palavras, cerca de {palavras // 450} páginas".replace(",", "."))
    if faltando:
        print(f"  por escrever: {', '.join(str(f) for f in faltando)}")
    return len(escritos), len(faltando)


if __name__ == "__main__":
    sys.exit(0 if main() else 0)
