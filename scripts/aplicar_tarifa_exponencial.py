"""
Grava a fórmula exponencial da CORSAN nos municípios que ela atende.

Contexto
--------
A CORSAN não cobra a água por faixas: cobra ``PB × Cⁿ + SB``, em que PB é o preço-base
do município, C o consumo do mês, n o expoente da **Tabela de Exponenciais** para
aquele consumo e SB o serviço básico. O expoente é lido pelo consumo total e vale
para todo o volume: 1,00 até 20 m³, subindo a 1,13 entre 101 e 150 m³ na categoria
residencial. Só a categoria industrial tem teto (1.000 m³, Tabela IX); nas demais a
tabela segue até 9.001 m³ e além.

O esgoto é cobrado **por m³ do consumo** («de acordo com o consumo», nas tabelas
tarifárias), sem o serviço básico e sem o expoente: R$ 6,40/m³ tratado para o PB de
R$ 9,15 do ANEXO-5. É 70% do PB, truncado no centavo.

Até a 5.0.0 o catálogo gravava esses municípios como uma reta, ``R$ 9,15/m³ + R$
43,39/mês``, com esgoto de 70% sobre a conta inteira, inclusive sobre o serviço
básico. Este script reescreve as faixas com os códigos de
`netuno/core/tariffs_structure.py`:

    [0, 0, SB, -1]          serviço básico
    [0, teto, PB, 2]        preço-base da fórmula
    [a, b, n, 3] ...        tabela de expoentes, cada linha para o consumo em (a, b]
    [teto, 999999, p, 1]    excedente acima do teto, só se houver teto

A tabela vem de um único arquivo, `tarifas/tabela_exponencial_corsan.json`, porque é a
mesma para todos os municípios: só o PB, o SB e o preço do esgoto mudam.

Uso
---
    python scripts/aplicar_tarifa_exponencial.py --conferir
    python scripts/aplicar_tarifa_exponencial.py --aplicar
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from netuno.core.tariff_regimes import EXPONENCIAL, validar_estrutura  # noqa: E402
from netuno.core.tariffs_structure import (  # noqa: E402
    ESGOTO_POR_M3,
    EXPOENTE_DE_CONSUMO,
    FAIXA_PROGRESSIVA,
    PRECO_BASE_EXPONENCIAL,
    TAXA_FIXA_DE_DISPONIBILIDADE,
)

BANCO = RAIZ / "netuno" / "data" / "brazil_cities_tariffs.json"
TABELA = RAIZ / "tarifas" / "tabela_exponencial_corsan.json"
TETO_ABERTO = 999999.0

#: Preço do esgoto tratado por m³, lido de cada tabela tarifária, pelo preço-base.
#: O PB de R$ 8,68 é o de Canoas e Esteio (ANEXO-3): PB 8,68, serviço básico 41,20 e
#: esgoto tratado 6,07/m³ na categoria Residencial B, como na base.
ESGOTO_TRATADO_R_M3 = {
    9.15: (6.40, "ANEXO-5, vigência 01/07/2026"),
    6.95: (4.86, "Tabela tarifária de Erechim, vigência 01/01/2026"),
    7.91: (5.53, "Tabela tarifária de Santa Cruz do Sul, vigência 01/01/2026"),
    8.68: (6.07, "ANEXO-3 (Canoas e Esteio), vigência 01/07/2026"),
}


def carregar_tabela(caminho: Path = TABELA) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8"))


def expoentes(tabela: dict, coluna: str | None = None) -> list[list[float]]:
    """A coluna da tabela como faixas ``(a, b]`` de consumo contínuo.

    A linha «31» vale de 31 a 35 m³ inteiros, isto é, para o consumo em (30, 35].
    A primeira começa em 0 e a última, sem linha seguinte, segue até o teto aberto.
    Linhas seguidas com o mesmo expoente viram uma faixa: de 1 a 20 m³, n = 1,00.
    """
    coluna = coluna or tabela["coluna_aplicada"]
    indice = tabela["colunas"].index(coluna)
    linhas = [(int(l[0]), l[indice]) for l in tabela["linhas"] if l[indice] is not None]
    faixas: list[list[float]] = []
    for i, (inicio, n) in enumerate(linhas):
        de = 0.0 if i == 0 else float(inicio - 1)
        ate = float(linhas[i + 1][0] - 1) if i + 1 < len(linhas) else TETO_ABERTO
        if faixas and faixas[-1][2] == float(n):
            faixas[-1][1] = ate  # mesmo expoente: uma faixa só, a conta é a mesma
        else:
            faixas.append([de, ate, float(n)])
    return faixas


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


def esgoto_por_m3(pb: float) -> tuple[float, str]:
    if pb in ESGOTO_TRATADO_R_M3:
        return ESGOTO_TRATADO_R_M3[pb]
    return math.floor(pb * 70.0) / 100.0, "70% do PB truncado no centavo"


def _real(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def faixas_exponenciais(pb: float, sb: float, tabela: dict) -> list:
    return ([[0.0, 0.0, sb, TAXA_FIXA_DE_DISPONIBILIDADE],
             [0.0, TETO_ABERTO, pb, PRECO_BASE_EXPONENCIAL]]
            + [[a, b, n, EXPOENTE_DE_CONSUMO] for a, b, n in expoentes(tabela)])


def descricao(pb: float, sb: float, esgoto: float) -> str:
    return (f"Fórmula exponencial: PB × Cⁿ + serviço básico; PB R$ {_real(pb)}/m³, serviço "
            f"básico R$ {_real(sb)}/mês, n de 1,00 (até 20 m³) a 1,13 (101 a 150 m³) pela "
            f"Tabela de Exponenciais; esgoto tratado R$ {_real(esgoto)}/m³ consumido")


def aplicar(cidades: dict, tabela: dict) -> list[str]:
    alteradas = []
    for chave, dados in cidades.items():
        if not atendido_pela_corsan(dados):
            continue
        pb, sb = preco_base_e_servico_basico(dados["faixas"])
        esgoto, origem = esgoto_por_m3(pb)
        dados["faixas"] = faixas_exponenciais(pb, sb, tabela)
        dados["faixas_desc"] = descricao(pb, sb, esgoto)
        dados["regime_tarifario"] = EXPONENCIAL
        dados["consumo_minimo_faturado_m3"] = 0.0
        dados["esgoto_modo"] = ESGOTO_POR_M3
        dados["esgoto_r_m3"] = esgoto
        dados["esgoto_fonte"] = origem
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
    print(f"tabela de expoentes: coluna {tabela['coluna_aplicada']}, "
          f"{len(expoentes(tabela))} faixas, verificada: {'sim' if tabela.get('verificada') else 'NÃO'}")
    if argumentos.aplicar:
        BANCO.write_text(json.dumps(banco, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"gravado: {BANCO.relative_to(RAIZ).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
