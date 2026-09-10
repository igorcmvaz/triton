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
    ("Parte 1 — Comece aqui", [
        (1, "o_que_o_netuno_faz"), (2, "instalacao"), (3, "por_onde_comecar"),
    ]),
    ("Parte 2 — Tutorial: um estudo do começo ao fim", [
        (4, "o_projeto_e_a_chuva"), (5, "a_edificacao_e_a_demanda"),
        (6, "a_primeira_simulacao"), (7, "escolher_o_volume"),
        (8, "reservatorio_superior"), (9, "qualidade_que_o_uso_exige"),
        (10, "quanto_custa"), (11, "quanto_carbono_evita"),
        (12, "qual_volume_escolher"), (13, "o_relatorio_e_o_artigo"),
    ]),
    ("Parte 3 — Guias de tarefa", [
        (14, "comparar_cidades"), (15, "cenario_climatico"),
        (16, "ajustar_a_tarifa"), (17, "modular_a_demanda"),
        (18, "escola_hospital_comercio"), (19, "rodar_em_lote"),
        (20, "sensibilidade"), (21, "importar_do_netuno4"),
        (22, "exportar_cad_bim_planilha"),
    ]),
    ("Parte 4 — O método", [
        (23, "balanco_diario"), (24, "volume_ideal"), (25, "indicadores"),
        (26, "indices_pluviometricos"), (27, "etap"),
        (28, "energia_de_bombeamento"), (29, "analise_economica"),
        (30, "acv"), (31, "certificacoes"), (32, "multicriterio"),
    ]),
    ("Parte 5 — Enganos comuns de projeto", [
        (33, "dez_enganos"),
    ]),
    ("Parte 6 — Confiabilidade", [
        (34, "verificacao"), (35, "comparacao_netuno4"), (36, "limitacoes"),
        (37, "mensagens_de_erro"),
    ]),
]

APENDICES = [
    ("A", "A_parametros"), ("B", "B_processos"), ("C", "C_fatores_de_emissao"),
    ("D", "D_regimes_tarifarios"), ("E", "E_base_climatica"),
    ("F", "F_linha_de_comando"), ("G", "G_glossario"), ("H", "H_referencias"),
    ("I", "I_fichas"),
]

TITULOS = {
    1: "O que o Netuno faz, e o que ele não faz",
    2: "Instalação e primeira execução",
    3: "Por onde começar, conforme o seu objetivo",
    4: "O projeto e a chuva", 5: "A edificação e a demanda",
    6: "A primeira simulação", 7: "Escolher o volume",
    8: "Precisa de reservatório superior?", 9: "Que qualidade o uso exige",
    10: "Quanto custa e em quanto se paga", 11: "Quanto carbono evita",
    12: "Qual volume escolher, afinal", 13: "O relatório, e o que declarar num artigo",
    14: "Comparar cidades", 15: "Usar cenário climático futuro",
    16: "Ajustar a tarifa do seu município", 17: "Modular a demanda por calendário",
    18: "Simular escola, hospital e comércio", 19: "Rodar em lote",
    20: "Análise de sensibilidade", 21: "Importar um projeto do Netuno 4",
    22: "Exportar para CAD, BIM e planilha",
    23: "O balanço hídrico diário", 24: "Volume ideal e a varredura",
    25: "Indicadores de eficiência", 26: "Índices pluviométricos",
    27: "Dimensionamento da ETAP", 28: "Energia de bombeamento",
    29: "Análise econômica e os regimes tarifários",
    30: "Avaliação de ciclo de vida", 31: "Certificações",
    32: "Decisão multicritério",
    33: "Dez enganos que o programa não impede",
    34: "Como o programa é verificado", 35: "Comparação com o Netuno 4",
    36: "Limitações conhecidas", 37: "Mensagens de erro e o que fazer",
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
