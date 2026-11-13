"""Decisão multicritério TOPSIS para as alternativas do Triton.

Refatorado com matriz de decisão multicritério (MCDM) balanceada em quatro
dimensões (Técnica, Econômica, Ambiental e Estrutural/Executiva):
1. Técnica: volumetric_reliability_pct, storage_efficiency_pct
2. Econômica: net_financial_savings_brl, lcow_brl_m3, payback_years
3. Ambiental: lifecycle_co2_kg
4. Estrutural/Executiva: material_mass_kg, overflow_m3_yr
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np


CRITERION_KEYS: Tuple[str, ...] = (
    "volumetric_reliability_pct",
    "storage_efficiency_pct",
    "net_financial_savings_brl",
    "lcow_brl_m3",
    "payback_years",
    "lifecycle_co2_kg",
    "material_mass_kg",
    "overflow_m3_yr",
)
CRITERION_LABELS: Tuple[str, ...] = (
    "Confiabilidade volumétrica",
    "Eficiência de armazenamento",
    "Economia financeira líquida",
    "Custo unitário nivelado (LCOW)",
    "Tempo de retorno (payback)",
    "CO₂ de ciclo de vida",
    "Massa a seco dos materiais",
    "Volume anual extravasado",
)
CRITERION_GROUPS: Tuple[str, ...] = (
    "technical", "technical",
    "economic", "economic", "economic",
    "environmental",
    "structural", "structural",
)
#: Parte de cada critério dentro do seu eixo (normalizada eixo a eixo; só as razões importam).
#: Ordem de ``CRITERION_KEYS``.
PARTES_NO_EIXO_PADRAO: Tuple[float, ...] = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
PARTES_IGUAIS_NO_EIXO: Tuple[float, ...] = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
# True = benefício (maximizar); False = custo/impacto (minimizar).
CRITERION_IS_BENEFIT = np.array([True, True, True, False, False, False, False, False], dtype=bool)


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
    # Critérios MCDM (novos e legados)
    volumetric_reliability_pct: Optional[float] = None
    storage_efficiency_pct: Optional[float] = None
    net_financial_savings_brl: Optional[float] = None
    lcow_brl_m3: Optional[float] = None
    payback_years: Optional[float] = None
    material_mass_kg: Optional[float] = None
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

    def faixa_de_escolha(self, tolerancia=None) -> Optional[Dict[str, Any]]:
        """Volumes com escore TOPSIS semelhante ao maior (ver ``faixa_de_escolha``)."""
        return faixa_de_escolha([c.lower_tank_vol for c in self.candidates], self.scores, True, tolerancia)

    @property
    def criterion_proximity_to_best(self) -> np.ndarray:
        """Proximidade por critério: 1 = ótimo observado; 0 = pior."""
        return 1.0 - np.asarray(self.criterion_gap_to_best, dtype=float)

    @property
    def group_proximity_to_best(self) -> np.ndarray:
        """Proximidade média nos eixos técnico, econômico, ambiental e estrutural."""
        proximity = self.criterion_proximity_to_best
        cols = [
            np.mean(proximity[:, 0:2], axis=1),
            np.mean(proximity[:, 2:5], axis=1),
            proximity[:, 5],
        ]
        if proximity.shape[1] >= 8:
            cols.append(np.mean(proximity[:, 6:8], axis=1))
        return np.column_stack(cols)


_EIXOS: Tuple[Tuple[int, ...], ...] = ((0, 1), (2, 3, 4), (5,), (6, 7))
_NOMES_EIXOS: Tuple[str, ...] = ("técnico", "econômico", "ambiental", "estrutural")


#: Mensagem para quem traz pesos ou partes do modelo de sete critérios (até a 0.1.0).
_SETE_CRITERIOS = (
    "O multicritério da versão 0.2.0 tem oito critérios em quatro eixos, e os sete "
    "valores do modelo anterior não correspondem a eles. Informe quatro pesos de eixo "
    "(técnico, econômico, ambiental, estrutural) ou oito pesos de critério."
)


def validar_partes_no_eixo(partes: Optional[Sequence[float]]) -> np.ndarray:
    """Valida as partes nos eixos (``None`` = padrão) e devolve as partes normalizadas dentro de cada eixo."""
    bruto = np.asarray(tuple(PARTES_NO_EIXO_PADRAO if partes is None else partes), dtype=float)
    if bruto.ndim == 1 and bruto.size == 7:
        raise ValueError(_SETE_CRITERIOS)
    if bruto.ndim != 1 or bruto.size != 8:
        raise ValueError("Informe 8 partes, uma por critério TOPSIS (na ordem dos critérios).")
    if not np.all(np.isfinite(bruto)) or np.any(bruto < 0):
        raise ValueError("As partes no eixo devem ser finitas e não negativas.")
    saida = np.zeros(8, dtype=float)
    for nome, indices in zip(_NOMES_EIXOS, _EIXOS):
        soma = float(np.sum(bruto[list(indices)]))
        if soma <= 0:
            raise ValueError(f"Ao menos um critério do eixo {nome} deve ter parte maior que zero.")
        saida[list(indices)] = bruto[list(indices)] / soma
    return saida


def pesos_de_eixo(pesos_eixos: Optional[Sequence[float]]) -> np.ndarray:
    """Os quatro pesos de eixo, normalizados.

    Três pesos (técnico, econômico, ambiental) vêm de projetos e estudos feitos até a
    0.1.0: o eixo estrutural, que não existia, recebe a média dos três, de modo que
    pesos iguais continuam iguais.
    """
    if pesos_eixos is None:
        eixos = np.asarray(PESOS_PADRAO, dtype=float)
    else:
        eixos = np.asarray(tuple(pesos_eixos), dtype=float)
        if eixos.ndim == 1 and eixos.size == 3:
            eixos = np.append(eixos, float(np.mean(eixos)))
    if eixos.ndim != 1 or eixos.size != 4:
        raise ValueError("Informe 4 pesos de eixo (técnico, econômico, ambiental, estrutural).")
    if not np.all(np.isfinite(eixos)) or np.any(eixos < 0):
        raise ValueError("Os pesos TOPSIS devem ser finitos e não negativos.")
    total = float(np.sum(eixos))
    if total <= 0:
        raise ValueError("Ao menos um peso TOPSIS deve ser maior que zero.")
    return eixos / total


def pesos_dos_criterios(pesos_eixos: Optional[Sequence[float]] = None, partes: Optional[Sequence[float]] = None) -> np.ndarray:
    """Oito pesos de critério: o peso de cada eixo repartido pelas partes no eixo."""
    eixos = pesos_de_eixo(pesos_eixos)
    normalizadas = validar_partes_no_eixo(partes)
    saida = np.zeros(8, dtype=float)
    for peso, indices in zip(eixos, _EIXOS):
        saida[list(indices)] = peso * normalizadas[list(indices)]
    return saida


def _criterion_weights(weights: Optional[Sequence[float]], parts: Optional[Sequence[float]] = None) -> np.ndarray:
    raw = None if weights is None else np.asarray(tuple(weights), dtype=float)
    if raw is not None and raw.ndim == 1 and raw.size == 7:
        raise ValueError(_SETE_CRITERIOS)
    if raw is not None and (raw.ndim != 1 or raw.size not in (3, 4, 8)):
        raise ValueError("Informe 4 pesos de eixo (técnico, econômico, ambiental, estrutural) ou 8 pesos de critério TOPSIS.")
    if raw is None or raw.size in (3, 4):
        return pesos_dos_criterios(raw, parts)
    if not np.all(np.isfinite(raw)) or np.any(raw < 0):
        raise ValueError("Os pesos TOPSIS devem ser finitos e não negativos.")
    total = float(np.sum(raw))
    if total <= 0:
        raise ValueError("Ao menos um peso TOPSIS deve ser maior que zero.")
    return raw / total


def _payback_values(candidates: Sequence[TopsisCandidate]) -> np.ndarray:
    """Payback descontado de cada alternativa; quem não se paga recebe uma penalidade explícita.

    A penalidade é o pior payback observado mais 10% (ao menos um ano a mais, e ao
    menos 20 anos): a alternativa sem retorno fica atrás de todas as que se pagam.
    """
    def _pb(c):
        pb = getattr(c, 'payback_years', None)
        if pb is None:
            pb = getattr(c, 'discounted_payback_years', None)
        if pb is not None and np.isfinite(pb) and pb > 0 and float(c.lower_tank_vol) > 0:
            return float(pb)
        return None

    valores = [_pb(c) for c in candidates]
    validos = [v for v in valores if v is not None]
    penalidade = max(max(validos) + 1.0, max(validos) * 1.10, 20.0) if validos else 20.0
    return np.array([penalidade if v is None else v for v in valores], dtype=float)


def _lcow_values(candidates: Sequence[TopsisCandidate]) -> np.ndarray:
    """Custo nivelado da água de cada alternativa, na moeda do projeto por m³.

    O valor vem da análise econômica (``lcow_brl_m3``, calculado com a taxa, o
    horizonte e os custos do projeto). A alternativa sem água entregue (volume zero)
    não tem custo nivelado: recebe o pior valor observado mais 10%. Sem nenhum valor
    informado, o critério fica constante e não pesa na escolha.
    """
    def _lcow(c):
        v = getattr(c, 'lcow_brl_m3', None)
        if v is None and c.extra_data:
            v = c.extra_data.get('lcow_brl_m3')
        if v is not None and np.isfinite(v) and v > 0 and float(c.lower_tank_vol) > 0:
            return float(v)
        return None

    valores = [_lcow(c) for c in candidates]
    validos = [v for v in valores if v is not None]
    penalidade = max(validos) * 1.10 if validos else 0.0
    return np.array([penalidade if v is None else v for v in valores], dtype=float)


def _decision_matrix(candidates: Sequence[TopsisCandidate]) -> np.ndarray:
    """Matriz de decisão (n x 8) na ordem de ``CRITERION_KEYS``.

    Cada critério vem do candidato. Os que podem faltar em chamadas antigas são
    deduzidos de outros campos do próprio candidato, sem constante externa:
    a confiabilidade volumétrica cai para o potencial de economia (que tem a demanda
    total no denominador, e não só a pluvial); a eficiência de armazenamento é a água
    entregue por dia sobre o volume; a economia líquida é o VPL; a massa a seco sai
    da calculadora de peso com a configuração padrão.
    """
    n = len(candidates)
    m = len(CRITERION_KEYS)
    matrix = np.zeros((n, m), dtype=float)
    pb_values = _payback_values(candidates)
    lcow_values = _lcow_values(candidates)

    for i, c in enumerate(candidates):
        vol_low = float(getattr(c, 'lower_tank_vol', 0.0) or 0.0)
        agua_ano = float(getattr(c, 'water_saved_m3_yr', 0.0) or 0.0)

        # 0: confiabilidade volumétrica (%)
        if getattr(c, 'volumetric_reliability_pct', None) is not None:
            v_rel = float(c.volumetric_reliability_pct)
        elif getattr(c, 'potential_savings_pct', None) is not None:
            v_rel = float(c.potential_savings_pct)
        else:
            v_rel = 0.0

        # 1: eficiência de armazenamento (% do volume entregue por dia)
        if getattr(c, 'storage_efficiency_pct', None) is not None:
            s_eff = float(c.storage_efficiency_pct)
        elif vol_low > 0:
            s_eff = min(100.0, 100.0 * (agua_ano * 1000.0 / 365.25) / vol_low)
        else:
            s_eff = 0.0

        # 2: economia financeira líquida (VPL contra a linha de base)
        if getattr(c, 'net_financial_savings_brl', None) is not None:
            net_fin = float(c.net_financial_savings_brl)
        else:
            net_fin = float(getattr(c, 'vpl_brl', 0.0) or 0.0)

        # 5: CO₂e líquido de ciclo de vida (menor é melhor)
        co2_val = float(c.lifecycle_co2_kg)

        # 6: massa a seco dos materiais
        if getattr(c, 'material_mass_kg', None) is not None:
            mass_val = float(c.material_mass_kg)
        elif c.extra_data and c.extra_data.get('material_mass_kg') is not None:
            mass_val = float(c.extra_data['material_mass_kg'])
        elif vol_low > 0 or float(getattr(c, 'upper_tank_vol', 0.0) or 0.0) > 0:
            from triton.core.system_weight import calculate_system_weight
            mass_val = float(calculate_system_weight(
                vol_low, upper_tank_vol_l=float(getattr(c, 'upper_tank_vol', 0.0) or 0.0)).total_dry_mass_kg)
        else:
            mass_val = 0.0

        # 7: extravasamento anual
        over_val = float(getattr(c, 'overflow_m3_yr', 0.0) or 0.0)

        matrix[i] = (v_rel, s_eff, net_fin, lcow_values[i], pb_values[i], co2_val, mass_val, over_val)

    if not np.all(np.isfinite(matrix)):
        bad = np.argwhere(~np.isfinite(matrix))[0]
        raise ValueError(
            f"O critério TOPSIS '{CRITERION_KEYS[int(bad[1])]}' da alternativa "
            f"{int(bad[0]) + 1} não é finito."
        )
    return matrix


build_decision_matrix = _decision_matrix
extract_mcdm_matrix = _decision_matrix


#: Pedido de pesos objetivos: no lugar dos pesos, a palavra «critic».
PESOS_CRITIC = "critic"


def eh_critic(pesos) -> bool:
    """True quando os pesos pedidos são os do CRITIC (a palavra «critic», sem distinguir maiúsculas)."""
    return isinstance(pesos, str) and pesos.strip().lower() == PESOS_CRITIC


def pesos_critic(matriz, volumes=None) -> np.ndarray:
    """Pesos objetivos pelo método CRITIC (Diakoulaki, Mavrotas e Papayannakis, 1995).

    Cada critério é normalizado de 0 (pior valor observado) a 1 (melhor), no sentido do critério.
    A informação do critério é Cⱼ = σⱼ · Σₖ (1 − rⱼₖ): o desvio-padrão σⱼ mede o contraste entre as
    alternativas, e (1 − rⱼₖ) o quanto o critério difere dos demais (r é a correlação de Pearson).
    O peso é Cⱼ / Σ C. Critério constante não informa nada e recebe peso zero.

    Os pesos saem das alternativas com volume maior que zero, quando há ao menos duas: a alternativa
    sem cisterna entra no TOPSIS com penalidades de LCOW e payback, e esses valores artificiais
    inflariam o contraste. Sem contraste nenhum, os pesos ficam iguais.
    """
    M = np.asarray(matriz, dtype=float)
    if volumes is not None:
        vol = np.asarray(volumes, dtype=float)
        if vol.shape[0] == M.shape[0] and int(np.count_nonzero(vol > 0)) >= 2:
            M = M[vol > 0]
    n, m = M.shape
    if n < 2:
        return np.ones(m, dtype=float) / m
    lo = M.min(axis=0)
    hi = M.max(axis=0)
    amplitude = hi - lo
    varia = amplitude > 1e-12 * np.maximum(1.0, np.abs(hi))
    R = np.zeros_like(M)
    for j in np.flatnonzero(varia):
        if CRITERION_IS_BENEFIT[j]:
            R[:, j] = (M[:, j] - lo[j]) / amplitude[j]
        else:
            R[:, j] = (hi[j] - M[:, j]) / amplitude[j]
    sigma = R.std(axis=0)
    corr = np.zeros((m, m), dtype=float)
    idx = np.flatnonzero(varia)
    if idx.size >= 2:
        corr[np.ix_(idx, idx)] = np.nan_to_num(np.corrcoef(R[:, idx], rowvar=False))
    np.fill_diagonal(corr, 1.0)
    informacao = sigma * np.sum(1.0 - corr, axis=1)
    total = float(np.sum(informacao))
    if not np.isfinite(total) or total <= 0:
        return np.ones(m, dtype=float) / m
    return informacao / total


def _pesos_da_decisao(weights, parts, matrix: np.ndarray, volumes) -> np.ndarray:
    """Os oito pesos de critério: os declarados (eixos e partes, ou oito) ou os do CRITIC."""
    if eh_critic(weights):
        return pesos_critic(matrix, volumes)
    if isinstance(weights, str):
        raise ValueError(f"Pesos «{weights}» desconhecidos: use números ou «critic».")
    return _criterion_weights(weights, parts)


#: Tolerância padrão da faixa de escolha: 5% da amplitude dos escores, contados do maior.
TOLERANCIA_FAIXA_PADRAO = 0.05


def validar_tolerancia_da_faixa(tolerancia) -> float:
    """A tolerância da faixa de escolha, de 0 a 1 (fração da amplitude dos escores)."""
    t = TOLERANCIA_FAIXA_PADRAO if tolerancia is None else float(tolerancia)
    if not np.isfinite(t) or t < 0.0 or t > 1.0:
        raise ValueError("A tolerância da faixa de escolha deve ficar entre 0 e 1 (fração da amplitude dos escores).")
    return t


def faixa_de_escolha(volumes, escores, maior_melhor: bool = True, tolerancia=None) -> Optional[Dict[str, Any]]:
    """Os volumes com resultado multicritério semelhante ao do maior escore.

    Quando vários volumes pontuam quase igual, apontar um só como «o melhor» exagera a precisão do
    método. A faixa reúne os volumes cujo escore, normalizado entre o pior (0) e o melhor (1) dos
    volumes maiores que zero, fica a até ``tolerancia`` do melhor (padrão: 5% da amplitude). A mesma
    regra vale para qualquer método: ``maior_melhor=False`` para o índice Q do VIKOR.

    Devolve ``volumes_l`` (os volumes da faixa, em ordem), ``min_volume_l``, ``max_volume_l``,
    ``best_volume_l`` (o de maior escore; empate, o menor volume), ``tolerance`` e ``contiguous``
    (False quando algum volume avaliado entre o menor e o maior da faixa fica fora dela).
    """
    tol = validar_tolerancia_da_faixa(tolerancia)
    v = np.asarray(volumes, dtype=float)
    s = np.asarray(escores, dtype=float)
    ok = (v > 0) & np.isfinite(s)
    if not np.any(ok):
        return None
    vv = v[ok]
    ss = s[ok] if maior_melhor else -s[ok]
    lo, hi = float(np.min(ss)), float(np.max(ss))
    amplitude = hi - lo
    normalizado = (ss - lo) / amplitude if amplitude > 1e-12 else np.ones_like(ss)
    dentro = normalizado >= 1.0 - tol - 1e-12
    sel = np.sort(vv[dentro])
    todos = np.sort(vv)
    entre = todos[(todos >= sel[0]) & (todos <= sel[-1])]
    melhor = float(vv[np.lexsort((vv, -ss))[0]])
    return {
        "tolerance": tol,
        "volumes_l": [float(x) for x in sel],
        "min_volume_l": float(sel[0]),
        "max_volume_l": float(sel[-1]),
        "best_volume_l": melhor,
        "contiguous": bool(len(entre) == len(sel)),
    }


def volumes_da_faixa(faixa: Optional[Dict[str, Any]]) -> str:
    """Os volumes da faixa, sem a unidade: «2000–3000», «2000» (um volume só) ou «1000, 3000» (com lacunas)."""
    if not faixa:
        return ""
    volumes = faixa.get("volumes_l") or [faixa["min_volume_l"]]
    if len(volumes) == 1 or faixa["min_volume_l"] == faixa["max_volume_l"]:
        return f"{faixa['min_volume_l']:.0f}"
    if not faixa.get("contiguous", True):
        return ", ".join(f"{v:.0f}" for v in volumes)
    return f"{faixa['min_volume_l']:.0f}–{faixa['max_volume_l']:.0f}"


def faixa_de_um_volume(faixa: Optional[Dict[str, Any]]) -> bool:
    """A faixa tem um volume só: nenhum outro fica perto o bastante do maior escore."""
    return bool(faixa) and len(faixa.get("volumes_l") or [faixa["min_volume_l"]]) == 1


def pesos_somados_por_eixo(pesos_dos_criterios: Sequence[float]) -> Tuple[float, float, float, float]:
    """Os oito pesos de critério somados nos quatro eixos (técnico, econômico, ambiental, estrutural)."""
    w = [float(x) for x in pesos_dos_criterios]
    if len(w) != len(CRITERION_KEYS):
        raise ValueError(_SETE_CRITERIOS if len(w) == 7 else f"esperados {len(CRITERION_KEYS)} pesos de critério, recebidos {len(w)}")
    return tuple(sum(w[i] for i in indices) for indices in _EIXOS)  # type: ignore[return-value]


def calculate_topsis_scores(
    candidates: List[TopsisCandidate],
    weights: Optional[Sequence[float]] = None,
    parts: Optional[Sequence[float]] = None,
) -> Optional[TopsisResult]:
    """Classifica alternativas pelos oito critérios técnicos/econômicos/ambientais/estruturais.

    ``weights``: quatro pesos de dimensão (repartidos pelas ``parts``), oito pesos de critério ou
    «critic» (pesos objetivos calculados da própria matriz; ver ``pesos_critic``).
    ``parts``: oito partes no eixo; ``None`` usa ``PARTES_NO_EIXO_PADRAO`` (ignoradas com «critic»).
    """
    if not candidates:
        return None

    n = len(candidates)
    matrix = _decision_matrix(candidates)
    volumes = np.asarray([float(c.lower_tank_vol) for c in candidates])
    criterion_weights = _pesos_da_decisao(weights, parts, matrix, volumes)

    # Candidatos com volume > 0 representam sistemas pluviais reais instaláveis
    pos_mask = volumes > 0
    if np.any(pos_mask):
        pos_indices = np.where(pos_mask)[0]

        # 1. Ótimo Técnico: prioriza o volume determinado pelo threshold (se marcado no candidato),
        # ou o menor volume onde o threshold foi atingido, senão a maior confiabilidade volumétrica
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
        # Empate favorece maior economia financeira líquida e menor volume
        sort_fin = np.lexsort((volumes[pos_indices], -matrix[pos_indices, 2], matrix[pos_indices, 4]))
        fin_best_idx = int(pos_indices[sort_fin[0]])

        # 3. Ótimo Ambiental: menor impacto líquido de ciclo de vida (maior offset de CO2) entre volumes > 0
        sort_env = np.lexsort((volumes[pos_indices], matrix[pos_indices, 5]))
        env_best_idx = int(pos_indices[sort_env[0]])
    else:
        tech_best_idx = int(np.lexsort((volumes, -matrix[:, 0]))[0])
        fin_best_idx = int(np.lexsort((volumes, -matrix[:, 2], matrix[:, 4]))[0])
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


#: Pesos dos grupos quando nada se declara: 4 dimensões (25% cada)
PESOS_PADRAO = (0.25, 0.25, 0.25, 0.25)


def candidato_dos_resultados(sim, econ, co2_evitado_kg_vida: float, massa_seca_kg: Optional[float] = None,
                             **extras) -> TopsisCandidate:
    """A alternativa do multicritério montada dos resultados do programa.

    ``sim``: resultado da simulação (``SingleTankSimulationResult``); ``econ``: resultado
    econômico mensal (``run_economic_analysis``) ou anual (``run_robust_economic_analysis``);
    ``co2_evitado_kg_vida``: CO₂e líquido evitado na vida útil; ``massa_seca_kg``: massa a seco
    do sistema (sem ela, a calculadora de peso com a configuração padrão). ``extras`` vai direto
    ao candidato (``upper_tank_vol``, ``technical_threshold_met``...). É a mesma montagem da linha
    de comando e da interface, para que manual e testes vejam os números do programa.
    """
    vol = float(sim.lower_tank_vol)
    vpl = float(econ.vpl)
    if hasattr(econ, "payback_discounted_years"):
        pb = econ.payback_discounted_years
    else:
        pb = econ.payback_years
    irr = getattr(econ, "tir_annual_pct", None)
    if irr is None:
        irr = getattr(econ, "tir_pct", None)
    capex = getattr(econ, "capex_total", None)
    if capex is None:
        capex = getattr(econ, "total_investment", 0.0)
    return TopsisCandidate(
        lower_tank_vol=vol,
        water_saved_m3_yr=sim.annual_pluvial_consumed_m3,
        vpl_brl=vpl,
        co2_saved_kg_lifetime=float(co2_evitado_kg_vida),
        capex_brl=float(capex or 0.0),
        potential_savings_pct=sim.potential_potable_savings_pct,
        overflow_m3_yr=sim.annual_spill_m3,
        discounted_payback_years=payback_do_criterio(pb, vpl) if vol > 0 else None,
        irr_pct=irr,
        potable_consumed_m3_yr=sim.annual_potable_consumed_m3,
        volumetric_reliability_pct=sim.volumetric_reliability_pct,
        storage_efficiency_pct=sim.storage_efficiency_pct,
        net_financial_savings_brl=vpl,
        lcow_brl_m3=econ.lcow_per_m3 if vol > 0 else None,
        material_mass_kg=massa_seca_kg,
        **extras,
    )


def payback_do_criterio(payback_descontado_anos, vpl_brl) -> "Optional[float]":
    """Payback descontado que entra no multicritério, ou None.

    Só existe payback de um investimento que se paga: com payback nulo ou
    ausente (a alternativa sem cisterna) ou com VPL não positivo, o critério
    recebe None.
    """
    if payback_descontado_anos is None or vpl_brl is None:
        return None
    if payback_descontado_anos <= 0 or vpl_brl <= 0:
        return None
    return float(payback_descontado_anos)
