# -*- coding: utf-8 -*-
"""Checks that the English manual follows the Portuguese one, section by section.

For each section of `gerar.ESTRUTURA`, the English file must exist and carry the same
skeleton as the Portuguese one: the same headings at each level, the same figures in the
same order, the same equations, the same cross-reference marks, the same included tables
and the same number of tables. The words are free; the structure is not. Anything the
Portuguese manual gains or loses shows up here until the English one follows.

It also looks for Portuguese left in the English text.

Usage:
    python manual/en/conferir.py            # every section
    python manual/en/conferir.py 23 24      # only these sections (file prefix)

`tests/unit/test_manual_en.py` runs the same checks.
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
MANUAL = os.path.dirname(AQUI)
if MANUAL not in sys.path:
    sys.path.insert(0, MANUAL)

import gerar  # noqa: E402

NL = chr(10)

#: Words that do not exist in English text, outside code, references and proper names.
_PORTUGUES = re.compile(
    r"\b(não|são|também|então|está|estão|uma|pelo|pela|pelos|pelas|seção|capítulo|"
    r"porque|quando|onde|como|mais|menos|cada|entre|sobre|depois|antes|ainda|"
    r"água|chuva|volume\s+ideal\s+é|reservatório|cisterna|programa\s+não)\b",
    re.IGNORECASE)

#: Sections whose text legitimately quotes Portuguese: reference titles, the glossary's
#: original terms, messages the program prints in Portuguese.
_TOLERANCIA = {"H_referencias": 10**6, "G_glossario": 80, "37_mensagens_de_erro": 80,
               "D_regimes_tarifarios": 10**6,  # nomes de municípios e prestadores
               "A_parametros": 5, "22_exportar_cad_bim_planilha": 15,
               "38_historico_de_versoes": 10, "16_ajustar_a_tarifa": 15, "21_importar_do_netuno4": 10,
               "F_arquivos_e_formatos": 15, "27_etap": 3,  # a sigla ETAP explicada em português
               "J_arquivos_de_exemplo": 15, "31_certificacoes": 10}


def secoes():
    for _, pasta, chaves in gerar.ESTRUTURA:
        for chave in chaves:
            yield pasta, chave


#: Proper names with Portuguese words in them.
_NOMES_PROPRIOS = ("São Paulo", "Casa Azul", "IPTU Verde", "Selo Casa Azul")


def _sem_codigo(texto):
    for nome in _NOMES_PROPRIOS:
        texto = texto.replace(nome, "")
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)
    texto = re.sub(r"`[^`\n]*`", "", texto)
    texto = re.sub(r"\*[^*\n]*\*", lambda m: m.group(0), texto)
    return texto


def esqueleto(texto):
    linhas = texto.split(NL)
    fora = []
    dentro = False
    for linha in linhas:
        if linha.startswith("```"):
            dentro = not dentro
            if linha.startswith("```equacao:"):
                fora.append(linha)
            continue
        if not dentro:
            fora.append(linha)
    corpo = NL.join(fora)
    return {
        "títulos": [len(m.group(1)) for m in re.finditer(r"^(#{1,4}) ", corpo, flags=re.M)],
        "figuras": re.findall(r"^!\[[^\]]*\]\(([^)]+)\)", corpo, flags=re.M),
        "chamadas de figura": Counter(re.findall(r"\{\{fig:([^}]+)\}\}", corpo)),
        "equações": re.findall(r"^```equacao:(\S+)", corpo, flags=re.M),
        "citações de equação": Counter(re.findall(r"\{\{eq:([^}]+)\}\}", corpo)),
        "remissões": sorted(set(re.findall(r"\{\{[nc]:([^}]+)\}\}", corpo))),
        "inclusões": re.findall(r"<!--\s*inclui:\s*(\S+)\s*-->", corpo),
        "tabelas": len(re.findall(r"^\|[\s:\-|]+\|\s*$", corpo, flags=re.M)),
    }


def problemas_da_secao(pasta, chave):
    pt = os.path.join(MANUAL, pasta, chave + ".md")
    en = os.path.join(AQUI, pasta, chave + ".md")
    if not os.path.exists(en):
        return [f"{chave}: falta o arquivo em inglês"]
    texto_pt = open(pt, encoding="utf-8").read()
    texto_en = open(en, encoding="utf-8").read()
    achados = []
    a, b = esqueleto(texto_pt), esqueleto(texto_en)
    for item in a:
        if item == "remissões":
            # O texto em inglês pode remeter a mais seções (as notas da International
            # Edition), mas não a menos.
            faltam = sorted(set(a[item]) - set(b[item]))
            if faltam:
                achados.append(f"{chave}: remissões ausentes no inglês: {faltam}")
            continue
        if a[item] != b[item]:
            achados.append(f"{chave}: {item} diferem — pt {a[item]} / en {b[item]}")
    if "Figura " in texto_en or "<!-- tabela: **Tabela" in texto_en:
        achados.append(f"{chave}: rótulo «Figura»/«Tabela» em português")
    if "**Aprofundamento" in texto_en or "**Atenção" in texto_en:
        achados.append(f"{chave}: caixa marcada em português")
    if "| Símbolo | Significado | Unidade |" in texto_en:
        achados.append(f"{chave}: cabeçalho de variáveis em português")
    restos = _PORTUGUES.findall(_sem_codigo(texto_en))
    if len(restos) > _TOLERANCIA.get(chave, 0):
        amostra = ", ".join(sorted(set(r.lower() for r in restos))[:12])
        achados.append(f"{chave}: {len(restos)} palavra(s) em português: {amostra}")
    return achados


def problemas(filtro=()):
    achados = []
    for pasta, chave in secoes():
        if filtro and not any(chave.startswith(f) for f in filtro):
            continue
        achados += problemas_da_secao(pasta, chave)
    return achados


if __name__ == "__main__":
    lista = problemas(sys.argv[1:])
    for p in lista:
        print(p)
    print(f"{len(lista)} problema(s)")
    sys.exit(1 if lista else 0)
