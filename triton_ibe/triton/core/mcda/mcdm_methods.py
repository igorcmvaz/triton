"""
Módulo Core de Métodos de Tomada de Decisão Multicritério (MCDM).
Inclui:
- TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
- VIKOR (VlseKriterijumska Optimizacija I Kompromisno Resenje - Solução de Compromisso)
- SMAA-2 (Stochastic Multicriteria Acceptability Analysis - Decisão Robusta com Pesos Estocásticos)
- PROMETHEE II (Preference Ranking Organization METHod for Enrichment Evaluations - Superação Completa)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Sequence
import numpy as np

try:
    from numba import njit
except ImportError:  # pragma: no cover
    def njit(*args, **kwargs):
        def _wrap(fn):
            return fn
        return _wrap

from triton.core.topsis import TopsisCandidate, CRITERION_KEYS, CRITERION_IS_BENEFIT


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
    rank_acceptabilities: np.ndarray  # Matriz (n_alternativas x n_posições), em percentual de 0 a 100
    first_rank_probs: np.ndarray      # Aceitabilidade de 1º lugar (b_i^1), em percentual de 0 a 100
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
        """A mesma aceitabilidade de 1º lugar, em fração de 0 a 1.

        O motor grava `first_rank_probs` sempre em percentual. A conversão é fixa:
        a versão anterior adivinhava a unidade pelo máximo, e um resultado em que
        nenhuma alternativa passasse de 1% seria devolvido cem vezes maior.
        """
        return np.asarray(self.first_rank_probs, dtype=float) / 100.0

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


@dataclass
class PrometheeResult:
    """Resultado do método de ordenação por superação PROMETHEE II."""
    candidates: List[TopsisCandidate]
    leaving_flows: np.ndarray     # Fluxos positivos de saída (Phi+)
    entering_flows: np.ndarray    # Fluxos negativos de entrada (Phi-)
    net_flows: np.ndarray         # Fluxos líquidos de superação (Phi = Phi+ - Phi-)
    rankings: np.ndarray          # Índices ordenados por Phi decrescente
    best_index: int               # Índice da melhor alternativa
    preference_function: str = "linear"
    v_weight: float = 0.5         # Compatibilidade de apresentação

    @property
    def ranks(self) -> np.ndarray:
        """Postos das alternativas (1 = melhor, maior Phi)."""
        return np.argsort(np.argsort(-self.net_flows)) + 1

    @property
    def best_candidate(self) -> TopsisCandidate:
        return self.candidates[self.best_index]


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


#: Sorteios de pesos do SMAA-VIKOR quando nada se declara. É o perfil «alta
#: precisão» da interface; a linha de comando usava 5.000, e com menos sorteios
#: o líder podia mudar entre as duas para o mesmo projeto.
AMOSTRAS_SMAA_PADRAO = 20000


@njit(cache=True)
def _smaa_vikor_kernel(diff_matrix: np.ndarray, weight_samples: np.ndarray, v_param: float):
    num_samples, m = weight_samples.shape
    n = diff_matrix.shape[0]
    rank_counts = np.zeros((n, n), dtype=np.int64)
    weight_sums = np.zeros((n, m), dtype=np.float64)
    win_counts = np.zeros(n, dtype=np.int64)
    s = np.empty(n, dtype=np.float64)
    r = np.empty(n, dtype=np.float64)
    q = np.empty(n, dtype=np.float64)
    for k in range(num_samples):
        w = weight_samples[k]
        s_star = 1e308
        s_minus = -1e308
        r_star = 1e308
        r_minus = -1e308
        for i in range(n):
            si = 0.0
            ri = -1e308
            for j in range(m):
                v = diff_matrix[i, j] * w[j]
                si += v
                if v > ri:
                    ri = v
            s[i] = si
            r[i] = ri
            if si < s_star:
                s_star = si
            if si > s_minus:
                s_minus = si
            if ri < r_star:
                r_star = ri
            if ri > r_minus:
                r_minus = ri
        s_span = (s_minus - s_star) if (s_minus - s_star) > 1e-12 else 1.0
        r_span = (r_minus - r_star) if (r_minus - r_star) > 1e-12 else 1.0
        for i in range(n):
            q[i] = v_param * ((s[i] - s_star) / s_span) + (1.0 - v_param) * ((r[i] - r_star) / r_span)
        ranks = np.argsort(q)
        w0 = ranks[0]
        win_counts[w0] += 1
        for j in range(m):
            weight_sums[w0, j] += w[j]
        for pos in range(n):
            rank_counts[ranks[pos], pos] += 1
    return rank_counts, weight_sums, win_counts


def run_smaa_vikor(
    candidates: Sequence[TopsisCandidate],
    v_param: float = 0.5,
    num_samples: int = AMOSTRAS_SMAA_PADRAO,
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

    rank_counts, weight_sums, win_counts = _smaa_vikor_kernel(diff_matrix, weight_samples, float(v_param))

    rank_acceptabilities = (rank_counts / num_samples) * 100.0
    first_rank_probs = rank_acceptabilities[:, 0]
    most_acceptable = int(np.argmax(first_rank_probs))

    central_weights = np.zeros((n, m), dtype=float)
    confidence_factors = np.zeros(n, dtype=float)

    for i in range(n):
        if win_counts[i] > 0:
            cw = weight_sums[i] / win_counts[i]
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


@njit(cache=True)
def _promethee_kernel(
    matrix: np.ndarray,
    is_benefit: np.ndarray,
    weights: np.ndarray,
    pref_type: int,  # 0 = usual, 1 = linear (v-shape), 2 = gaussian
    q_param: np.ndarray,
    p_param: np.ndarray,
    s_param: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Kernel acelerado para cálculo de preferências e fluxos PROMETHEE II."""
    n, m = matrix.shape
    if n <= 1:
        return np.zeros(n, dtype=np.float64), np.zeros(n, dtype=np.float64), np.zeros(n, dtype=np.float64)

    pi = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for k in range(n):
            if i == k:
                continue
            total_pref = 0.0
            for j in range(m):
                if is_benefit[j]:
                    d = matrix[i, j] - matrix[k, j]
                else:
                    d = matrix[k, j] - matrix[i, j]

                if d <= 0.0:
                    p = 0.0
                elif pref_type == 0:  # Usual
                    p = 1.0
                elif pref_type == 1:  # Linear com limiares
                    q = q_param[j]
                    p_th = p_param[j]
                    if d <= q:
                        p = 0.0
                    elif d > p_th:
                        p = 1.0
                    else:
                        denom = p_th - q
                        p = (d - q) / denom if denom > 1e-12 else 1.0
                elif pref_type == 2:  # Gaussiana
                    sigma = s_param[j]
                    if sigma > 1e-12:
                        p = 1.0 - np.exp(-(d * d) / (2.0 * sigma * sigma))
                    else:
                        p = 1.0
                else:
                    p = 1.0 if d > 0.0 else 0.0

                total_pref += weights[j] * p
            pi[i, k] = total_pref

    denom = float(n - 1)
    phi_plus = np.zeros(n, dtype=np.float64)
    phi_minus = np.zeros(n, dtype=np.float64)
    for i in range(n):
        phi_plus[i] = np.sum(pi[i, :]) / denom
        phi_minus[i] = np.sum(pi[:, i]) / denom
    phi_net = phi_plus - phi_minus
    return phi_plus, phi_minus, phi_net


def run_promethee(
    candidates: Sequence[TopsisCandidate],
    weights: Optional[Sequence[float]] = None,
    preference_function: str = "linear",
    q_thresholds: Optional[Sequence[float]] = None,
    p_thresholds: Optional[Sequence[float]] = None,
) -> PrometheeResult:
    """Executa o método PROMETHEE II para ordenação completa por fluxos líquidos de superação.

    Parâmetros:
    -----------
    candidates: sequência de alternativas avaliadas
    weights: pesos dos 7 critérios ou 3 dimensões (Técnica, Econômica, Ambiental)
    preference_function: 'usual', 'linear' (padrão) ou 'gaussian'
    q_thresholds: limiares de indiferença por critério (opcional)
    p_thresholds: limiares de preferência por critério (opcional, padrão = amplitude max - min)
    """
    cand_list = list(candidates)
    n = len(cand_list)
    if n == 0:
        raise ValueError("A lista de candidatos não pode ser vazia.")

    m = len(CRITERION_KEYS)
    if n == 1:
        return PrometheeResult(
            candidates=cand_list,
            leaving_flows=np.zeros(1),
            entering_flows=np.zeros(1),
            net_flows=np.zeros(1),
            rankings=np.zeros(1, dtype=int),
            best_index=0,
            preference_function=preference_function,
        )

    matrix = np.zeros((n, m), dtype=float)
    for i, c in enumerate(cand_list):
        pot = c.potential_savings_pct if c.potential_savings_pct is not None else (
            c.water_saved_m3_yr / max(1e-6, c.water_saved_m3_yr) * 100)
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

    is_benefit = np.asarray(CRITERION_IS_BENEFIT, dtype=bool)

    pref_norm = str(preference_function).lower().strip()
    if pref_norm in ("usual", "strict", "tipo1"):
        pref_type = 0
    elif pref_norm in ("gaussian", "tipo6"):
        pref_type = 2
    else:
        pref_type = 1

    q_arr = np.zeros(m, dtype=float)
    if q_thresholds is not None:
        for idx in range(min(m, len(q_thresholds))):
            val = q_thresholds[idx]
            if val is not None and float(val) > 0:
                q_arr[idx] = float(val)

    p_arr = np.zeros(m, dtype=float)
    s_arr = np.zeros(m, dtype=float)
    for j in range(m):
        col = matrix[:, j]
        span = float(np.max(col) - np.min(col))
        if span <= 1e-12:
            span = 1.0
        if p_thresholds is not None and j < len(p_thresholds) and p_thresholds[j] is not None and p_thresholds[j] > 0:
            p_arr[j] = float(p_thresholds[j])
        else:
            p_arr[j] = span
        s_arr[j] = span / 2.0

    phi_plus, phi_minus, phi_net = _promethee_kernel(
        matrix, is_benefit, w, pref_type, q_arr, p_arr, s_arr
    )

    rankings = np.argsort(-phi_net)
    best_idx = int(rankings[0])

    return PrometheeResult(
        candidates=cand_list,
        leaving_flows=phi_plus,
        entering_flows=phi_minus,
        net_flows=phi_net,
        rankings=rankings,
        best_index=best_idx,
        preference_function=preference_function,
    )
