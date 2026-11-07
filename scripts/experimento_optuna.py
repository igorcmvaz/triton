# -*- coding: utf-8 -*-
"""Compara a busca em grade do Triton com a busca bayesiana do optuna (experimento de desenvolvimento, opcional).

Uso (da raiz do monorepo, com o extra ``otimizacao``: ``pip install "triton-int[otimizacao]"`` ou ``pip install optuna``):

    python scripts/experimento_optuna.py --help
    python scripts/experimento_optuna.py                       # a edição de TRITON_EDITION (ou a Brasil), todos os experimentos
    python scripts/experimento_optuna.py --edicao ibe --experimento 1d --experimento 2d
    python scripts/experimento_optuna.py --edicao brl --json auditoria/iniciativas/resultado_brl.json

O mesmo problema vai para os dois métodos. Por edição: Brasil, o arquétipo comercial de Santa Catarina
(``triton_brl/estudos/santa-catarina/comercial/comercial.triton``); Ibérica, ``triton_ibe/examples/portugal/lisboa.triton``;
Internacional, ``triton_int/examples/london.triton``. Experimentos:

    1d    varredura do volume do reservatório inferior na grade do projeto (a do ``estudo run`` de hoje)
    1da   a mesma varredura ampliada 5 vezes (40 pontos, o máximo da varredura), onde o ótimo deixa a borda
    2d    volume (grade ampliada) × área de captação (29 valores, de 0,25 a 2 vezes a do projeto)
    nsga  o par «água pluvial aproveitada (maximizar) × custo de implantação (minimizar)» na grade do 2d, com NSGA-II

A grade é a verdade: ``cli.run_analysis`` com varredura (o caminho do ``estudo run``). O optuna usa
``_run_technical`` (``run_single_simulation``) e ``_economic_row`` em cada tentativa e, ao fim, o melhor ponto é
REAVALIADO por outra via (a varredura oficial sobre uma cópia nova do projeto). Reprodutível: ``TPESampler``,
``RandomSampler`` e ``NSGAIISampler`` com semente, ``n_jobs=1``, armazenamento em memória (sem SQLite). Só os tempos variam
de uma execução para outra. O optuna é importado por ``triton.core._opcional`` e nunca entra no programa nem no instalador.
"""
from __future__ import annotations

import argparse
import copy
import io
import contextlib
import json
import os
import platform
import statistics
import sys
import time
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

RAIZ = Path(__file__).resolve().parents[1]
EDICOES = ("brl", "int", "ibe")
EXPERIMENTOS = ("1d", "1da", "2d", "nsga")
PROBLEMAS: Dict[str, Tuple[str, str]] = {
    "brl": ("triton_brl/estudos/santa-catarina/comercial/comercial.triton",
            "arquétipo comercial de Santa Catarina (Florianópolis, CLIMBra INM-CM4, histórico 1981-2010)"),
    "ibe": ("triton_ibe/examples/portugal/lisboa.triton", "exemplo de Lisboa da edição Ibérica"),
    "int": ("triton_int/examples/london.triton", "exemplo de Londres da edição Internacional"),
}
FATOR_DA_GRADE_AMPLIADA = 5            # a grade ampliada vai até 5 vezes o volume máximo do projeto
FATORES_DE_AREA = tuple(0.25 + 0.0625 * k for k in range(29))   # 0,25 ... 2,00 vezes a área do projeto (29 valores)
SEMENTE_BASE = 42


def _configurar_saida() -> None:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            try:
                fluxo.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def montar_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="experimento_optuna.py", formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Compara a busca em grade do Triton com a busca bayesiana do optuna no mesmo problema "
                    "(extra opcional «otimizacao»; só para desenvolvimento).",
        epilog="Os resultados da busca bayesiana são sempre reavaliados no motor determinístico do Triton.")
    ap.add_argument("--edicao", choices=EDICOES, default=None,
                    help="edição a usar (padrão: a variável TRITON_EDITION; sem ela, brl)")
    ap.add_argument("--projeto", type=Path, default=None, help="outro projeto .triton em vez do problema padrão da edição")
    ap.add_argument("--experimento", action="append", choices=EXPERIMENTOS, default=None,
                    help="experimento a rodar; repita a opção para mais de um (padrão: todos)")
    ap.add_argument("--semente", type=int, default=SEMENTE_BASE, help="primeira semente (padrão: %(default)s)")
    ap.add_argument("--n-sementes", type=int, default=5, help="quantas sementes consecutivas (padrão: %(default)s)")
    ap.add_argument("--tentativas-1d", type=int, default=60, help="orçamento de tentativas nos experimentos 1d e 1da (padrão: %(default)s)")
    ap.add_argument("--tentativas-2d", type=int, default=300, help="orçamento de tentativas no experimento 2d (padrão: %(default)s)")
    ap.add_argument("--tentativas-nsga", type=int, default=400, help="orçamento de tentativas no experimento nsga (padrão: %(default)s)")
    ap.add_argument("--populacao", type=int, default=30, help="tamanho da população do NSGA-II (padrão: %(default)s)")
    ap.add_argument("--tolerancia-pct", type=float, default=1.0,
                    help="tolerância do «mesmo resultado em classe», em %% do VPL ótimo da grade (padrão: %(default)s)")
    ap.add_argument("--repeticoes-de-tempo", type=int, default=5,
                    help="repetições da grade para medir o tempo, depois de aquecida (padrão: %(default)s)")
    ap.add_argument("--repeticoes-do-estudo", type=int, default=5,
                    help="quantas vezes repetir cada estudo (mesma semente) para medir o tempo; vale o mais rápido e as "
                         "trajetórias têm de sair idênticas (padrão: %(default)s)")
    ap.add_argument("--aguardar-cpu", action=argparse.BooleanOptionalAction, default=False,
                    help="antes de cada medida de tempo, espera (até 8 s) a CPU voltar ao desempenho inicial (padrão: desligado; "
                         "o custo em «grades» já compensa a variação de desempenho)")
    ap.add_argument("--json", type=Path, default=None, help="grava os resultados brutos neste arquivo JSON")
    return ap


def preparar_edicao(edicao: str) -> Any:
    """Põe a pasta da edição no ``sys.path``, fixa ``TRITON_EDITION`` e devolve o módulo ``triton.core._opcional``."""
    os.environ["TRITON_EDITION"] = edicao
    pasta = str(RAIZ / f"triton_{edicao}")
    if pasta not in sys.path:
        sys.path.insert(0, pasta)
    from triton.core import _opcional
    return _opcional


def exigir_optuna(opcional: Any) -> Any:
    """Importa o optuna pelo ``_opcional``; sem ele, sai com a mensagem de instalação do extra ``otimizacao``."""
    try:
        return opcional.importar("optuna", "otimizacao", "comparar a busca em grade com a busca bayesiana")
    except opcional.PacoteOpcionalAusente as erro:
        sys.exit(f"erro: {erro}")


# ---------------------------------------------------------------------------------------------------------------------
# Calibração da CPU: máquinas portáteis (ou ambientes com limite de CPU) reduzem o desempenho depois de alguns segundos de
# carga contínua. Sem cuidado, o método medido por último parece mais lento. Antes de cada bloco cronometrado, o script espera
# a CPU voltar ao desempenho do início (um laço de ~30 ms serve de régua) e anota a régua ao fim do bloco.
# ---------------------------------------------------------------------------------------------------------------------
class Calma:
    """Régua de desempenho da CPU: ``aguardar`` espera o desempenho de partida; ``razao`` é o desempenho atual (1 = partida)."""

    def __init__(self, ativa: bool, espera_maxima_s: float = 8.0) -> None:
        self.ativa, self.espera_maxima_s = ativa, espera_maxima_s
        self.referencia = min(self._laco() for _ in range(7)) if ativa else 0.0
        self.esperas_s = 0.0
        self.razoes_no_fim: List[float] = []

    @staticmethod
    def _laco() -> float:
        t0, soma = time.perf_counter(), 0
        for i in range(1_000_000):
            soma += i * i
        return time.perf_counter() - t0

    def razao(self) -> float:
        return min(self._laco() for _ in range(2)) / self.referencia if self.ativa else 1.0

    def aguardar(self) -> None:
        if not self.ativa:
            return
        inicio = time.perf_counter()
        while self.razao() > 1.5 and time.perf_counter() - inicio < self.espera_maxima_s:
            time.sleep(1.0)
        self.esperas_s += time.perf_counter() - inicio

    def fechar_bloco(self) -> float:
        r = self.razao()
        self.razoes_no_fim.append(r)
        return r


CALMA = Calma(False)


# ---------------------------------------------------------------------------------------------------------------------
# O problema: um projeto do Triton, avaliado pela varredura oficial (a grade) ou ponto a ponto (o optuna)
# ---------------------------------------------------------------------------------------------------------------------
class Problema:
    """Projeto carregado pelo ``triton.cli`` e as duas formas de avaliá-lo."""

    def __init__(self, caminho: Path) -> None:
        from triton import cli
        self.cli = cli
        self.caminho = caminho
        bundle = cli._load_bundle(str(caminho))
        self.cfg = bundle["config"]
        self.precip = cli._get_precipitation(bundle)
        self.area0 = float(self.cfg.area)
        self.vmax0 = float(self.cfg.lower_tank_max)
        self.passo0 = float(self.cfg.lower_tank_step)
        with contextlib.redirect_stderr(io.StringIO()):
            cli._run_technical(self.cfg, self.precip, volume=0.0)    # concilia as frações e aquece o compilador (numba)

    def _ajustar(self, area: Optional[float], vmax: Optional[float], passo: Optional[float]):
        cfg = self.cfg
        antes = (cfg.area, cfg.lower_tank_max, cfg.lower_tank_step)
        if area is not None:
            cfg.area = float(area)
        if vmax is not None:
            cfg.lower_tank_max = float(vmax)
        if passo is not None:
            cfg.lower_tank_step = float(passo)
        return antes

    def _restaurar(self, antes: Tuple[float, float, float]) -> None:
        self.cfg.area, self.cfg.lower_tank_max, self.cfg.lower_tank_step = antes

    def grade(self, area: Optional[float], vmax: float, passo: float, cfg: Any = None) -> List[Dict[str, float]]:
        """A varredura oficial do volume (``cli.run_analysis``, tipo ``economic``) para uma área: uma linha por volume."""
        cfg = cfg or self.cfg
        antes = (cfg.area, cfg.lower_tank_max, cfg.lower_tank_step)
        try:
            if area is not None:
                cfg.area = float(area)
            cfg.lower_tank_max, cfg.lower_tank_step = float(vmax), float(passo)
            with contextlib.redirect_stderr(io.StringIO()):
                rel = self.cli.run_analysis(cfg, self.precip, "economic")
        finally:
            cfg.area, cfg.lower_tank_max, cfg.lower_tank_step = antes
        tec, eco = rel["technical"]["alternatives"], rel["economic"]["alternatives"]
        return [{"volume": e["lower_tank_volume_l"], "npv": e["npv_brl"], "capex": e["capex_brl"],
                 "agua": t["annual_rainwater_m3"]} for t, e in zip(tec, eco)]

    def avaliar(self, volume: float, area: Optional[float] = None) -> Dict[str, float]:
        """Um ponto: ``run_single_simulation`` (via ``_run_technical``) e a linha econômica, como na varredura."""
        antes = self._ajustar(area, None, None)
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                res, _ = self.cli._run_technical(self.cfg, self.precip, volume=float(volume))
                linha, _ = self.cli._economic_row(self.cfg, res[0], preco_por_volume=True)
        finally:
            self._restaurar(antes)
        return {"volume": float(volume), "npv": float(linha["npv_brl"]), "capex": float(linha["capex_brl"]),
                "agua": float(res[0].annual_pluvial_consumed_m3), "area": self.area0 if area is None else float(area)}


class Espaco:
    """O espaço discreto de busca: os volumes da grade (índice) e, se houver, as áreas (índice)."""

    def __init__(self, problema: Problema, volumes_vmax: float, passo: float, fatores_de_area: Sequence[float] = ()) -> None:
        self.p = problema
        self.vmax, self.passo = float(volumes_vmax), float(passo)
        self.areas: List[Optional[float]] = [problema.area0 * f for f in fatores_de_area] if fatores_de_area else [None]
        self.tabela: Dict[Tuple[int, int], Dict[str, float]] = {}
        self.volumes: List[float] = []
        self.tempo_da_grade_s = 0.0
        self.tempo_mediano_da_grade_s = 0.0
        self.repeticoes = 0
        self._montar()

    def _varrer(self) -> Dict[Tuple[int, int], Dict[str, float]]:
        tab: Dict[Tuple[int, int], Dict[str, float]] = {}
        for ia, area in enumerate(self.areas):
            linhas = self.p.grade(area, self.vmax, self.passo)
            for iv, linha in enumerate(linhas):
                tab[(ia, iv)] = {**linha, "area": area if area is not None else self.p.area0}
        return tab

    def _montar(self) -> None:
        self.tabela = self._varrer()
        self.volumes = [self.tabela[(0, iv)]["volume"] for iv in range(sum(1 for k in self.tabela if k[0] == 0))]

    def medir_grade(self, repeticoes: int) -> float:
        """Tempo mínimo (s) da grade inteira em ``repeticoes`` execuções, depois de aquecida (a mediana fica em ``tempo_mediano_da_grade_s``)."""
        tempos = []
        for _ in range(max(1, repeticoes)):
            CALMA.aguardar()
            t0 = time.perf_counter()
            self._varrer()
            tempos.append(time.perf_counter() - t0)
            CALMA.fechar_bloco()
        self.tempo_da_grade_s = min(tempos)      # o mais rápido: outros processos e a CPU só aumentam o tempo
        self.tempo_mediano_da_grade_s = statistics.median(tempos)
        self.repeticoes = len(tempos)
        return self.tempo_da_grade_s

    def referencia_s(self) -> float:
        """Tempo (s) de UMA varredura de volume (uma área), o mais rápido de 3: a régua do momento.

        A grade inteira são ``len(areas)`` varreduras; medir a régua logo antes e logo depois de cada estudo dá o custo do
        estudo em «grades» (tempo do estudo ÷ tempo da grade na mesma condição da máquina), que não depende de a CPU estar
        rápida ou reduzida naquele instante.
        """
        tempos = []
        for _ in range(3):
            t0 = time.perf_counter()
            self.p.grade(self.areas[0], self.vmax, self.passo)
            tempos.append(time.perf_counter() - t0)
        return min(tempos)

    @property
    def n_pontos(self) -> int:
        return len(self.tabela)

    @property
    def bidimensional(self) -> bool:
        return len(self.areas) > 1

    def ponto(self, chave: Tuple[int, int]) -> Dict[str, float]:
        """Avalia um ponto do espaço pelo motor ponto a ponto."""
        ia, iv = chave
        return self.p.avaliar(self.volumes[iv], self.areas[ia])

    def melhor_da_grade(self) -> Tuple[Tuple[int, int], Dict[str, float]]:
        chave = max(self.tabela, key=lambda k: (self.tabela[k]["npv"], -k[1], -k[0]))
        return chave, self.tabela[chave]


# ---------------------------------------------------------------------------------------------------------------------
# Utilidades de medida
# ---------------------------------------------------------------------------------------------------------------------
def _primeiro_indice(valores: Sequence[float], alvo: float) -> Optional[int]:
    """Número (a partir de 1) da primeira tentativa cujo melhor valor até ali chega a ``alvo``; ``None`` se nunca."""
    melhor = float("-inf")
    for i, v in enumerate(valores, 1):
        melhor = max(melhor, v)
        if melhor >= alvo:
            return i
    return None


def _resumo(valores: Sequence[Optional[float]], casas: int = 0) -> Dict[str, Any]:
    """Mediana e pior caso das sementes que chegaram; ``falhas`` conta as que não chegaram dentro do orçamento."""
    ok = [v for v in valores if v is not None]
    falhas = len(valores) - len(ok)
    return {"mediana": round(statistics.median(ok), casas) if ok else None,
            "pior": None if falhas or not ok else round(max(ok), casas),
            "melhor": round(min(ok), casas) if ok else None, "falhas": falhas, "sementes": len(valores)}


def _fmt(r: Dict[str, Any], casas: int = 0) -> str:
    if r["mediana"] is None:
        return f"não chegou ({r['falhas']}/{r['sementes']})"
    pior = f"{r['pior']:.{casas}f}" if r["pior"] is not None else f"não chegou em {r['falhas']}/{r['sementes']}"
    return f"{r['mediana']:.{casas}f} (pior: {pior})"


def hipervolume(pontos: Sequence[Tuple[float, float]]) -> float:
    """Hipervolume 2-D de pontos (agua a maximizar, custo a minimizar), ambos já em [0, 1], com referência (0, 1)."""
    frente: List[Tuple[float, float]] = []
    for agua, custo in sorted(set(pontos), key=lambda p: (p[1], -p[0])):
        if not frente or agua > frente[-1][0]:
            frente.append((agua, custo))
    area, agua_anterior = 0.0, 0.0
    for agua, custo in frente:
        area += (agua - agua_anterior) * (1.0 - custo)
        agua_anterior = agua
    return area


def frente_de_pareto(pontos: Dict[Tuple[int, int], Tuple[float, float]]) -> List[Tuple[int, int]]:
    """Chaves não dominadas (agua a maximizar, custo a minimizar); empates exatos ficam todos."""
    chaves = list(pontos)
    frente = []
    for k in chaves:
        a, c = pontos[k]
        dominado = any((pontos[j][0] >= a and pontos[j][1] <= c) and (pontos[j][0] > a or pontos[j][1] < c) for j in chaves)
        if not dominado:
            frente.append(k)
    return frente


# ---------------------------------------------------------------------------------------------------------------------
# Experimentos de objetivo único (VPL)
# ---------------------------------------------------------------------------------------------------------------------
def _rodar_estudo(optuna: Any, esp: Espaco, sampler: Any, tentativas: int, objetivo_vpl: bool = True,
                  duas_direcoes: bool = False, cache: Optional[Dict] = None):
    """Roda um estudo com ``n_jobs=1``; devolve a lista de tentativas (chave, valores, instante) e o tempo total."""
    registros: List[Dict[str, Any]] = []
    cache = {} if cache is None else cache
    CALMA.aguardar()
    ref_antes = esp.referencia_s()
    n_iv, n_ia = len(esp.volumes) - 1, len(esp.areas) - 1
    t0 = 0.0

    def objetivo(trial):
        iv = trial.suggest_int("iv", 0, n_iv)
        ia = trial.suggest_int("ia", 0, n_ia) if esp.bidimensional else 0
        chave = (ia, iv)
        novo = chave not in cache
        if novo:
            cache[chave] = esp.ponto(chave)
        v = cache[chave]
        registros.append({"chave": chave, "novo": novo, "t": time.perf_counter() - t0})
        if duas_direcoes:
            return v["agua"], (v["capex"] if v["capex"] > 0 else v["volume"])
        return v["npv"]

    direcoes = ["maximize", "minimize"] if duas_direcoes else ["maximize"]
    estudo = optuna.create_study(directions=direcoes, sampler=sampler)
    t0 = time.perf_counter()
    estudo.optimize(objetivo, n_trials=tentativas, n_jobs=1)
    total = time.perf_counter() - t0
    CALMA.fechar_bloco()
    ref = (ref_antes + esp.referencia_s()) / 2.0
    return registros, cache, total, ref


REPETICOES_DO_ESTUDO = 5


def _rodar_medido(optuna: Any, esp: Espaco, fabrica, semente: int, tentativas: int, duas_direcoes: bool = False):
    """Roda o MESMO estudo (mesma semente) algumas vezes: a trajetória tem de sair idêntica; vale a repetição de menor custo relativo.

    A trajetória idêntica é a prova prática de reprodutibilidade (semente fixa, ``n_jobs=1``, memória). O tempo mínimo
    afasta o ruído de outros processos e da redução de desempenho da CPU, que só aumentam o tempo, nunca o diminuem.
    """
    melhor = None
    trajetoria = None
    for _ in range(REPETICOES_DO_ESTUDO):
        registros, cache, total, ref = _rodar_estudo(optuna, esp, fabrica(semente), tentativas, duas_direcoes=duas_direcoes)
        chaves = [r["chave"] for r in registros]
        if trajetoria is None:
            trajetoria = chaves
        elif chaves != trajetoria:
            raise RuntimeError(f"estudo não reprodutível com a semente {semente}: trajetórias diferentes")
        if melhor is None or total / ref < melhor[2] / melhor[3]:
            melhor = (registros, cache, total, ref)
    return melhor


def experimento_vpl(optuna: Any, esp: Espaco, tentativas: int, sementes: Sequence[int], tolerancia_pct: float,
                    reavaliar) -> Dict[str, Any]:
    """TPE e busca aleatória (referência) contra a grade, em VPL; reavalia o melhor ponto de cada semente."""
    chave_otima, otimo = esp.melhor_da_grade()
    alvo_exato = otimo["npv"] - 1e-6 * max(1.0, abs(otimo["npv"]))
    alvo_classe = otimo["npv"] - tolerancia_pct / 100.0 * abs(otimo["npv"])
    saida: Dict[str, Any] = {
        "grade": {"pontos": esp.n_pontos, "tempo_s": esp.tempo_da_grade_s, "repeticoes": esp.repeticoes,
                  "otimo": {"chave": chave_otima, **otimo}},
        "metodos": {}}
    for nome, fabrica in (("TPE", lambda s: optuna.samplers.TPESampler(seed=s)),
                          ("aleatória", lambda s: optuna.samplers.RandomSampler(seed=s))):
        por_semente = []
        for semente in sementes:
            registros, cache, tempo_total, ref = _rodar_medido(optuna, esp, fabrica, semente, tentativas)
            em_grades = lambda t: t / (ref * len(esp.areas))      # tempo ÷ tempo da grade inteira na mesma condição
            valores = [cache[r["chave"]]["npv"] for r in registros]
            n_exato, n_classe = _primeiro_indice(valores, alvo_exato), _primeiro_indice(valores, alvo_classe)

            def sims(n: Optional[int]) -> Optional[int]:
                return None if n is None else sum(1 for r in registros[:n] if r["novo"])

            def seg(n: Optional[int]) -> Optional[float]:
                return None if n is None else em_grades(registros[n - 1]["t"])

            melhor_chave = max((r["chave"] for r in registros), key=lambda k: cache[k]["npv"])
            melhor = cache[melhor_chave]
            reav = reavaliar(esp, melhor_chave)
            por_semente.append({
                "semente": semente, "tentativas_exato": n_exato, "tentativas_classe": n_classe,
                "simulacoes_exato": sims(n_exato), "simulacoes_classe": sims(n_classe),
                "custo_exato": seg(n_exato), "custo_classe": seg(n_classe), "custo_orcamento": em_grades(tempo_total),
                "tempo_orcamento_s": tempo_total,
                "simulacoes_no_orcamento": sum(1 for r in registros if r["novo"]),
                "melhor": {"chave": melhor_chave, **melhor}, "reavaliado": reav,
                "dif_vpl": melhor["npv"] - otimo["npv"], "dif_vpl_pct": 100.0 * (melhor["npv"] - otimo["npv"]) / abs(otimo["npv"]) if otimo["npv"] else 0.0,
                "dif_volume_l": melhor["volume"] - otimo["volume"], "dif_area_m2": melhor["area"] - otimo["area"],
            })
        saida["metodos"][nome] = {
            "por_semente": por_semente,
            "tentativas_exato": _resumo([r["tentativas_exato"] for r in por_semente]),
            "tentativas_classe": _resumo([r["tentativas_classe"] for r in por_semente]),
            "simulacoes_exato": _resumo([r["simulacoes_exato"] for r in por_semente]),
            "simulacoes_classe": _resumo([r["simulacoes_classe"] for r in por_semente]),
            "custo_exato": _resumo([r["custo_exato"] for r in por_semente], 2),
            "custo_classe": _resumo([r["custo_classe"] for r in por_semente], 2),
            "custo_orcamento": round(statistics.median(r["custo_orcamento"] for r in por_semente), 2),
            "tempo_orcamento_ms": round(statistics.median(r["tempo_orcamento_s"] for r in por_semente) * 1000, 1),
            "simulacoes_no_orcamento": _resumo([r["simulacoes_no_orcamento"] for r in por_semente]),
            "dif_vpl_pct_pior": max(abs(r["dif_vpl_pct"]) for r in por_semente),
            "dif_volume_pior_l": max(abs(r["dif_volume_l"]) for r in por_semente),
            "dif_area_pior_m2": max(abs(r["dif_area_m2"]) for r in por_semente),
            "reavaliacao_dif_max": max(abs(r["reavaliado"]["npv"] - r["melhor"]["npv"]) for r in por_semente),
            "tentativas": tentativas,
        }
    return saida


def reavaliar_na_grade(problema: Problema, bundle_caminho: Path):
    """Reavaliação por outra via: cópia nova do projeto e a varredura oficial da área do ponto (não a função ponto a ponto)."""
    from triton import cli
    novo = cli._load_bundle(str(bundle_caminho))
    cfg_novo = novo["config"]
    precip_novo = cli._get_precipitation(novo)

    def reavaliar(esp: Espaco, chave: Tuple[int, int]) -> Dict[str, float]:
        ia, iv = chave
        cfg = copy.deepcopy(cfg_novo)
        if esp.areas[ia] is not None:
            cfg.area = float(esp.areas[ia])
        cfg.lower_tank_max, cfg.lower_tank_step = esp.vmax, esp.passo
        with contextlib.redirect_stderr(io.StringIO()):
            rel = cli.run_analysis(cfg, precip_novo, "economic")
        linha = rel["economic"]["alternatives"][iv]
        tec = rel["technical"]["alternatives"][iv]
        assert abs(linha["lower_tank_volume_l"] - esp.volumes[iv]) < 1e-9
        return {"npv": linha["npv_brl"], "capex": linha["capex_brl"], "agua": tec["annual_rainwater_m3"]}

    return reavaliar


# ---------------------------------------------------------------------------------------------------------------------
# Experimento biobjetivo (NSGA-II)
# ---------------------------------------------------------------------------------------------------------------------
def experimento_nsga(optuna: Any, esp: Espaco, tentativas: int, populacao: int, sementes: Sequence[int],
                     reavaliar) -> Dict[str, Any]:
    capex_zero = all(v["capex"] <= 0 for v in esp.tabela.values())
    custo = (lambda v: v["volume"]) if capex_zero else (lambda v: v["capex"])
    agua_max = max(v["agua"] for v in esp.tabela.values()) or 1.0
    custo_max = max(custo(v) for v in esp.tabela.values()) or 1.0
    norm = lambda v: (v["agua"] / agua_max, custo(v) / custo_max)
    pontos_grade = {k: norm(v) for k, v in esp.tabela.items()}
    frente = frente_de_pareto(pontos_grade)
    hv_grade = hipervolume([pontos_grade[k] for k in frente])
    marcos = sorted({m for m in (60, 120, 240, tentativas) if m <= tentativas})
    saida: Dict[str, Any] = {"grade": {"pontos": esp.n_pontos, "tempo_s": esp.tempo_da_grade_s, "repeticoes": esp.repeticoes, "frente": len(frente),
                                      "hipervolume": hv_grade, "custo": "volume do reservatório (capex zero no projeto)" if capex_zero else "capex"},
                             "marcos": marcos, "metodos": {}}
    for nome, fabrica in (("NSGA-II", lambda s: optuna.samplers.NSGAIISampler(seed=s, population_size=populacao)),
                          ("aleatória", lambda s: optuna.samplers.RandomSampler(seed=s))):
        por_semente = []
        for semente in sementes:
            registros, cache, tempo_total, ref = _rodar_medido(optuna, esp, fabrica, semente, tentativas, duas_direcoes=True)
            por_marco = {}
            for m in marcos:
                visitados = {r["chave"] for r in registros[:m]}
                pts = [norm(cache[k]) for k in visitados]
                por_marco[m] = {"hv_razao": hipervolume(pts) / hv_grade if hv_grade else 1.0,
                                "frente_achada": len(visitados & set(frente)) / len(frente),
                                "simulacoes": sum(1 for r in registros[:m] if r["novo"])}
            visitados = {r["chave"] for r in registros}
            achados = sorted(visitados & set(frente))
            reav = [reavaliar(esp, k) for k in achados[:3]]
            dif = max([abs(reav[i]["agua"] - cache[k]["agua"]) for i, k in enumerate(achados[:3])] or [0.0])
            por_semente.append({"semente": semente, "por_marco": por_marco, "tempo_orcamento_s": tempo_total,
                                "custo_orcamento": tempo_total / (ref * len(esp.areas)), "reavaliacao_dif_agua_max": dif})
        saida["metodos"][nome] = {
            "por_semente": por_semente,
            "por_marco": {m: {"hv_razao_mediana": statistics.median(s["por_marco"][m]["hv_razao"] for s in por_semente),
                              "hv_razao_pior": min(s["por_marco"][m]["hv_razao"] for s in por_semente),
                              "frente_achada_mediana": statistics.median(s["por_marco"][m]["frente_achada"] for s in por_semente),
                              "frente_achada_pior": min(s["por_marco"][m]["frente_achada"] for s in por_semente),
                              "simulacoes_mediana": statistics.median(s["por_marco"][m]["simulacoes"] for s in por_semente)}
                          for m in marcos},
            "custo_orcamento": round(statistics.median(s["custo_orcamento"] for s in por_semente), 2),
            "tempo_orcamento_ms": round(statistics.median(s["tempo_orcamento_s"] for s in por_semente) * 1000, 1),
            "reavaliacao_dif_max": max(s["reavaliacao_dif_agua_max"] for s in por_semente),
            "tentativas": tentativas,
        }
    return saida


# ---------------------------------------------------------------------------------------------------------------------
# Relatório em texto (Markdown)
# ---------------------------------------------------------------------------------------------------------------------
def _num(x: float, casas: int = 0) -> str:
    return f"{x:,.{casas}f}".replace(",", " ")


def imprimir_vpl(titulo: str, r: Dict[str, Any], tolerancia_pct: float) -> str:
    g = r["grade"]
    o = g["otimo"]
    linhas = [f"### {titulo}", "",
              f"Grade: {g['pontos']} simulações, {g['tempo_s'] * 1000:.1f} ms, o mais rápido de {g['repeticoes']} execuções "
              f"({g['tempo_s'] * 1000 / g['pontos']:.3f} ms por ponto). "
              f"Ótimo da grade: VPL {_num(o['npv'])}, volume {_num(o['volume'])} L, área {_num(o['area'], 0)} m², custo de implantação {_num(o['capex'])}.", "",
              "Custo em «grades»: tempo do método ÷ tempo da grade inteira medido na mesma condição da máquina (1,00 = o mesmo tempo da grade).", "",
              f"| Método | Tentativas até o ótimo exato | Simulações distintas | Custo (grades) | "
              f"Tentativas até VPL dentro de {tolerancia_pct:g} % | Simulações distintas | Custo (grades) | "
              f"Custo do orçamento (grades) | Pior diferença de VPL (%) | Pior diferença de volume (L) | Diferença máxima na reavaliação |",
              "| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |"]
    for nome, m in r["metodos"].items():
        linhas.append(f"| {nome} ({m['tentativas']} tent.) | {_fmt(m['tentativas_exato'])} | {_fmt(m['simulacoes_exato'])} | {_fmt(m['custo_exato'], 2)} | "
                      f"{_fmt(m['tentativas_classe'])} | {_fmt(m['simulacoes_classe'])} | {_fmt(m['custo_classe'], 2)} | "
                      f"{m['custo_orcamento']:.2f} | {m['dif_vpl_pct_pior']:.4f} | {_num(m['dif_volume_pior_l'])} | {m['reavaliacao_dif_max']:.3g} |")
    return chr(10).join(linhas)


def imprimir_nsga(r: Dict[str, Any]) -> str:
    g = r["grade"]
    linhas = ["### nsga: água pluvial aproveitada × custo", "",
              f"Grade: {g['pontos']} simulações, {g['tempo_s'] * 1000:.1f} ms; frente de Pareto da grade: {g['frente']} pontos "
              f"(custo = {g['custo']}).", "",
              "| Método | Tentativas | Simulações distintas (mediana) | Hipervolume / grade (mediana; pior) | Pontos da frente achados (mediana; pior) | Custo do orçamento (grades) |",
              "| :-- | --: | --: | --: | --: | --: |"]
    for nome, m in r["metodos"].items():
        for marco, v in m["por_marco"].items():
            custo = f"{m['custo_orcamento']:.2f}" if int(marco) == m["tentativas"] else ""
            linhas.append(f"| {nome} | {marco} | {v['simulacoes_mediana']:.0f} | {v['hv_razao_mediana']:.4f}; {v['hv_razao_pior']:.4f} | "
                          f"{100 * v['frente_achada_mediana']:.0f} %; {100 * v['frente_achada_pior']:.0f} % | {custo} |")
    linhas.append("")
    linhas.append("Diferença máxima de água aproveitada na reavaliação (m³/ano): " +
                  ", ".join(f"{n} {m['reavaliacao_dif_max']:.3g}" for n, m in r["metodos"].items()))
    return chr(10).join(linhas)


def ambiente(optuna: Any, edicao: str, caminho: Path, args: argparse.Namespace) -> Dict[str, Any]:
    import numpy
    try:
        from triton.core import simulation
        numba_ativo = bool(getattr(simulation, "HAS_NUMBA", False))
    except Exception:
        numba_ativo = False
    try:
        from triton import __version__ as versao
    except Exception:
        versao = "?"
    return {"edicao": edicao, "triton": versao, "projeto": caminho.relative_to(RAIZ).as_posix() if caminho.is_relative_to(RAIZ) else str(caminho),
            "python": platform.python_version(), "numpy": numpy.__version__, "optuna": optuna.__version__, "numba_ativo": numba_ativo,
            "sistema": platform.platform(), "processador": platform.processor(), "nucleos_logicos": os.cpu_count(),
            "semente_inicial": args.semente, "n_sementes": args.n_sementes, "n_jobs": 1, "armazenamento": "memória"}


def executar(args: argparse.Namespace) -> int:
    edicao = args.edicao or (os.environ.get("TRITON_EDITION", "").lower() if os.environ.get("TRITON_EDITION", "").lower() in EDICOES else "brl")
    opcional = preparar_edicao(edicao)
    optuna = exigir_optuna(opcional)
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    warnings.simplefilter("ignore")
    caminho = (args.projeto or (RAIZ / PROBLEMAS[edicao][0])).resolve()
    if not caminho.is_file():
        sys.exit(f"erro: projeto não encontrado: {caminho}")
    escolhidos = list(args.experimento or EXPERIMENTOS)
    sementes = [args.semente + i for i in range(max(1, args.n_sementes))]
    global CALMA, REPETICOES_DO_ESTUDO
    CALMA = Calma(args.aguardar_cpu)
    REPETICOES_DO_ESTUDO = max(1, args.repeticoes_do_estudo)
    problema = Problema(caminho)
    reavaliar = reavaliar_na_grade(problema, caminho)
    env = ambiente(optuna, edicao, caminho, args)
    print(f"# Experimento grade × optuna — edição {edicao}: {PROBLEMAS[edicao][1] if args.projeto is None else caminho.name}\n")
    print("```\n" + json.dumps(env, ensure_ascii=False, indent=1) + "\n```\n")
    resultados: Dict[str, Any] = {"ambiente": env}
    zero = problema.avaliar(1000.0)["capex"] <= 0
    if zero:
        print("Aviso: o projeto não declara custos de implantação (capex zero); o VPL só cresce com o volume e a área, "
              "e o ótimo é a borda ou um patamar da grade.\n")

    espaco_1d = espaco_1da = espaco_2d = None
    if "1d" in escolhidos:
        espaco_1d = Espaco(problema, problema.vmax0, problema.passo0)
        espaco_1d.medir_grade(args.repeticoes_de_tempo)
        r = experimento_vpl(optuna, espaco_1d, args.tentativas_1d, sementes, args.tolerancia_pct, reavaliar)
        resultados["1d"] = r
        print(imprimir_vpl("1d: volume na grade do projeto", r, args.tolerancia_pct) + "\n")
    vmax_amp = problema.vmax0 * FATOR_DA_GRADE_AMPLIADA
    passo_amp = vmax_amp / 40.0
    if "1da" in escolhidos:
        espaco_1da = Espaco(problema, vmax_amp, passo_amp)
        espaco_1da.medir_grade(args.repeticoes_de_tempo)
        r = experimento_vpl(optuna, espaco_1da, args.tentativas_1d, sementes, args.tolerancia_pct, reavaliar)
        resultados["1da"] = r
        print(imprimir_vpl(f"1da: volume na grade ampliada ({FATOR_DA_GRADE_AMPLIADA}x)", r, args.tolerancia_pct) + "\n")
    if "2d" in escolhidos or "nsga" in escolhidos:
        espaco_2d = Espaco(problema, vmax_amp, passo_amp, FATORES_DE_AREA)
        espaco_2d.medir_grade(max(1, args.repeticoes_de_tempo // 2))
    if "2d" in escolhidos:
        r = experimento_vpl(optuna, espaco_2d, args.tentativas_2d, sementes, args.tolerancia_pct, reavaliar)
        resultados["2d"] = r
        print(imprimir_vpl("2d: volume × área de captação", r, args.tolerancia_pct) + "\n")
    if "nsga" in escolhidos:
        r = experimento_nsga(optuna, espaco_2d, args.tentativas_nsga, args.populacao, sementes, reavaliar)
        resultados["nsga"] = r
        print(imprimir_nsga(r) + "\n")
    if CALMA.ativa:
        resultados["calma"] = {"espera_total_s": round(CALMA.esperas_s, 1), "blocos": len(CALMA.razoes_no_fim),
                               "razao_cpu_no_fim_max": round(max(CALMA.razoes_no_fim or [1.0]), 2),
                               "blocos_com_cpu_lenta_no_fim": sum(1 for r in CALMA.razoes_no_fim if r > 1.5)}
        print("Calibração da CPU: " + json.dumps(resultados["calma"]) + "\n")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(resultados, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        print(f"Resultados brutos em {args.json}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    _configurar_saida()
    args = montar_parser().parse_args(argv)
    return executar(args)


if __name__ == "__main__":
    sys.exit(main())
