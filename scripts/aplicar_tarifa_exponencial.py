"""
Grava a fórmula exponencial da CORSAN nos municípios que ela atende.

Contexto
--------
A CORSAN não cobra a água por faixas: cobra ``PB × Cⁿ + Serviço Básico``, em que PB é
o preço-base do município, C o consumo do mês e n o expoente da **tabela
exponencial** para aquele consumo. A fórmula vale até 1.000 m³; acima disso, o
excedente é cobrado pelo preço do m³. O esgoto é um percentual do valor da água.

Até a versão 5.0.0 o catálogo gravava esses municípios como ``R$ 9,15/m³ + R$
43,39/mês``, uma reta. A reta só coincide com a fórmula quando n = 1. Este script
reescreve as faixas na forma exponencial, com os códigos de
`netuno/core/tariffs_structure.py`:

    [0, 0, SB, -1]          serviço básico
    [0, teto, PB, 2]        preço-base da fórmula
    [a, b, n, 3] ...        tabela exponencial, de 0 ao teto
    [teto, 999999, PB, 1]   excedente acima do teto

A tabela exponencial vem de um único arquivo, `tarifas/tabela_exponencial_corsan.json`,
porque é a mesma para todos os municípios: só o PB e o SB mudam. Corrigir a tabela ali
e rodar este script atualiza os 34 municípios de uma vez.

Uso
---
    python scripts/aplicar_tarifa_exponencial.py --conferir
    python scripts/aplicar_tarifa_exponencial.py --aplicar
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from netuno.core.tariff_regimes import EXPONENCIAL, validar_estrutura  # noqa: E402
from netuno.core.tariffs_structure import (  # noqa: E402
    EXPOENTE_DE_CONSUMO,
    FAIXA_PROGRESSIVA,
    PRECO_BASE_EXPONENCIAL,
    TAXA_FIXA_DE_DISPONIBILIDADE,
)

BANCO = RAIZ / "netuno" / "data" / "brazil_cities_tariffs.json"
TABELA = RAIZ / "tarifas" / "tabela_exponencial_corsan.json"
TETO_ABERTO = 999999.0


def carregar_tabela(caminho: Path = TABELA) -> dict:
    tabela = json.loads(caminho.read_text(encoding="utf-8"))
    expoentes = [[float(a), float(b), float(n)] for a, b, n in tabela["expoentes"]]
    teto = float(tabela["teto_exponencial_m3"])
    if expoentes[0][0] != 0.0 or expoentes[-1][1] < teto:
        raise ValueError("a tabela exponencial precisa cobrir de 0 ao teto da fórmula")
    return dict(tabela, expoentes=expoentes, teto_exponencial_m3=teto)


def atendido_pela_corsan(dados: dict) -> bool:
    return "CORSAN" in str(dados.get("prestador_saneamento", "")).upper()


def preco_base_e_servico_basico(faixas: list) -> tuple[float, float]:
    """Lê PB e SB tanto da forma linear antiga quanto da exponencial."""
    base = [f for f in faixas if int(f[3]) == PRECO_BASE_EXPONENCIAL]
    if base:
        pb = float(base[0][2])
    else:
        progressivas = [f for f in faixas if int(f[3]) == FAIXA_PROGRESSIVA]
        if len(progressivas) != 1:
            raise ValueError(f"forma linear esperada, com uma faixa: {faixas}")
        pb = float(progressivas[0][2])
    sb = sum(float(f[2]) for f in faixas if int(f[3]) == TAXA_FIXA_DE_DISPONIBILIDADE)
    return pb, sb


def _real(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def faixas_exponenciais(pb: float, sb: float, tabela: dict) -> list:
    teto = tabela["teto_exponencial_m3"]
    faixas = [[0.0, 0.0, sb, TAXA_FIXA_DE_DISPONIBILIDADE],
              [0.0, teto, pb, PRECO_BASE_EXPONENCIAL]]
    faixas += [[a, b, n, EXPOENTE_DE_CONSUMO] for a, b, n in tabela["expoentes"]]
    faixas.append([teto, TETO_ABERTO, pb, FAIXA_PROGRESSIVA])
    return faixas


def descricao(pb: float, sb: float, tabela: dict) -> str:
    teto = f"{tabela['teto_exponencial_m3']:,.0f}".replace(",", ".")
    return (f"Fórmula exponencial: PB × Cⁿ + serviço básico; PB R$ {_real(pb)}/m³, "
            f"serviço básico R$ {_real(sb)}/mês, n pela tabela exponencial até "
            f"{teto} m³; acima, R$ {_real(pb)}/m³")


def aplicar(cidades: dict, tabela: dict) -> list[str]:
    alteradas = []
    for chave, dados in cidades.items():
        if not atendido_pela_corsan(dados):
            continue
        pb, sb = preco_base_e_servico_basico(dados["faixas"])
        dados["faixas"] = faixas_exponenciais(pb, sb, tabela)
        dados["faixas_desc"] = descricao(pb, sb, tabela)
        dados["regime_tarifario"] = EXPONENCIAL
        dados["consumo_minimo_faturado_m3"] = 0.0
        dados["expoentes_verificados"] = bool(tabela.get("verificada"))
        dados["expoentes_fonte"] = tabela.get("fonte", "")
        erros = [a for a in validar_estrutura(dados) if a.gravidade == "erro"]
        if erros:
            raise ValueError(f"{chave}: {erros}")
        alteradas.append(chave)
    return alteradas


def main() -> int:
    analisador = argparse.ArgumentParser(description=__doc__)
    grupo = analisador.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--conferir", action="store_true", help="apenas relata, não grava")
    grupo.add_argument("--aplicar", action="store_true", help="grava o banco tarifário")
    argumentos = analisador.parse_args()

    tabela = carregar_tabela()
    banco = json.loads(BANCO.read_text(encoding="utf-8"))
    alteradas = aplicar(banco["cities"], tabela)
    print(f"municípios da CORSAN na fórmula exponencial: {len(alteradas)}")
    print(f"tabela exponencial verificada: {'sim' if tabela.get('verificada') else 'NÃO'}"
          f" ({len(tabela['expoentes'])} linhas)")
    if argumentos.aplicar:
        BANCO.write_text(json.dumps(banco, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"gravado: {BANCO.relative_to(RAIZ).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
