"""
Completa tarifas de municípios cuja base auditada só registrava a tarifa mínima.

Contexto
--------
A reconciliação com a base auditada (`reconciliar_tarifas.py`) reduziu de 43 para 7 os
municípios cuja conta de água não responde ao consumo. Os sete remanescentes não são
erro de conversão: a base auditada realmente só registra a tarifa mínima deles, sem
parcela volumétrica. Enquanto durarem assim, o Netuno calcula economia monetária nula
para qualquer sistema nesses municípios, por melhor que seja o desempenho hídrico.

Este script aplica tarifas obtidas em **fonte primária** — o sítio oficial do prestador
ou a resolução da agência reguladora — com a procedência registrada em cada entrada.

Critério de inclusão
--------------------
Só entra aqui o que foi lido diretamente da fonte oficial e cuja estrutura é
inequívoca. Municípios cuja tabela não pôde ser obtida por completo permanecem na lista
de pendências de `tests/unit/test_tariffs_structure.py`, e é assim que devem permanecer:
uma tarifa estimada é pior que uma tarifa ausente, porque a ausência é detectável e a
estimativa não.

Uso
---
    python scripts/completar_tarifas_faltantes.py --conferir
    python scripts/completar_tarifas_faltantes.py --aplicar
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

BANCO = RAIZ / "netuno" / "data" / "brazil_cities_tariffs.json"

FAIXA_PROGRESSIVA = 1
TAXA_FIXA = -1
FRANQUIA_MINIMA = -2


#: Tarifas obtidas em fonte primária, com procedência.
#:
#: Cada entrada traz as faixas no formato do catálogo — (mínimo m³, máximo m³, valor,
#: código) — e a documentação da origem. O campo ``observacao`` registra limitações
#: conhecidas da transcrição, para que não se tome por exato o que é aproximado.
TARIFAS_DE_FONTE_PRIMARIA = {
    ("MG", "Viçosa"): {
        "faixas": [
            [0.0, 5.0, 2.8170, FAIXA_PROGRESSIVA],
            [5.0, 10.0, 2.9296, FAIXA_PROGRESSIVA],
            [10.0, 15.0, 3.1388, FAIXA_PROGRESSIVA],
            [15.0, 20.0, 7.0343, FAIXA_PROGRESSIVA],
            [20.0, 40.0, 7.0343, FAIXA_PROGRESSIVA],
            [40.0, 60.0, 9.7387, FAIXA_PROGRESSIVA],
            [60.0, 300.0, 10.3342, FAIXA_PROGRESSIVA],
            [300.0, 999999.0, 10.9458, FAIXA_PROGRESSIVA],
        ],
        "fonte": "https://www.saaevicosa.mg.gov.br/pagina/89/tarifas",
        "ato": "Resolução ARIS-MG nº 227/2026",
        "consultado_em": "2026-09-08",
        "observacao": (
            "Tabela residencial completa, com oito faixas. A primeira faixa (2,8170) já "
            "constava do catálogo e confere com a fonte, o que corrobora a leitura das "
            "demais. A Tarifa Básica Operacional (TBO) de R$ 26,57 NÃO foi incluída: a "
            "documentação do SAAE a associa ao esgoto, e incluí-la como parcela fixa de "
            "água exigiria confirmação."
        ),
    },
    ("SP", "Bauru"): {
        "faixas": [
            [0.0, 6.0, 19.37, FRANQUIA_MINIMA],
            [6.0, 999999.0, 3.23, FAIXA_PROGRESSIVA],
        ],
        "fonte": "https://www.daebauru.sp.gov.br/conta_agua.php?item=CA1",
        "ato": "Resolução nº 02, de 11/02/2026",
        "consultado_em": "2026-09-08",
        "observacao": (
            "A franquia de R$ 19,37 até 6 m³ já constava do catálogo e confere com a "
            "fonte. A marginal de R$ 3,23/m³ é confirmada pelos degraus publicados "
            "(7 m³ = R$ 22,60; 8 m³ = R$ 25,82; 9 m³ = R$ 29,05), cujas diferenças são "
            "3,23, 3,22 e 3,23. ATENÇÃO: a tabela oficial segue por degraus até 100 m³ "
            "com valores crescentes, e apenas os primeiros foram lidos. A marginal "
            "constante adotada é, portanto, um PISO — subestima a conta em consumos "
            "altos, e com ela a economia. É conservadora, e melhor que a ausência "
            "anterior de qualquer parcela volumétrica, mas não é a tabela integral."
        ),
    },
}


def _normalizar(texto: str) -> str:
    import unicodedata

    sem_acento = "".join(
        c for c in unicodedata.normalize("NFKD", str(texto))
        if unicodedata.category(c) != "Mn"
    )
    return sem_acento.strip().lower()


def _localizar(cidades: dict, uf: str, municipio: str):
    chave_direta = f"{uf} - {municipio}"
    if chave_direta in cidades:
        return chave_direta
    alvo = (uf.upper(), _normalizar(municipio))
    for chave, dados in cidades.items():
        if (str(dados.get("uf", "")).upper(), _normalizar(dados.get("municipio", ""))) == alvo:
            return chave
    return None


def main() -> int:
    analisador = argparse.ArgumentParser(description=__doc__)
    grupo = analisador.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--conferir", action="store_true")
    grupo.add_argument("--aplicar", action="store_true")
    argumentos = analisador.parse_args()

    banco = json.loads(BANCO.read_text(encoding="utf-8"))
    cidades = banco["cities"]
    alteracoes = []

    for (uf, municipio), entrada in TARIFAS_DE_FONTE_PRIMARIA.items():
        chave = _localizar(cidades, uf, municipio)
        if chave is None:
            print(f"  {uf}/{municipio}: AUSENTE do catálogo")
            continue

        antes = cidades[chave].get("faixas")
        depois = entrada["faixas"]
        print(f"\n{uf}/{municipio}  ({entrada['ato']})")
        print(f"  antes  : {antes}")
        print(f"  depois : {depois}")
        print(f"  fonte  : {entrada['fonte']}")
        print(f"  nota   : {entrada['observacao'][:110]}...")

        if antes != depois:
            cidades[chave]["faixas"] = depois
            cidades[chave]["fonte_url"] = entrada["fonte"]
            cidades[chave]["vigencia_saneamento"] = entrada["ato"]
            cidades[chave]["procedencia_tarifa"] = {
                "fonte": entrada["fonte"],
                "ato": entrada["ato"],
                "consultado_em": entrada["consultado_em"],
                "observacao": entrada["observacao"],
            }
            alteracoes.append(chave)

    print(f"\n{len(alteracoes)} município(s) a alterar")

    if argumentos.aplicar and alteracoes:
        shutil.copy2(BANCO, BANCO.with_suffix(".json.bak"))
        banco["version"] = date.today().isoformat()
        BANCO.write_text(json.dumps(banco, ensure_ascii=False, indent=2),
                         encoding="utf-8", newline="")
        print(f"gravado em {BANCO.relative_to(RAIZ).as_posix()}")
    elif argumentos.conferir:
        print("nada gravado — use --aplicar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
