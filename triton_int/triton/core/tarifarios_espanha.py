# -*- coding: utf-8 -*-
"""Tarifas de água de Espanha, por camadas de confiança (``triton/data/espanha_tarifarios.json``, só na IBE).

Camada 1: tarifário do município, transcrito de documento oficial arquivado (URL, data de acesso, SHA-256); mesma
estrutura do ``portugal_tarifarios.json``. Camada 2: município sem documento próprio que herda o da sua entidade
(``herda_de``), sempre com aviso. Camada 3: média regional do INE (um preço total por m3, sem parte fixa), só
indicativa. Nenhum valor é inventado: município sem camada 1, 2 ou 3 devolve ``None`` e a interface diz «sem tarifa».

Camada 1 transcrita mas ainda não conferida (``procedencia.conferido`` falso): o aviso diz «Tarifa transcrita, ainda não
conferida (segunda leitura pendente)» com a fonte. ``iva_pct`` nulo significa «a taxa não consta da fonte»: o cálculo usa 0 %
nesse serviço (conta sem IVA, nunca com taxa suposta) e o aviso diz «IVA do <serviço> não consta da fonte».
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Dict, Optional

from triton.core.fatura_portuguesa import Escalao, FaturaPortuguesa, Parcela

_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "data", "espanha_tarifarios.json")
ROTULO_DA_CAMADA = {1: "tarifa do município (transcrita)", 2: "tarifa de outra entidade ou município (herdada)",
                    3: "média regional do INE (indicativa)"}


@lru_cache(maxsize=1)
def carregar() -> dict:
    if not os.path.isfile(_ARQUIVO):
        return {}
    with open(_ARQUIVO, encoding="utf-8") as f:
        return json.load(f)


def _pct(valor) -> float:
    """Taxa de imposto em %; ``None`` (taxa que não consta da fonte) vale 0 no cálculo, e o aviso declara a falta."""
    return 0.0 if valor is None else float(valor)


def _escaloes(lista):
    return [Escalao(float(a), None if b is None else float(b), float(p)) for a, b, p in lista]


def _fatura_do_municipio(d: dict, codigo: str) -> FaturaPortuguesa:
    agua, san = d["agua"], d.get("saneamiento") or {}
    f = FaturaPortuguesa(
        entidade=d.get("entidades", ""), concelho=d.get("nome", codigo), fixa_agua=float(agua["fixa_mes"]),
        escaloes=_escaloes(agua["escaloes"]), iva_agua_pct=_pct(agua.get("iva_pct")),
        parcelas=[Parcela(p["nome"], float(p.get("fixa", 0.0)), float(p.get("por_m3", 0.0)), _pct(p.get("iva_pct", 0.0)))
                  for p in d.get("parcelas", [])],
        fonte="; ".join(d.get("fontes", [])), vigencia=d.get("vigencia", ""))
    if san.get("escaloes"):
        f.saneamento_escaloes = _escaloes(san["escaloes"])
        f.saneamento_fixa = float(san.get("fixa_mes", 0.0))
        f.coef_recolha = float(san.get("coef_recolha", 1.0))
        f.iva_saneamento_pct = _pct(san.get("iva_pct", 0.0))
    f.validar()
    return f


def _resolver(codigo: str, profundidade: int = 0) -> Optional[tuple]:
    """(camada, registro) do município: 1 própria, 2 herdada, 3 média da comunidade; None se não houver nada."""
    dados = carregar()
    m = (dados.get("municipios") or {}).get(codigo)
    if m and m.get("camada") == 1 and m.get("agua"):
        return 1, m
    if m and m.get("camada") == 2 and m.get("herda_de") and profundidade < 3:
        base = _resolver(m["herda_de"], profundidade + 1)
        if base and base[0] == 1:
            return 2, {**base[1], "aviso": m.get("aviso") or "tarifa de outro município da mesma entidade gestora; confirme na sua fatura"}
    from triton.core import base_climatica_iberica as _ib
    u = _ib.unidade(codigo) if _ib.disponivel() else None
    c3 = (dados.get("camada3") or {})
    preco = (c3.get("eur_m3_total") or {}).get((u or {}).get("regiao", ""))
    if preco is not None:
        return 3, {"regiao": u["regiao"], "eur_m3_total": float(preco), "ano": c3.get("ano"), "aviso": c3.get("aviso", ""),
                   "fonte": c3.get("fonte", ""), "url": c3.get("url", ""), "sha256_documento": c3.get("sha256_documento", "")}
    return None


def camada(codigo: str) -> Optional[int]:
    r = _resolver(codigo)
    return r[0] if r else None


def fatura(codigo: str) -> Optional[FaturaPortuguesa]:
    r = _resolver(codigo)
    if r is None:
        return None
    cam, reg = r
    if cam in (1, 2):
        return _fatura_do_municipio(reg, codigo)
    f = FaturaPortuguesa(entidade=f"Média regional INE, {reg['regiao']} ({reg['ano']})", concelho=codigo, fixa_agua=0.0,
                         escaloes=[Escalao(0.0, None, reg["eur_m3_total"])], iva_agua_pct=0.0, parcelas=[],
                         fonte=f"{reg['fonte']} — {reg['url']}", vigencia=str(reg["ano"]))
    f.validar()
    return f


_SERVICO_SEM_IVA = {"agua": ("da água", "of water"), "saneamiento": ("do saneamento", "of sanitation"),
                    "parcelas": ("das parcelas adicionais", "of the additional charges")}


def iva_ausente(codigo: str) -> list:
    """Serviços da camada 1 (ou 2) cujo ``iva_pct`` é nulo na fonte: subconjunto de ``agua``, ``saneamiento``, ``parcelas``."""
    r = _resolver(codigo)
    if r is None or r[0] not in (1, 2):
        return []
    reg = r[1]
    falta = []
    if (reg.get("agua") or {}).get("iva_pct") is None:
        falta.append("agua")
    san = reg.get("saneamiento") or {}
    if san.get("escaloes") and san.get("iva_pct") is None:
        falta.append("saneamiento")
    if any(p.get("iva_pct") is None for p in reg.get("parcelas", [])):
        falta.append("parcelas")
    return falta


def conferida(codigo: str) -> bool:
    """Verdadeiro só se a camada 1 do município tem a segunda leitura registada (``procedencia.conferido``)."""
    r = _resolver(codigo)
    return bool(r and r[0] == 1 and (r[1].get("procedencia") or {}).get("conferido"))


def fonte_da_camada1(codigo: str) -> dict:
    """Entidade, URL, data de acesso, SHA-256 e vigência do documento principal da camada 1 ({} se não houver)."""
    r = _resolver(codigo)
    if r is None or r[0] not in (1, 2):
        return {}
    reg = r[1]
    docs = (reg.get("procedencia") or {}).get("documentos") or []
    if not docs:
        return {}
    d = docs[0]
    return {"entidade": d.get("entidade") or reg.get("entidades", ""), "url": d.get("url", ""),
            "acedido_em": d.get("confirmado_em", ""), "sha256": d.get("sha256", ""), "vigencia": reg.get("vigencia", "")}


def nota_da_camada1(codigo: str, lingua: str = "pt") -> str:
    """«Tarifa transcrita, ainda não conferida (segunda leitura pendente)», a fonte e as taxas que faltam; vazio fora da camada 1."""
    r = _resolver(codigo)
    if r is None or r[0] != 1:
        return ""
    en = lingua == "en"
    f = fonte_da_camada1(codigo)
    if not conferida(codigo):
        txt = ("Transcribed tariff, not yet checked (second reading pending)." if en
               else "Tarifa transcrita, ainda não conferida (segunda leitura pendente).")
    else:
        txt = "Transcribed tariff, checked against a second reading." if en else "Tarifa transcrita e conferida em segunda leitura."
    if f:
        txt += (f" Source: {f['entidade']}, {f['url']}, accessed {f['acedido_em']}, in force: {f['vigencia']}." if en
                else f" Fonte: {f['entidade']}, {f['url']}, acedida em {f['acedido_em']}, vigência: {f['vigencia']}.")
    for k in iva_ausente(codigo):
        txt += (f" VAT {_SERVICO_SEM_IVA[k][1]} is not stated in the source (calculated without it)." if en
                else f" IVA {_SERVICO_SEM_IVA[k][0]} não consta da fonte (calculado sem ele).")
    return txt


def aviso(codigo: str) -> str:
    """O aviso que acompanha a camada 1 não conferida, a 2 e a 3 (vazio na 1 conferida sem taxas em falta e sem tarifa)."""
    r = _resolver(codigo)
    if r is None:
        return ""
    if r[0] == 1:
        return nota_da_camada1(codigo) if (not conferida(codigo) or iva_ausente(codigo)) else ""
    return r[1].get("aviso") or ""


def procedencia(codigo: str) -> str:
    r = _resolver(codigo)
    if r is None:
        return "sem tarifa: nenhuma fonte verificada para este município"
    cam, reg = r
    txt = f"camada {cam}: {ROTULO_DA_CAMADA[cam]}"
    if cam == 3:
        txt += f"; {reg['eur_m3_total']:.2f}".replace(".", ",") + f" €/m³ total (água e saneamento), {reg['ano']}; {reg['aviso']}"
    elif cam == 2:
        txt += f"; {reg.get('aviso', '')}"
    else:
        txt += f"; {nota_da_camada1(codigo)}"
    return txt


def aplicar(codigo: str, cfg) -> bool:
    """Grava no projeto a tarifa do município de Espanha (camada 1, 2 ou 3); False se não houver (a tarifa fica vazia)."""
    from triton.core.fatura_portuguesa import aplicar_ao_projeto
    f = fatura(codigo)
    if f is None:
        return False
    aplicar_ao_projeto(f, cfg)
    cfg.tariff_city_name = codigo
    cfg.tariff_vigencia = f.vigencia
    cfg.tariff_category = "residencial"
    return True


def contagem_por_camada() -> Dict[int, int]:
    """Quantos municípios de Espanha têm cada camada (lida dos dados, nunca digitada)."""
    from triton.core import base_climatica_iberica as _ib
    c = {1: 0, 2: 0, 3: 0, 0: 0}
    for u in _ib.unidades():
        if u["pais"] != "ES":
            continue
        k = camada(u["codigo"])
        c[k or 0] += 1
    return c
