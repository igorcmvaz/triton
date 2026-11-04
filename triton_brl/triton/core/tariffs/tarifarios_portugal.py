# -*- coding: utf-8 -*-
"""Tarifários transcritos da Edição Ibérica (``triton/data/portugal_tarifarios.json``).

Cada concelho traz a água (tarifa fixa e escalões), o saneamento (por escalões sobre o volume
recolhido, ou como parcela por m³), as demais parcelas da fatura e o IVA de cada uma, com as
fontes e as contas de conferência. ``fatura`` devolve a ``FaturaPortuguesa`` pronta para
``fatura_portuguesa.aplicar_ao_projeto``.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Dict, List, Optional

from triton.core.fatura_portuguesa import Escalao, FaturaPortuguesa, Parcela

_a1 = os.path.join(os.path.dirname(__file__), "..", "data", "portugal_tarifarios.json")
_a2 = os.path.join(os.path.dirname(__file__), "..", "..", "data", "portugal_tarifarios.json")
_ARQUIVO = _a1 if os.path.exists(_a1) else _a2


@lru_cache(maxsize=1)
def carregar() -> Dict[str, dict]:
    # Só a Edição Ibérica traz o arquivo; nas demais, nenhum concelho e nenhum erro.
    if not os.path.isfile(_ARQUIVO):
        return {}
    with open(_ARQUIVO, encoding="utf-8") as f:
        dados = json.load(f)
    return {k: v for k, v in dados.items() if not k.startswith("_")}


def concelhos() -> List[str]:
    """Concelhos com tarifário transcrito."""
    return sorted(carregar())


def _escaloes(lista) -> List[Escalao]:
    return [Escalao(float(a), None if b is None else float(b), float(p)) for a, b, p in lista]


def fatura(concelho: str) -> Optional[FaturaPortuguesa]:
    """A fatura doméstica do concelho, ou None se ele ainda não foi transcrito."""
    d = carregar().get(concelho)
    if d is None:
        return None
    agua, san = d["agua"], d.get("saneamento") or {}
    f = FaturaPortuguesa(
        entidade=d["entidades"], concelho=concelho,
        fixa_agua=float(agua["fixa_mes"]), escaloes=_escaloes(agua["escaloes"]),
        iva_agua_pct=float(agua["iva_pct"]),
        parcelas=[Parcela(p["nome"], float(p.get("fixa", 0.0)), float(p.get("por_m3", 0.0)),
                          float(p.get("iva_pct", 0.0))) for p in d.get("parcelas", [])],
        fonte="; ".join(d.get("fontes", [])), vigencia=d.get("vigencia", ""))
    if san.get("escaloes"):
        f.saneamento_escaloes = _escaloes(san["escaloes"])
        f.saneamento_fixa = float(san.get("fixa_mes", 0.0))
        f.saneamento_trh_m3 = float(san.get("trh_m3", 0.0))
        f.coef_recolha = float(san.get("coef_recolha", 1.0))
        f.iva_saneamento_pct = float(san.get("iva_pct", 0.0))
    f.validar()
    return f


def aplicar(concelho: str, cfg) -> bool:
    """Grava no projeto o tarifário do concelho e a vigência; False se não houver."""
    from triton.core.fatura_portuguesa import aplicar_ao_projeto
    f = fatura(concelho)
    if f is None:
        return False
    aplicar_ao_projeto(f, cfg)
    cfg.tariff_city_name = concelho
    cfg.tariff_city_uf = carregar()[concelho].get("distrito", "")
    cfg.tariff_vigencia = f.vigencia
    cfg.tariff_category = "residencial"
    return True


#: Estados de confiança de cada serviço de um concelho: verde (verificado), amarelo (a validar), cinza (sem dado).
ESTADOS = ("verde", "amarelo", "cinza")
#: Quem pode verificar um tarifário de modo independente: uma fatura real (±0,05 € contra o motor) ou uma
#: segunda leitura feita por uma pessoa diferente do transcritor. Um modelo de IA nunca conta.
VERIFICACOES_INDEPENDENTES = ("fatura", "humano")
MESES_DE_CONFIRMACAO = 12
LIMITE_DE_PENDENCIA_PCT = 1.0
ROTULO_DO_SERVICO = {"agua": "água", "saneamento": "saneamento", "residuos": "resíduos"}
SERVICOS = ("agua", "saneamento", "residuos")


def _meses_entre(desde: str, hoje) -> Optional[int]:
    try:
        ano, mes = int(desde[0:4]), int(desde[5:7])
    except (ValueError, TypeError):
        return None
    return (hoje.year - ano) * 12 + hoje.month - mes


def avaliar_servico(documentos: List[dict], transcrito: bool, conferido: bool, pendencias: List[dict],
                    hoje=None) -> tuple:
    """(estado, motivos) de um serviço (água, saneamento ou resíduos) de um concelho.

    Verde exige, tudo junto: documento oficial arquivado com URL e SHA-256; ``confirmado_em`` há menos de
    12 meses; transcrição conferida com as contas impressas (que o teste reproduz); verificação independente
    registada em ``verificado_por`` («fatura» ou «humano»); e nenhuma pendência com efeito acima de 1 % na
    conta de 10 m³ (ou sem efeito quantificável). Amarelo: há documento, mas falta algum desses requisitos.
    Cinza: sem documento. ``motivos`` diz, em texto, o que falta.
    """
    from datetime import date
    hoje = hoje or date.today()
    if not documentos:
        return "cinza", ["sem documento oficial arquivado"]
    motivos: List[str] = []
    if any(not d.get("sha256") or not d.get("url") for d in documentos):
        motivos.append("documento sem URL de origem ou sem SHA-256 registados")
    datas = [str(d.get("confirmado_em") or "") for d in documentos]
    meses = [_meses_entre(x, hoje) for x in datas]
    if any(m is None for m in meses):
        motivos.append("sem data de reconfirmação (confirmado_em)")
    elif max(meses) >= MESES_DE_CONFIRMACAO:
        motivos.append(f"reconfirmado há {max(meses)} meses (o limite é {MESES_DE_CONFIRMACAO})")
    if not transcrito:
        motivos.append("documento arquivado, ainda não transcrito")
    elif not conferido:
        motivos.append("transcrição sem conferência aritmética")
    if any(str(d.get("verificado_por") or "") not in VERIFICACOES_INDEPENDENTES for d in documentos):
        motivos.append("sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa)")
    for p in pendencias:
        efeito = p.get("efeito_pct")
        if efeito is None or efeito > LIMITE_DE_PENDENCIA_PCT:
            quanto = "efeito não quantificável" if efeito is None else f"efeito de {efeito:.2f} % na conta".replace(".", ",")
            motivos.append(f"pendência ({quanto}): {p['texto']}")
    return ("amarelo" if motivos else "verde"), motivos


def estados(concelho: str, hoje=None) -> Dict[str, tuple]:
    """{serviço: (estado, motivos)} dos concelhos transcritos; {} se o concelho não tem tarifário transcrito."""
    d = carregar().get(concelho)
    p = (d or {}).get("procedencia")
    if not p:
        return {}
    out = {}
    for s in SERVICOS:
        docs = [x for x in p.get("documentos", []) if s in x.get("servicos", [])]
        pend = [x for x in p.get("pendencias", []) if s in x.get("servicos", SERVICOS)]
        transcrito = p.get("servicos", {}).get(s) == "transcrito"
        out[s] = avaliar_servico(docs, transcrito, bool(p.get("conferido")), pend, hoje)
    return out


def estado_do_concelho(por_servico: Dict[str, tuple]) -> str:
    """Verde só se todos os serviços forem verdes; cinza só se todos forem cinza; senão, amarelo."""
    ests = [e for e, _ in por_servico.values()]
    if not ests:
        return "cinza"
    if all(e == "verde" for e in ests):
        return "verde"
    if all(e == "cinza" for e in ests):
        return "cinza"
    return "amarelo"


def procedencia(concelho: str) -> str:
    """De onde vem o tarifário do concelho e quanto confiar nele, numa linha, para as telas.

    Vazio se o concelho não tem tarifário transcrito (ou fora da Edição Ibérica, onde não há o arquivo).
    """
    d = carregar().get(concelho)
    p = (d or {}).get("procedencia")
    if not p:
        return ""
    por = estados(concelho)
    ico = {"verde": "🟢", "amarelo": "🟡", "cinza": "⚪"}
    resumo = ", ".join(f"{ROTULO_DO_SERVICO[s]} {ico[e]}" for s, (e, _) in por.items())
    partes = [f"{ico[estado_do_concelho(por)]} {estado_do_concelho(por)}: {resumo}",
              f"documentos oficiais das entidades gestoras, vigência {d.get('vigencia', '--')}"]
    partes.append("conferido com as contas impressas" if p.get("conferido") else "SEM conferência com as contas impressas")
    verificados = [x for x in p.get("documentos", []) if x.get("verificado_por") in VERIFICACOES_INDEPENDENTES]
    if not verificados:
        partes.append("sem verificação independente (fatura real ou segunda leitura humana)")
    grandes = [x["texto"] for x in p.get("pendencias", [])
               if x.get("efeito_pct") is None or x["efeito_pct"] > LIMITE_DE_PENDENCIA_PCT]
    if grandes:
        partes.append(f"{len(grandes)} pendência(s) com efeito acima de 1 % por confirmar: " + "; ".join(grandes))
    if p.get("em_falta"):
        partes.append("em falta: " + "; ".join(p["em_falta"]))
    return "; ".join(partes)
