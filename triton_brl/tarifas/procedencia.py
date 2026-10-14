# -*- coding: utf-8 -*-
"""De onde vem a tarifa de cada município, e o que falta fazer com ela.

Classes da residencial (uma por município):

* ``completa``    — transcrita de documento guardado, com as quatro categorias também;
* ``documentada`` — residencial transcrita de documento guardado em `tarifas/fontes/`;
* ``a_renovar``   — documentada, mas a vigência tem mais de 12 meses;
* ``sem_documento`` — auditada pelo catálogo antigo, sem o documento guardado;
* ``a_confirmar`` — valor na base sem auditoria;
* ``ruim``        — dado sabidamente errado (grau D).

`FILA.md` é gerado daqui: documentos recebidos e ainda não transcritos, com os municípios
que cada um destrava, e os municípios a renovar.

Uso:
    python tarifas/procedencia.py        # regera tarifas/transcricoes/FILA.md
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _p in (AQUI, os.path.join(RAIZ, "manual")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import registro_de_fontes as R  # noqa: E402
import tabela_de_faixas as T  # noqa: E402

FILA = os.path.join(AQUI, "transcricoes", "FILA.md")
CATEGORIAS = ("comercial", "publica", "industrial", "social")
MESES_PARA_RENOVAR = 12
NL = chr(10)

CLASSES = {
    "completa": "documentada, com as 4 categorias",
    "documentada": "residencial documentada",
    "a_renovar": "documentada, vigência com mais de 12 meses",
    "sem_documento": "auditada sem documento guardado",
    "a_confirmar": "a confirmar",
    "ruim": "dado ruim",
}


def data_da_vigencia(texto) -> date | None:
    """A data de início da vigência, de textos como «01/04/2026», «2025», «abr/2026»."""
    texto = str(texto or "")
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", texto)
    if m:
        d, mes, a = map(int, m.groups())
        return date(a, mes, d)
    m = re.search(r"\b(\d{1,2})/(\d{4})\b", texto)
    if m:
        return date(int(m.group(2)), int(m.group(1)), 1)
    m = re.search(r"\b(20\d\d)\b", texto)
    if m:
        return date(int(m.group(1)), 1, 1)
    return None


def _meses(desde: date, hoje: date) -> int:
    return (hoje.year - desde.year) * 12 + hoje.month - desde.month


def classe(d: dict, hoje: date | None = None) -> str:
    hoje = hoje or date.today()
    if d.get("fonte_registro"):
        inicio = data_da_vigencia(d.get("vigencia_saneamento"))
        if inicio and _meses(inicio, hoje) > MESES_PARA_RENOVAR:
            return "a_renovar"
        extra = d.get("categorias") or {}
        if all(c in extra and extra[c].get("fonte_registro") for c in CATEGORIAS):
            return "completa"
        return "documentada"
    cor = T.situacao(d)
    if cor == "vermelho":
        return "ruim"
    if cor == "amarelo":
        return "a_confirmar"
    return "sem_documento"


def origem(d: dict, itens: dict) -> dict:
    """O documento-base do município, para o mapa e a tabela da lista de coleta."""
    ids = d.get("fonte_registro") or []
    item = itens.get(ids[0]) if ids else None
    return {
        "doc": d.get("fonte_documento") or "",
        "tab": d.get("fonte_tabela") or "",
        "reg": ids,
        "rec": item["recebido_em"] if item else "",
        "onde": item["guardado_em"] if item else "",
        "vig": str(d.get("vigencia_saneamento") or ""),
        "url": d.get("fonte_url") or "",
        "motivo": d.get("motivo_dado_ruim") or "",
        "abrangencia": d.get("fonte_abrangencia") or "",
    }


def _mesmo(prestador_do_registro: str, prestador_da_base: str) -> bool:
    """«SANEPAR» casa com «SANEPAR – Curitiba»; «CAER» não casa com «CAERN»."""
    return re.search(r"(?<!\w)" + re.escape(prestador_do_registro.lower()) + r"(?!\w)",
                     prestador_da_base.lower()) is not None


def gerar_fila() -> str:
    cidades = T.carregar()
    reg = R.carregar()
    por_prestador = defaultdict(list)
    for d in cidades.values():
        por_prestador[d.get("prestador_saneamento") or "—"].append(d)

    L = ["# Fila da base tarifária", "",
         f"Gerado em {date.today().isoformat()} por `tarifas/procedencia.py`. Não edite à mão.", "",
         "Fluxo: arquivo novo em `tarifas/entrada/` → `python tarifas/processar_entrada.py` (registra e "
         "move para `tarifas/fontes/<prestador>/`) → transcrição em `tarifas/transcricoes/<prestador>.json` → "
         "`python tarifas/aplicar_transcricoes.py --aplicar`. Por município vale a transcrição de vigência "
         "mais recente.", ""]

    conta = Counter(classe(d) for d in cidades.values())
    L += ["## Situação dos municípios", "", "| Classe | Municípios |", "| :--- | ---: |"]
    for k, rot in CLASSES.items():
        L.append(f"| {rot} | {conta[k]} |")
    L += [f"| **total** | **{len(cidades)}** |", ""]

    L += ["## 1. Recebidos, a transcrever", "",
          "Documentos já guardados em `tarifas/fontes/` que ainda não viraram transcrição. "
          "Em ordem de municípios que destravam.", "",
          "| # | Recebido | Prestador | Arquivo | Vigência | Municípios na base |",
          "| ---: | :--- | :--- | :--- | :--- | ---: |"]
    pend = [i for i in reg["itens"] if i["situacao"] == "recebido"]

    def n_mun(i):
        return sum(len(v) for p, v in por_prestador.items() if _mesmo(i["prestador"], p))
    for i in sorted(pend, key=lambda i: (-n_mun(i), i["id"])):
        L.append(f"| {i['id']} | {i['recebido_em']} | {i['prestador']} | {i['arquivo']} | "
                 f"{i.get('vigencia') or '—'} | {n_mun(i)} |")
    L.append("")

    cons = [i for i in reg["itens"] if i["situacao"] == "consultado" and i.get("guardado_em")
            and not str(i.get("uso", "")).startswith("tarifas/transcricoes/")]
    if cons:
        L += ["### Consultados sem transcrição: o que faltou", "",
              "| # | Prestador | Arquivo | Por que não virou transcrição |", "| ---: | :--- | :--- | :--- |"]
        for i in cons:
            L.append(f"| {i['id']} | {i['prestador']} | {i['arquivo']} | {i.get('uso') or '—'} |")
        L.append("")

    L += ["## 2. Documentados com vigência antiga (a renovar)", "",
          f"Vigência com mais de {MESES_PARA_RENOVAR} meses: procurar o reajuste mais recente.", "",
          "| Município | Prestador | Documento | Vigência |", "| :--- | :--- | :--- | :--- |"]
    for k, d in sorted(cidades.items()):
        if classe(d) == "a_renovar":
            L.append(f"| {k} | {d.get('prestador_saneamento')} | {d.get('fonte_documento')} | "
                     f"{d.get('vigencia_saneamento')} |")
    L.append("")

    L += ["## 3. Sem documento: o que buscar", "",
          "Prestadores com municípios ainda sem documento guardado. A pasta é só sugestão: "
          "qualquer nome serve, o processamento identifica o prestador.", "",
          "| Prestador | Sem documento | A confirmar | Ruim | Já recebido, falta transcrever |",
          "| :--- | ---: | ---: | ---: | :---: |"]
    recebidos = {i["prestador"] for i in pend}
    linhas = []
    for p, lista in por_prestador.items():
        c = Counter(classe(d) for d in lista)
        falta = c["sem_documento"] + c["a_confirmar"] + c["ruim"]
        if falta:
            linhas.append((falta, p, c))
    for falta, p, c in sorted(linhas, key=lambda x: (-x[0], x[1].lower())):
        tem = "sim" if any(_mesmo(r, p) for r in recebidos) else ""
        L.append(f"| {p} | {c['sem_documento']} | {c['a_confirmar']} | {c['ruim']} | {tem} |")
    texto = NL.join(L) + NL
    os.makedirs(os.path.dirname(FILA), exist_ok=True)
    with open(FILA, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    return texto


if __name__ == "__main__":
    gerar_fila()
    print(f"gerado: {os.path.relpath(FILA, RAIZ)}")
