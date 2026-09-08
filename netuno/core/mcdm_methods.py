"""
Módulo Core de Métodos de Tomada de Decisão Multicritério (MCDM).
Inclui:
- TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
- VIKOR (VlseKriterijumska Optimizacija I Kompromisno Resenje - Solução de Compromisso)
- SMAA-2 (Stochastic Multicriteria Acceptability Analysis - Decisão Robusta com Pesos Estocásticos)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Sequence
import numpy as np

from netuno.core.topsis import (
    TopsisCandidate, TopsisResult, calculate_topsis_scores,
    CRITERION_KEYS, CRITERION_LABELS, CRITERION_IS_BENEFIT
)


@dataclass
class VikorResult:
    """Resultado do método de compromisso VIKOR."""
    candidates: List[TopsisCandidate]
    s_scores: np.ndarray          # Medida de utilidade de grupo (S)
    r_scores: np.ndarray          # Medida de arrependimento individual (R)
    q_scores: np.ndarray          # Índice agregado VIKOR (Q - menor é melhor)
    rankings: np.ndarray          # Ranking ordenado por Q
    best_index: int               # Índice da melhor alternativa de compromisso
    v_weight: float = 0.5         # Peso da estratégia de consenso

    @property
    def ranks(self) -> np.ndarray:
        return np.argsort(np.argsort(self.q_scores)) + 1

    @property
    def best_candidate(self) -> TopsisCandidate:
        return self.candidates[self.best_index]


@dataclass
class SmaaResult:
    """Resultado da análise de aceitabilidade estocástica SMAA-2 / SMAA-VIKOR."""
    candidates: List[TopsisCandidate]
    rank_acceptabilities: np.ndarray  # Matriz (n_alternativas x n_posições) com probabilidades (0 a 100%)
    first_rank_probs: np.ndarray      # Probabilidade de cada alternativa ficar em 1º lugar (b_i^1)
    central_weights: np.ndarray       # Vetores centrais de pesos que elegem cada alternativa (n_alt x n_crit)
    most_acceptable_index: int        # Alternativa com maior probabilidade de 1º lugar
    num_samples: int = 5000
    engine: str = "vikor"             # Algoritmo de ranqueamento interno ("vikor" ou "topsis")
    confidence_factors: np.ndarray = field(default_factory=lambda: np.zeros(0))
    v_weight: float = 0.5             # Peso da estratégia de consenso do VIKOR

    @property
    def best_index(self) -> int:
        return self.most_acceptable_index

    @property
    def best_candidate(self) -> TopsisCandidate:
        return self.candidates[self.most_acceptable_index]

    @property
    def first_rank_acceptabilities(self) -> np.ndarray:
        return self.first_rank_probs / 100.0 if np.max(self.first_rank_probs) > 1.0 else self.first_rank_probs

    @property
    def ranks(self) -> np.ndarray:
        return np.argsort(np.argsort(-self.first_rank_probs)) + 1

    @property
    def acceptability_matrix(self) -> np.ndarray:
        return self.rank_acceptabilities

    @property
    def num_simulations(self) -> int:
        """Alias de apresentação para explicitar o total de execuções Monte Carlo."""
        return self.num_samples

    def get_central_dimension_weights(self, index: int) -> Tuple[float, float, float]:
        """
        Retorna os pesos centrais agregados nas 3 dimensões (Técnica, Econômica, Ambiental)
        para a alternativa indicada.
        """
        if index < 0 or index >= len(self.central_weights):
            return (0.333, 0.333, 0.334)
        cw = self.central_weights[index]
        if np.sum(cw) <= 1e-9:
            return (0.333, 0.333, 0.334)
        # Critérios: 0,1 -> Técnico; 2,3,4 -> Econômico; 5,6 -> Ambiental
        w_tech = float(cw[0] + cw[1])
        w_econ = float(cw[2] + cw[3] + cw[4])
        w_env = float(cw[5] + cw[6])
        tot = w_tech + w_econ + w_env
        if tot <= 1e-9:
            return (0.333, 0.333, 0.334)
        return (w_tech / tot, w_econ / tot, w_env / tot)


def run_vikor(
    candidates: Sequence[TopsisCandidate],
    weights: Optional[Sequence[float]] = None,
    v_param: float = 0.5
) -> VikorResult:
    """
    Executa o método VIKOR para identificação da solução de compromisso com menor arrependimento.
    """
    cand_list = list(candidates)
    n = len(cand_list)
    if n == 0:
        raise ValueError("A lista de candidatos não pode ser vazia.")

    # Constrói matriz de decisão
    m = len(CRITERION_KEYS)
    matrix = np.zeros((n, m), dtype=float)
    for i, c in enumerate(cand_list):
        pot = c.potential_savings_pct if c.potential_savings_pct is not None else (c.water_saved_m3_yr / max(1e-6, c.water_saved_m3_yr) * 100)
        over = c.overflow_m3_yr if c.overflow_m3_yr is not None else 0.0
        dpb = c.discounted_payback_years if c.discounted_payback_years is not None else 20.0
        irr = c.irr_pct if c.irr_pct is not None else 0.0
        pot_cons = c.potable_consumed_m3_yr if c.potable_consumed_m3_yr is not None else 0.0

        matrix[i, 0] = pot
        matrix[i, 1] = over
        matrix[i, 2] = c.vpl_brl
        matrix[i, 3] = dpb
        matrix[i, 4] = irr
        matrix[i, 5] = c.lifecycle_co2_kg
        matrix[i, 6] = pot_cons

    if weights is None:
        w = np.ones(m, dtype=float) / m
    else:
        raw_w = np.asarray(weights, dtype=float)
        if raw_w.size == 3:
            raw_w = raw_w / np.sum(raw_w)
            w = np.array([
                raw_w[0] / 2.0, raw_w[0] / 2.0,
                raw_w[1] / 3.0, raw_w[1] / 3.0, raw_w[1] / 3.0,
                raw_w[2] / 2.0, raw_w[2] / 2.0
            ], dtype=float)
        else:
            w = raw_w / np.sum(raw_w)

    # Identifica o melhor f* e o pior f- por critério
    f_best = np.zeros(m, dtype=float)
    f_worst = np.zeros(m, dtype=float)
    for j in range(m):
        col = matrix[:, j]
        if CRITERION_IS_BENEFIT[j]:
            f_best[j] = np.max(col)
            f_worst[j] = np.min(col)
        else:
            f_best[j] = np.min(col)
            f_worst[j] = np.max(col)

    # Calcula S e R
    s = np.zeros(n, dtype=float)
    r = np.zeros(n, dtype=float)
    denom = np.abs(f_best - f_worst)
    denom[denom == 0] = 1e-12

    for i in range(n):
        diffs = np.zeros(m, dtype=float)
        for j in range(m):
            if CRITERION_IS_BENEFIT[j]:
                val_diff = (f_best[j] - matrix[i, j]) / denom[j]
            else:
                val_diff = (matrix[i, j] - f_best[j]) / denom[j]
            diffs[j] = w[j] * max(0.0, val_diff)
        s[i] = np.sum(diffs)
        r[i] = np.max(diffs)

    s_star = np.min(s)
    s_minus = np.max(s)
    r_star = np.min(r)
    r_minus = np.max(r)

    s_span = (s_minus - s_star) if (s_minus - s_star) > 1e-12 else 1.0
    r_span = (r_minus - r_star) if (r_minus - r_star) > 1e-12 else 1.0

    q = v_param * ((s - s_star) / s_span) + (1.0 - v_param) * ((r - r_star) / r_span)

    # Ordenação por Q (menor Q = melhor)
    rankings = np.argsort(q)
    best_idx = int(rankings[0])

    return VikorResult(
        candidates=cand_list,
        s_scores=s,
        r_scores=r,
        q_scores=q,
        rankings=rankings,
        best_index=best_idx,
        v_weight=v_param,
    )


def run_smaa_vikor(
    candidates: Sequence[TopsisCandidate],
    v_param: float = 0.5,
    num_samples: int = 5000,
    random_seed: int = 42
) -> SmaaResult:
    """
    Executa o método estocástico híbrido SMAA-VIKOR (Stochastic Multicriteria Acceptability Analysis + VIKOR).
    Amostra vetores de pesos pelo simplex uniforme e ranqueia as alternativas pela solução de compromisso VIKOR,
    computando índices de aceitabilidade por posto (b_i^r), vetor central de pesos (w_i^c) e fatores de confiança.
    """
    cand_list = list(candidates)
    n = len(cand_list)
    if n == 0:
        raise ValueError("A lista de candidatos não pode ser vazia.")
    if not isinstance(num_samples, (int, np.integer)) or num_samples < 1:
        raise ValueError("num_samples deve ser um inteiro positivo.")

    m = len(CRITERION_KEYS)
    matrix = np.zeros((n, m), dtype=float)
    for i, c in enumerate(cand_list):
        pot = c.potential_savings_pct if c.potential_savings_pct is not None else (c.water_saved_m3_yr / max(1e-6, c.water_saved_m3_yr) * 100)
        over = c.overflow_m3_yr if c.overflow_m3_yr is not None else 0.0
        dpb = c.discounted_payback_years if c.discounted_payback_years is not None else 20.0
        irr = c.irr_pct if c.irr_pct is not None else 0.0
        pot_cons = c.potable_consumed_m3_yr if c.potable_consumed_m3_yr is not None else 0.0

        matrix[i, 0] = pot
        matrix[i, 1] = over
        matrix[i, 2] = c.vpl_brl
        matrix[i, 3] = dpb
        matrix[i, 4] = irr
        matrix[i, 5] = c.lifecycle_co2_kg
        matrix[i, 6] = pot_cons

    # Melhores (f*) e piores (f-) por critério
    f_best = np.zeros(m, dtype=float)
    f_worst = np.zeros(m, dtype=float)
    for j in range(m):
        col = matrix[:, j]
        if CRITERION_IS_BENEFIT[j]:
            f_best[j] = np.max(col)
            f_worst[j] = np.min(col)
        else:
            f_best[j] = np.min(col)
            f_worst[j] = np.max(col)

    denom = np.abs(f_best - f_worst)
    denom[denom == 0] = 1e-12

    # Matriz de distâncias normalizadas por critério
    diff_matrix = np.zeros((n, m), dtype=float)
    for j in range(m):
        if CRITERION_IS_BENEFIT[j]:
            diff_matrix[:, j] = (f_best[j] - matrix[:, j]) / denom[j]
        else:
            diff_matrix[:, j] = (matrix[:, j] - f_best[j]) / denom[j]
    diff_matrix = np.maximum(0.0, diff_matrix)

    rng = np.random.default_rng(random_seed)
    weight_samples = rng.dirichlet(np.ones(m), size=num_samples)

    rank_counts = np.zeros((n, n), dtype=int)
    first_rank_weights = [[] for _ in range(n)]

    for k in range(num_samples):
        w = weight_samples[k]
        w_diffs = diff_matrix * w  # shape (n, m)
        s = np.sum(w_diffs, axis=1)  # shape (n,)
        r = np.max(w_diffs, axis=1)  # shape (n,)

        s_star = np.min(s)
        s_minus = np.max(s)
        r_star = np.min(r)
        r_minus = np.max(r)

        s_span = (s_minus - s_star) if (s_minus - s_star) > 1e-12 else 1.0
        r_span = (r_minus - r_star) if (r_minus - r_star) > 1e-12 else 1.0

        q = v_param * ((s - s_star) / s_span) + (1.0 - v_param) * ((r - r_star) / r_span)

        ranks = np.argsort(q)
        for pos, alt_idx in enumerate(ranks):
            rank_counts[alt_idx, pos] += 1
            if pos == 0:
                first_rank_weights[alt_idx].append(w)

    rank_acceptabilities = (rank_counts / num_samples) * 100.0
    first_rank_probs = rank_acceptabilities[:, 0]
    most_acceptable = int(np.argmax(first_rank_probs))

    central_weights = np.zeros((n, m), dtype=float)
    confidence_factors = np.zeros(n, dtype=float)

    for i in range(n):
        if len(first_rank_weights[i]) > 0:
            cw = np.mean(first_rank_weights[i], axis=0)
            central_weights[i] = cw
            w_diffs_c = diff_matrix * cw
            s_c = np.sum(w_diffs_c, axis=1)
            r_c = np.max(w_diffs_c, axis=1)
            s_star_c, s_minus_c = np.min(s_c), np.max(s_c)
            r_star_c, r_minus_c = np.min(r_c), np.max(r_c)
            s_span_c = (s_minus_c - s_star_c) if (s_minus_c - s_star_c) > 1e-12 else 1.0
            r_span_c = (r_minus_c - r_star_c) if (r_minus_c - r_star_c) > 1e-12 else 1.0
            q_c = v_param * ((s_c - s_star_c) / s_span_c) + (1.0 - v_param) * ((r_c - r_star_c) / r_span_c)
            confidence_factors[i] = 1.0 if np.argmin(q_c) == i else 0.0
        else:
            central_weights[i] = np.zeros(m)
            confidence_factors[i] = 0.0

    return SmaaResult(
        candidates=cand_list,
        rank_acceptabilities=rank_acceptabilities,
        first_rank_probs=first_rank_probs,
        central_weights=central_weights,
        most_acceptable_index=most_acceptable,
        num_samples=num_samples,
        engine="vikor",
        confidence_factors=confidence_factors,
        v_weight=v_param,
    )


def run_smaa_analysis(
    candidates: Sequence[TopsisCandidate],
    num_samples: int = 5000,
    random_seed: int = 42,
    engine: str = "vikor",
    v_param: float = 0.5
) -> SmaaResult:
    """
    Executa a análise de aceitabilidade estocástica SMAA-2 (usando SMAA-VIKOR como padrão robusto).
    """
    if engine.lower() == "vikor":
        return run_smaa_vikor(
            candidates=candidates,
            v_param=v_param,
            num_samples=num_samples,
            random_seed=random_seed
        )

    if not isinstance(num_samples, (int, np.integer)) or num_samples < 1:
        raise ValueError("num_samples deve ser um inteiro positivo.")

    # Engine TOPSIS alternativo
    cand_list = list(candidates)
    n = len(cand_list)
    if n == 0:
        raise ValueError("A lista de candidatos não pode ser vazia.")

    m = len(CRITERION_KEYS)
    matrix = np.zeros((n, m), dtype=float)
    for i, c in enumerate(cand_list):
        pot = c.potential_savings_pct if c.potential_savings_pct is not None else (c.water_saved_m3_yr / max(1e-6, c.water_saved_m3_yr) * 100)
        over = c.overflow_m3_yr if c.overflow_m3_yr is not None else 0.0
        dpb = c.discounted_payback_years if c.discounted_payback_years is not None else 20.0
        irr = c.irr_pct if c.irr_pct is not None else 0.0
        pot_cons = c.potable_consumed_m3_yr if c.potable_consumed_m3_yr is not None else 0.0

        matrix[i, 0] = pot
        matrix[i, 1] = over
        matrix[i, 2] = c.vpl_brl
        matrix[i, 3] = dpb
        matrix[i, 4] = irr
        matrix[i, 5] = c.lifecycle_co2_kg
        matrix[i, 6] = pot_cons

    norm_factors = np.linalg.norm(matrix, axis=0)
    norm_factors[norm_factors == 0] = 1.0
    norm_matrix = matrix / norm_factors

    rng = np.random.default_rng(random_seed)
    weight_samples = rng.dirichlet(np.ones(m), size=num_samples)

    rank_counts = np.zeros((n, n), dtype=int)
    first_rank_weights = [[] for _ in range(n)]

    for k in range(num_samples):
        w = weight_samples[k]
        weighted = norm_matrix * w

        ideal_best = np.zeros(m)
        ideal_worst = np.zeros(m)
        for j in range(m):
            if CRITERION_IS_BENEFIT[j]:
                ideal_best[j] = np.max(weighted[:, j])
                ideal_worst[j] = np.min(weighted[:, j])
            else:
                ideal_best[j] = np.min(weighted[:, j])
                ideal_worst[j] = np.max(weighted[:, j])

        d_best = np.sqrt(np.sum((weighted - ideal_best) ** 2, axis=1))
        d_worst = np.sqrt(np.sum((weighted - ideal_worst) ** 2, axis=1))
        scores = d_worst / np.maximum(1e-12, (d_best + d_worst))

        ranks = np.argsort(-scores)
        for pos, alt_idx in enumerate(ranks):
            rank_counts[alt_idx, pos] += 1
            if pos == 0:
                first_rank_weights[alt_idx].append(w)

    rank_acceptabilities = (rank_counts / num_samples) * 100.0
    first_rank_probs = rank_acceptabilities[:, 0]
    most_acceptable = int(np.argmax(first_rank_probs))

    central_weights = np.zeros((n, m), dtype=float)
    for i in range(n):
        if len(first_rank_weights[i]) > 0:
            central_weights[i] = np.mean(first_rank_weights[i], axis=0)
        else:
            central_weights[i] = np.zeros(m)

    return SmaaResult(
        candidates=cand_list,
        rank_acceptabilities=rank_acceptabilities,
        first_rank_probs=first_rank_probs,
        central_weights=central_weights,
        most_acceptable_index=most_acceptable,
        num_samples=num_samples,
        engine="topsis",
    )
