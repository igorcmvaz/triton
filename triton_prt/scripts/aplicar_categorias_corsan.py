"""
Grava as categorias Comercial, Pública e Industrial da CORSAN, a partir das tabelas oficiais.

Até a 1.0.0 a comercial era a residencial vezes 1,85, sem fonte. Aqui cada categoria sai
da Tabela I da tabela tarifária do município, transcrita em
`tarifas/categorias/corsan_2026.json` com o documento e a vigência: preço-base, serviço
básico e esgoto tratado por m³, e o expoente da coluna da categoria na Tabela de
Exponenciais. A Industrial tem teto de 1.000 m³ na fórmula, com o excedente pelos preços
da Tabela IX, que só o ANEXO-5 traz; nas outras tabelas ela fica de fora.

Os municípios de cada tabela são os do catálogo cujo PB residencial é o da tabela, a
mesma chave de `scripts/aplicar_tarifa_exponencial.py`.

Uso
---
    python scripts/aplicar_categorias_corsan.py --conferir
    python scripts/aplicar_categorias_corsan.py --aplicar
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
for _p in (RAIZ, RAIZ / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from aplicar_tarifa_exponencial import (  # noqa: E402
    BANCO, TETO_ABERTO, _real, atendido_pela_corsan, carregar_tabela, expoentes,
    preco_base_e_servico_basico,
)
from triton.core.tariff_regimes import EXPONENCIAL, validar_estrutura  # noqa: E402
from triton.core.tariffs_structure import (  # noqa: E402
    ESGOTO_POR_M3, EXPOENTE_DE_CONSUMO, FAIXA_PROGRESSIVA, PRECO_BASE_EXPONENCIAL,
    TAXA_FIXA_DE_DISPONIBILIDADE,
)

TRANSCRICAO = RAIZ / "tarifas" / "categorias" / "corsan_2026.json"


def faixas_da_categoria(cat: dict, tabela_exp: dict) -> list:
    excedente = cat.get("excedente_tabela_ix") or []
    teto = float(excedente[0][0]) if excedente else TETO_ABERTO
    faixas = [[0.0, 0.0, float(cat["sb"]), TAXA_FIXA_DE_DISPONIBILIDADE],
              [0.0, teto, float(cat["pb"]), PRECO_BASE_EXPONENCIAL]]
    for a, b, n in expoentes(tabela_exp, cat["coluna"]):
        if a >= teto:
            break
        faixas.append([a, min(b, teto), n, EXPOENTE_DE_CONSUMO])
    faixas += [[float(a), float(b), float(p), FAIXA_PROGRESSIVA] for a, b, p in excedente]
    return faixas


def registro(cat_id: str, cat: dict, tabela: dict, tabela_exp: dict) -> dict:
    texto = (f"Fórmula exponencial, categoria {cat_id}: PB R$ {_real(cat['pb'])}/m³, serviço básico "
             f"R$ {_real(cat['sb'])}/mês, expoente da coluna {cat['coluna']}; esgoto tratado "
             f"R$ {_real(cat['esgoto_tratado_m3'])}/m³ consumido")
    if cat.get("excedente_tabela_ix"):
        texto += "; acima de 1.000 m³, preços da Tabela IX sem expoente"
    return {
        "faixas": faixas_da_categoria(cat, tabela_exp),
        "faixas_desc": texto,
        "tarifa_fixa_mensal": float(cat["sb"]),
        "regime_tarifario": EXPONENCIAL,
        "consumo_minimo_faturado_m3": 0.0,
        "esgoto_modo": ESGOTO_POR_M3,
        "esgoto_r_m3": float(cat["esgoto_tratado_m3"]),
        "esgoto_fonte": f"{tabela['documento']}, Tabela I, esgoto tratado",
        "fonte_url": tabela["fonte_url"],
        "fonte_documento": tabela["documento"],
        "vigencia_saneamento": tabela["vigencia"],
        "expoentes_verificados": bool(tabela_exp.get("verificada")),
    }


def aplicar(cidades: dict, transcricao: dict, tabela_exp: dict) -> dict:
    por_pb = {round(t["pb_residencial"], 2): t for t in transcricao["tabelas"]}
    contagem: dict = {}
    for chave, dados in cidades.items():
        if not atendido_pela_corsan(dados):
            continue
        pb, _sb = preco_base_e_servico_basico(dados["faixas"])
        tabela = por_pb.get(round(pb, 2))
        if tabela is None:
            raise ValueError(f"{chave}: PB residencial {pb} sem tabela transcrita")
        categorias = {}
        for cat_id, cat in tabela["categorias"].items():
            novo = registro(cat_id, cat, tabela, tabela_exp)
            erros = [a for a in validar_estrutura(dict(dados, **novo)) if a.gravidade == "erro"]
            if erros:
                raise ValueError(f"{chave} {cat_id}: {erros}")
            categorias[cat_id] = novo
            contagem[cat_id] = contagem.get(cat_id, 0) + 1
        dados["categorias"] = categorias
    return contagem


def main() -> int:
    analisador = argparse.ArgumentParser(description=__doc__)
    grupo = analisador.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--conferir", action="store_true")
    grupo.add_argument("--aplicar", action="store_true")
    argumentos = analisador.parse_args()
    banco = json.loads(BANCO.read_text(encoding="utf-8"))
    contagem = aplicar(banco["cities"], json.loads(TRANSCRICAO.read_text(encoding="utf-8")),
                       carregar_tabela())
    for cat, n in sorted(contagem.items()):
        print(f"  {cat}: {n} municípios")
    if argumentos.aplicar:
        BANCO.write_text(json.dumps(banco, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"gravado: {BANCO.relative_to(RAIZ).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
