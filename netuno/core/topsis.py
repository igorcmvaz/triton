"""Decisão multicritério TOPSIS para as alternativas do Netuno.

O modelo usa sete critérios auditáveis, agrupados nos três eixos exibidos na
interface. Pesos de três eixos continuam aceitos e são divididos igualmente
entre os critérios do respectivo eixo. Também é possível informar sete pesos
diretamente.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np


CRITERION_KEYS: Tuple[str, ...] = (
    "technical_potential_pct",
    "technical_overflow_m3_yr",
    "economic_npv_brl",
    "economic_discounted_payback_years",
    "economic_irr_pct",
    "environmental_lifecycle_co2_kg",
    "environmental_potable_water_m3_yr",
)
CRITERION_LABELS: Tuple[str, ...] = (
    "Potencial máximo",
    "Mínimo extravasamento",
    "Maior VPL",
    "Menor payback descontado",
    "Maior TIR",
    "Menor CO₂ no fim da vida",
    "Menor consumo de água potável",
)
CRITERION_GROUPS: Tuple[str, ...] = (
    "technical", "technical",
    "economic", "economic", "economic",
    "environmental", "environmental",
)
# True = benefício (maximizar); False = custo/impacto (minimizar).
CRITERION_IS_BENEFIT = np.array([True, False, True, False, True, False, False], dtype=bool)


@dataclass
class TopsisCandidate:
    lower_tank_vol: float
    water_saved_m3_yr: float
    vpl_brl: float
    co2_saved_kg_lifetime: float
    capex_brl: float = 0.0
    capex: float = 0.0
    upper_tank_vol: float = 0.0
    technical_threshold_met: bool = False
    is_technical_optimum: bool = False
    extra_data: Dict[str, Any] = field(default_factory=dict)
    # ``None`` mantém compatibilidade com integrações antigas; os construtores
    # do fluxo completo sempre informam estes cinco indicadores.
    potential_savings_pct: Optional[float] = None
    overflow_m3_yr: Optional[float] = None
    discounted_payback_years: Optional[float] = None
    irr_pct: Optional[float] = None
    potable_consumed_m3_yr: Optional[float] = None

    @property
    def lifecycle_co2_kg(self) -> float:
        """Impacto líquido ao fim da vida: menor é melhor."""
        return -float(self.co2_saved_kg_lifetime)


@dataclass
class TopsisResult:
    candidates: List[TopsisCandidate]
    scores: np.ndarray
    rankings: np.ndarray
    best_index: int
    best_candidate: TopsisCandidate
    technical_best_index: int
    financial_best_index: int
    environmental_best_index: int
    decision_matrix: np.ndarray
    normalized_matrix: np.ndarray
    weighted_matrix: np.ndarray
    ideal_best: np.ndarray
    ideal_worst: np.ndarray
    dist_best: np.ndarray
    dist_worst: np.ndarray
    criterion_gap_to_best: np.ndarray
    criterion_weights: np.ndarray
    criterion_keys: Tuple[str, ...] = CRITERION_KEYS
    criterion_labels: Tuple[str, ...] = CRITERION_LABELS

    @property
    def criterion_proximity_to_best(self) -> np.ndarray:
        """Proximidade por critério: 1 = ótimo observado; 0 = pior."""
        return 1.0 - np.asarray(self.criterion_gap_to_best, dtype=float)

    @property
    def group_proximity_to_best(self) -> np.ndarray:
        """Proximidade média nos eixos técnico, econômico e ambiental."""
        proximity = self.criterion_proximity_to_best
        return np.column_stack((
            np.mean(proximity[:, 0:2], axis=1),
            np.mean(proximity[:, 2:5], axis=1),
            np.mean(proximity[:, 5:7], axis=1),
        ))


def _criterion_weights(weights: Optional[Sequence[float]]) -> np.ndarray:
    raw = np.array((0.333, 0.333, 0.334), dtype=float) if weights is None else np.asarray(tuple(weights), dtype=float)
    if raw.ndim != 1 or raw.size not in (3, 7):
        raise ValueError("Informe 3 pesos de eixo ou 7 pesos de critérios TOPSIS.")
    if not np.all(np.isfinite(raw)) or np.any(raw < 0):
        raise ValueError("Os pesos TOPSIS devem ser finitos e não negativos.")
    total = float(np.sum(raw))
    if total <= 0:
        raise ValueError("Ao menos um peso TOPSIS deve ser maior que zero.")
    raw = raw / total
    if raw.size == 7:
        return raw
    technical, economic, environmental = raw.tolist()
    return np.array((
        technical / 2.0, technical / 2.0,
        economic / 3.0, economic / 3.0, economic / 3.0,
        environmental / 2.0, environmental / 2.0,
    ), dtype=float)


def _payback_values(candidates: Sequence[TopsisCandidate]) -> np.ndarray:
    """Converte ausência de retorno ou volume zero em penalidade finita e explícita."""
    valid = [
        float(c.discounted_payback_years)
        for c in candidates
        if c.discounted_payback_years is not None
        and np.isfinite(c.discounted_payback_years)
        and c.discounted_payback_years > 0
        and float(c.lower_tank_vol) > 0
    ]
    if valid:
        worst = max(valid)
        no_return_penalty = max(worst + 1.0, worst * 1.10, 1.0)
    else:
        no_return_penalty = 1.0
    return np.array([
        float(c.discounted_payback_years)
        if c.discounted_payback_years is not None
        and np.isfinite(c.discounted_payback_years)
        and c.discounted_payback_years > 0
        and float(c.lower_tank_vol) > 0
        else no_return_penalty
        for c in candidates
    ], dtype=float)


def _decision_matrix(candidates: Sequence[TopsisCandidate]) -> np.ndarray:
    paybacks = _payback_values(candidates)
    rows = []
    for index, candidate in enumerate(candidates):
        # Fallbacks preservam chamadas antigas. No fluxo novo, os campos
        # opcionais são sempre preenchidos com os resultados da mesma simulação.
        potential = candidate.potential_savings_pct if candidate.potential_savings_pct is not None else candidate.water_saved_m3_yr
        overflow = candidate.overflow_m3_yr if candidate.overflow_m3_yr is not None else 0.0
        irr = candidate.irr_pct if candidate.irr_pct is not None else 0.0
        potable = candidate.potable_consumed_m3_yr if candidate.potable_consumed_m3_yr is not None else -candidate.water_saved_m3_yr
        rows.append((
            potential,
            overflow,
            candidate.vpl_brl,
            paybacks[index],
            irr,
            candidate.lifecycle_co2_kg,
            potable,
        ))
    matrix = np.asarray(rows, dtype=float)
    if not np.all(np.isfinite(matrix)):
        bad = np.argwhere(~np.isfinite(matrix))[0]
        raise ValueError(
            f"O critério TOPSIS '{CRITERION_KEYS[int(bad[1])]}' da alternativa "
            f"{int(bad[0]) + 1} não é finito."
        )
    return matrix


def calculate_topsis_scores(
    candidates: List[TopsisCandidate],
    weights: Optional[Sequence[float]] = None,
) -> Optional[TopsisResult]:
    """Classifica alternativas pelos sete critérios técnicos/econômicos/ambientais."""
    if not candidates:
        return None

    n = len(candidates)
    criterion_weights = _criterion_weights(weights)
    matrix = _decision_matrix(candidates)
    volumes = np.asarray([float(c.lower_tank_vol) for c in candidates])

    # Candidatos com volume > 0 representam sistemas pluviais reais instaláveis
    pos_mask = volumes > 0
    if np.any(pos_mask):
        pos_indices = np.where(pos_mask)[0]

        # 1. Ótimo Técnico: prioriza o volume determinado pelo threshold (se marcado no candidato),
        # ou o menor volume onde o threshold foi atingido, senão o maior potencial
        tech_thresh = [
            i for i in pos_indices
            if getattr(candidates[i], 'is_technical_optimum', False)
            or (candidates[i].extra_data and candidates[i].extra_data.get('is_technical_optimum', False))
        ]
        if tech_thresh:
            tech_best_idx = int(tech_thresh[0])
        else:
            first_thresh = [i for i in pos_indices if getattr(candidates[i], 'technical_threshold_met', False)]
            if first_thresh:
                tech_best_idx = int(first_thresh[0])
            else:
                sort_tech = np.lexsort((volumes[pos_indices], -matrix[pos_indices, 0]))
                tech_best_idx = int(pos_indices[sort_tech[0]])

        # 2. Ótimo Econômico: menor tempo de retorno (payback viável > 0) entre volumes > 0
        # Empate favorece maior VPL e menor volume
        sort_fin = np.lexsort((volumes[pos_indices], -matrix[pos_indices, 2], matrix[pos_indices, 3]))
        fin_best_idx = int(pos_indices[sort_fin[0]])

        # 3. Ótimo Ambiental: menor impacto líquido de ciclo de vida (maior offset de CO2) entre volumes > 0
        sort_env = np.lexsort((volumes[pos_indices], matrix[pos_indices, 5]))
        env_best_idx = int(pos_indices[sort_env[0]])
    else:
        tech_best_idx = int(np.lexsort((volumes, -matrix[:, 0]))[0])
        fin_best_idx = int(np.lexsort((volumes, -matrix[:, 2], matrix[:, 3]))[0])
        env_best_idx = int(np.lexsort((volumes, matrix[:, 5]))[0])

    col_min = np.min(matrix, axis=0)
    col_max = np.max(matrix, axis=0)
    col_range = col_max - col_min
    shifted = matrix - col_min
    norm_factors = np.sqrt(np.sum(shifted ** 2, axis=0))
    norm_factors[norm_factors == 0] = 1.0
    normalized = shifted / norm_factors
    weighted = normalized * criterion_weights

    ideal_best = np.where(CRITERION_IS_BENEFIT, np.max(weighted, axis=0), np.min(weighted, axis=0))
    ideal_worst = np.where(CRITERION_IS_BENEFIT, np.min(weighted, axis=0), np.max(weighted, axis=0))
    dist_best = np.sqrt(np.sum((weighted - ideal_best) ** 2, axis=1))
    dist_worst = np.sqrt(np.sum((weighted - ideal_worst) ** 2, axis=1))
    denominator = dist_best + dist_worst
    scores = np.divide(
        dist_worst, denominator,
        out=np.full(n, 0.5, dtype=float),
        where=denominator > np.finfo(float).eps,
    )
    if n == 1:
        scores[0] = 1.0

    gap = np.zeros_like(matrix, dtype=float)
    varying = col_range > 0
    benefit_cols = varying & CRITERION_IS_BENEFIT
    cost_cols = varying & ~CRITERION_IS_BENEFIT
    gap[:, benefit_cols] = (col_max[benefit_cols] - matrix[:, benefit_cols]) / col_range[benefit_cols]
    gap[:, cost_cols] = (matrix[:, cost_cols] - col_min[cost_cols]) / col_range[cost_cols]

    order = np.lexsort((volumes, -scores))
    rankings = np.empty(n, dtype=int)
    rankings[order] = np.arange(1, n + 1)
    best_idx = int(order[0])

    return TopsisResult(
        candidates=candidates,
        scores=scores,
        rankings=rankings,
        best_index=best_idx,
        best_candidate=candidates[best_idx],
        technical_best_index=tech_best_idx,
        financial_best_index=fin_best_idx,
        environmental_best_index=env_best_idx,
        decision_matrix=matrix,
        normalized_matrix=normalized,
        weighted_matrix=weighted,
        ideal_best=ideal_best,
        ideal_worst=ideal_worst,
        dist_best=dist_best,
        dist_worst=dist_worst,
        criterion_gap_to_best=gap,
        criterion_weights=criterion_weights,
    )
