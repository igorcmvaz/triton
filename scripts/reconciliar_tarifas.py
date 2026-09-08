"""
Reconcilia o banco tarifário com a base auditada, corrigindo a primeira faixa.

Problema
--------
Existiam duas cópias divergentes de `brazil_cities_tariffs.json`:

- ``data/tarifas/`` (versão 2026-08-31) — a que o programa carrega. Tem a tarifa da
  **primeira** faixa progressiva zerada em 464 das 652 cidades.
- ``netuno/data/`` (versão 2026.08.24) — a do pacote. Nenhuma faixa zerada.

Nenhuma das duas está inteiramente certa, porque a primeira faixa tem dois significados
diferentes conforme o prestador:

1. **Faixa coberta pela tarifa mínima.** O prestador cobra um valor fixo que já dá
   direito a um consumo inicial (ex.: SANEACRE, 0–15 m³ por R$ 38,37). Aqui a tarifa
   por m³ da primeira faixa deve ser **zero** — a parcela fixa já a cobra. A cópia do
   pacote guardava ``fixa ÷ largura``, o que somado à parcela fixa **cobrava em dobro**.

2. **Faixa com tarifa volumétrica própria.** O prestador cobra por m³ desde o início,
   além de eventual parcela fixa (ex.: COPASA em Belo Horizonte, R$ 2,69/m³ de 0 a 5 m³;
   CORSAN, preço-base de R$ 9,15/m³ mais serviço básico). Aqui zerar **perde tarifa
   real**, e foi o que a cópia carregada fez.

Critério de correção
--------------------
A distinção não é aritmética: é documental. Vem de `tarifas/tarifas_detalhadas_auditadas.csv`,
a base auditada com procedência e grau de confiança por município:

- ``tarifa_agua_r_m3`` preenchida na primeira faixa  → tarifa volumétrica genuína, restaurar.
- apenas ``tarifa_agua_fixa_minima_r`` preenchida     → faixa coberta pelo mínimo, manter zero.

Uso
---
    python scripts/reconciliar_tarifas.py --conferir   # relatório, não grava
    python scripts/reconciliar_tarifas.py --aplicar    # grava as duas cópias
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

BASE_AUDITADA = RAIZ / "tarifas" / "tarifas_detalhadas_auditadas.csv"
# Cópia única do banco tarifário, dentro do pacote (ver tariffs_database._find_database_file).
COPIAS = [
    RAIZ / "netuno" / "data" / "brazil_cities_tariffs.json",
]

FAIXA_PROGRESSIVA = 1
TAXA_FIXA = -1
FRANQUIA_MINIMA = -2

#: Parcela fixa declarada na base auditada, por município. Preenchido por
#: `carregar_referencia_auditada`.
_FIXA_AUDITADA: dict = {}

#: Menor tarifa por m³ declarada, usada em estruturas de franquia.
_TAXA_ACIMA_DA_FRANQUIA: dict = {}


def _normalizar(texto: str) -> str:
    sem_acento = "".join(
        c for c in unicodedata.normalize("NFKD", str(texto))
        if unicodedata.category(c) != "Mn"
    )
    return sem_acento.strip().lower()


def _limite_inferior(descricao_da_faixa) -> int | None:
    """Extrai o limite inferior de uma descrição de faixa, em m³.

    Aceita as formas presentes na base: ``0–5 m³``, ``>5–10 m³``, ``1 a 10 m³``,
    ``>50 m³``. Devolve ``None`` para rótulos sem faixa numérica —
    ``Tarifa fixa``, ``Tarifa básica``, ``Preço-base (fórmula exponencial)``.
    """
    texto = str(descricao_da_faixa).replace("–", "-").replace(">", "").strip()
    # "Até 5 m³" (SANEPAR) descreve a faixa inicial, de 0 a 5 m³.
    if texto.lower().startswith(("até", "ate")):
        return 0
    correspondencia = re.match(r"(\d+)", texto)
    return int(correspondencia.group(1)) if correspondencia else None


def carregar_referencia_auditada() -> dict:
    """Mapeia (uf, município) → tarifa volumétrica da primeira faixa, ou None.

    ``None`` significa que a base auditada não registra tarifa por m³ para a menor
    faixa de consumo — ou seja, essa faixa é coberta pela tarifa mínima e cobrá-la
    novamente por m³ duplicaria a conta.

    A escolha da linha é explícita, e não pela ordem do arquivo: em 65 municípios a
    primeira linha é o rótulo ``Tarifa fixa``/``Tarifa básica``, não a menor faixa,
    e lê-la levaria a zerar tarifas volumétricas legítimas (o caso de Goiânia,
    Brasília e Campo Grande).
    """
    df = pd.read_csv(BASE_AUDITADA, encoding="utf-8-sig", low_memory=False)
    referencia: dict[tuple[str, str], float | None] = {}

    for (uf, municipio), grupo in df.groupby(["uf", "municipio"], sort=False):
        chave = (str(uf).strip().upper(), _normalizar(municipio))
        _FIXA_AUDITADA[chave] = max(
            [float(v) for v in grupo["tarifa_agua_fixa_minima_r"] if pd.notna(v)] or [0.0]
        )

        com_faixa_numerica = [
            (_limite_inferior(linha["faixa_consumo_m3"]), linha)
            for _, linha in grupo.iterrows()
        ]
        numericas = [(limite, linha) for limite, linha in com_faixa_numerica if limite is not None]

        if numericas:
            menor_limite = min(limite for limite, _ in numericas)
            empatadas = [linha for limite, linha in numericas if limite == menor_limite]

            taxas_distintas = {
                round(float(linha["tarifa_agua_r_m3"]), 4)
                for linha in empatadas
                if pd.notna(linha.get("tarifa_agua_r_m3"))
            }
            if len(empatadas) > 1 and len(taxas_distintas) > 1:
                # Duas tabelas concorrentes para a mesma faixa (ES/Aracruz declara
                # "SAAE Aracruz / CESAN conforme área"). Escolher uma seria arbitrar
                # sobre qual concessionária atende o imóvel; a cidade fica intocada
                # e é reportada para decisão humana.
                referencia[chave] = "ambiguo"
                continue

            linha_escolhida = empatadas[0]
        else:
            # Sem faixa numérica: estruturas como o preço-base da CORSAN, em que a
            # tarifa volumétrica existe mas não é descrita por intervalo de consumo.
            com_tarifa = [
                linha for _, linha in grupo.iterrows()
                if pd.notna(linha.get("tarifa_agua_r_m3"))
            ]
            if not com_tarifa:
                referencia[chave] = None
                continue
            linha_escolhida = com_tarifa[0]

        taxa = linha_escolhida.get("tarifa_agua_r_m3")
        referencia[chave] = float(taxa) if pd.notna(taxa) and float(taxa) > 0 else None

        # Municípios com franquia de consumo mínimo têm a faixa volumétrica declarada
        # acima da franquia (ex.: DAE Americana, "0–6 m³" mínimo e ">6 m³" a R$ 3,49).
        # Guarda-se a menor faixa com tarifa por m³ para uso nesses casos.
        com_tarifa_por_m3 = [
            (limite, linha) for limite, linha in numericas
            if pd.notna(linha.get("tarifa_agua_r_m3")) and float(linha["tarifa_agua_r_m3"]) > 0
        ] if numericas else []
        if com_tarifa_por_m3:
            _, linha_acima = min(com_tarifa_por_m3, key=lambda item: item[0])
            _TAXA_ACIMA_DA_FRANQUIA[chave] = float(linha_acima["tarifa_agua_r_m3"])

    return referencia


def reconciliar(cidades: dict, referencia: dict) -> tuple[dict, list, list, list]:
    """Corrige a primeira faixa progressiva de cada cidade. Devolve as mudanças."""
    restauradas, mantidas_zero, sem_referencia, ambiguas, fixas_corrigidas = [], [], [], [], []

    for chave_cidade, dados in cidades.items():
        faixas = dados.get("faixas") or []
        indices_progressivas = [i for i, f in enumerate(faixas) if int(f[3]) == FAIXA_PROGRESSIVA]
        if not indices_progressivas:
            continue

        indice = indices_progressivas[0]
        atual = float(faixas[indice][2])
        chave = (str(dados.get("uf", "")).strip().upper(), _normalizar(dados.get("municipio", "")))

        if chave not in referencia:
            sem_referencia.append(chave_cidade)
            continue

        esperada = referencia[chave]
        if esperada == "ambiguo":
            ambiguas.append(chave_cidade)
            continue

        if any(int(f[3]) == FRANQUIA_MINIMA for f in faixas):
            # A faixa progressiva de um município com franquia cobre o consumo ACIMA
            # dela; a tarifa aplicável é a da menor faixa volumétrica declarada.
            alvo = _TAXA_ACIMA_DA_FRANQUIA.get(chave, 0.0)
        else:
            alvo = esperada if esperada is not None else 0.0

        if abs(atual - alvo) > 1e-6:
            faixas[indice][2] = alvo
            if alvo > 0:
                restauradas.append((chave_cidade, atual, alvo))
            else:
                mantidas_zero.append((chave_cidade, atual, alvo))

        # Parcela fixa: só é reconciliada quando o município não usa a franquia de
        # consumo mínimo, cujo valor fixo vive na própria faixa -2 e não numa taxa
        # de disponibilidade separada.
        usa_franquia = any(int(f[3]) == FRANQUIA_MINIMA for f in faixas)
        fixa_esperada = _FIXA_AUDITADA.get(chave)
        if not usa_franquia and fixa_esperada is not None:
            indices_fixas = [i for i, f in enumerate(faixas) if int(f[3]) == TAXA_FIXA]
            fixa_atual = sum(float(faixas[i][2]) for i in indices_fixas)
            if abs(fixa_atual - fixa_esperada) > 0.02:
                if fixa_esperada <= 0 and indices_fixas:
                    for i in sorted(indices_fixas, reverse=True):
                        faixas.pop(i)
                elif indices_fixas:
                    faixas[indices_fixas[0]][2] = fixa_esperada
                    for i in sorted(indices_fixas[1:], reverse=True):
                        faixas.pop(i)
                else:
                    faixas.insert(0, [0.0, 0.0, fixa_esperada, TAXA_FIXA])
                fixas_corrigidas.append((chave_cidade, fixa_atual, fixa_esperada))

    return cidades, restauradas, mantidas_zero, sem_referencia, ambiguas, fixas_corrigidas


def main() -> int:
    analisador = argparse.ArgumentParser(description=__doc__)
    grupo = analisador.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--conferir", action="store_true", help="apenas relata, não grava")
    grupo.add_argument("--aplicar", action="store_true", help="grava as duas cópias")
    argumentos = analisador.parse_args()

    referencia = carregar_referencia_auditada()
    print(f"base auditada: {len(referencia)} municípios")
    com_volumetrica = sum(1 for v in referencia.values() if isinstance(v, float))
    print(f"  com tarifa volumétrica na 1ª faixa : {com_volumetrica}")
    print(f"  cobertos pela tarifa mínima        : {len(referencia) - com_volumetrica}\n")

    for caminho in COPIAS:
        if not caminho.exists():
            print(f"AUSENTE: {caminho}")
            continue

        banco = json.loads(caminho.read_text(encoding="utf-8"))
        _, restauradas, zeradas, sem_ref, ambiguas, fixas = reconciliar(banco["cities"], referencia)

        rotulo = caminho.relative_to(RAIZ).as_posix()
        print(f"--- {rotulo}")
        print(f"    tarifas restauradas (estavam zeradas indevidamente) : {len(restauradas)}")
        print(f"    tarifas zeradas (a parcela fixa já as cobria)       : {len(zeradas)}")
        print(f"    parcelas fixas corrigidas                           : {len(fixas)}")
        for chave, antes, depois in fixas:
            print(f"       {chave}: fixa {antes:.2f} -> {depois:.2f}")
        print(f"    sem correspondência na base auditada                : {len(sem_ref)}")
        if ambiguas:
            print(f"    NÃO alteradas por ambiguidade na base auditada      : {len(ambiguas)}")
            for chave in ambiguas:
                print(f"       {chave}")
        for chave, antes, depois in restauradas[:3]:
            print(f"       {chave}: {antes} -> {depois}")

        if argumentos.aplicar and (restauradas or zeradas or fixas):
            backup = caminho.with_suffix(".json.bak")
            shutil.copy2(caminho, backup)
            banco["version"] = date.today().isoformat()
            banco["reconciliacao"] = {
                "data": date.today().isoformat(),
                "fonte": "tarifas/tarifas_detalhadas_auditadas.csv",
                "primeira_faixa_restaurada": len(restauradas),
                "primeira_faixa_zerada": len(zeradas),
            }
            caminho.write_text(
                json.dumps(banco, ensure_ascii=False, indent=2), encoding="utf-8", newline=""
            )
            print(f"    gravado (backup em {backup.name})")
        print()

    if argumentos.conferir:
        print("nada foi gravado — use --aplicar para efetivar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
