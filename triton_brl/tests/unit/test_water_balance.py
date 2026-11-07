"""Suíte de Auditoria Matemática e Balanço Hídrico Auditado (Inspirado no conceito Jacobian).

Valida matematicamente o modelo comportamental geral de Latham/Fewkes com parâmetro theta:
  theta = 0 -> YAS (Yield After Spillage)
  theta = 1 -> YBS (Yield Before Spillage)
  0 < theta < 1 -> Regras operacionais intermediárias

Equações analíticas auditadas (conforme Fewkes 2000b):
  (1) Q_t = A * C * max(P_t - F, 0) * 10^-3
  (2) Y_t = min(D_t, V_(t-1) + theta * Q_t)
  (3) V_t = min(V_(t-1) + Q_t - Y_t, S - (1 - theta) * Y_t)
  (4) O_t = V_(t-1) + Q_t - Y_t - V_t
  (5) M_t = D_t - Y_t

Invariante fundamental de conservação de massa:
  Delta_V + Y_t + O_t - Q_t = 0  (com precisão estrita de máquina: residuo auditado 0,00 m³)
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence
import pytest


@dataclass(frozen=True)
class ParametrosRWH:
    area_captacao_m2: float       # A (m²)
    coef_runoff: float            # C (adimensional, 0 a 1)
    capacidade_cisterna_m3: float # S (m³)
    first_flush_mm: float = 0.0   # F (mm)
    theta: float = 0.0            # 0 = YAS, 1 = YBS
    volume_inicial_m3: float = 0.0 # V_0 (m³)

    def __post_init__(self):
        if self.area_captacao_m2 <= 0:
            raise ValueError("Área de captação deve ser estritamente positiva.")
        if not (0.0 <= self.coef_runoff <= 1.0):
            raise ValueError("Coeficiente de runoff C deve estar entre 0 e 1.")
        if self.capacidade_cisterna_m3 < 0:
            raise ValueError("Capacidade da cisterna S não pode ser negativa.")
        if not (0.0 <= self.theta <= 1.0):
            raise ValueError("Parâmetro theta deve estar entre 0 (YAS) e 1 (YBS).")
        if not (0.0 <= self.volume_inicial_m3 <= self.capacidade_cisterna_m3):
            raise ValueError("Volume inicial V_0 deve estar entre 0 e S.")


@dataclass
class ResultadoPasso:
    t: int
    chuva_mm: float
    afluente_m3: float     # Q_t
    demanda_m3: float      # D_t
    atendimento_m3: float  # Y_t (Yield)
    extravasado_m3: float  # O_t (Overflow)
    rede_publica_m3: float # M_t (Mains backup)
    volume_final_m3: float # V_t
    residuo_massa: float   # (V_(t-1) + Q_t) - (V_t + Y_t + O_t)


@dataclass
class IndicadoresDesempenho:
    total_dias: int
    chuva_total_mm: float
    afluente_total_m3: float
    demanda_total_m3: float
    atendimento_total_m3: float
    extravasamento_total_m3: float
    rede_publica_total_m3: float
    economia_agua_potavel_pct: float     # E (%)
    confiabilidade_volumetrica_pct: float # R_v (%)
    confiabilidade_temporal_pct: float   # R_t (%)
    eficiencia_armazenamento_pct: float  # eta (%)
    razao_extravasamento_pct: float      # epsilon (%)
    max_residuo_massa: float             # auditoria numérica


def simular_balanco(
    params: ParametrosRWH,
    chuva_diaria_mm: Sequence[float],
    demanda_diaria_m3: Sequence[float],
    demanda_total_edificio_m3: Sequence[float] | None = None,
) -> tuple[IndicadoresDesempenho, list[ResultadoPasso]]:
    n_dias = len(chuva_diaria_mm)
    if len(demanda_diaria_m3) != n_dias:
        raise ValueError("Comprimento da série de chuva difere da série de demanda.")

    if demanda_total_edificio_m3 is None:
        demanda_total_edificio_m3 = demanda_diaria_m3

    passos: list[ResultadoPasso] = []
    v_ant = params.volume_inicial_m3

    soma_q = 0.0
    soma_d = 0.0
    soma_dt = 0.0
    soma_y = 0.0
    soma_o = 0.0
    soma_m = 0.0
    dias_plenos = 0
    max_residuo = 0.0

    for t in range(n_dias):
        p_t = chuva_diaria_mm[t]
        d_t = demanda_diaria_m3[t]
        dt_total = demanda_total_edificio_m3[t]

        # 1. Afluente Q_t (Eq. 1)
        lamina_efetiva = max(p_t - params.first_flush_mm, 0.0)
        q_t = params.area_captacao_m2 * params.coef_runoff * lamina_efetiva * 1e-3

        # 2. Atendimento Y_t (Eq. 2)
        y_t = min(d_t, v_ant + params.theta * q_t)

        # 3. Volume armazenado V_t (Eq. 3)
        v_t = min(v_ant + q_t - y_t, params.capacidade_cisterna_m3 - (1.0 - params.theta) * y_t)
        v_t = max(v_t, 0.0)

        # 4. Extravasamento O_t (Eq. 4)
        o_t = max(v_ant + q_t - y_t - v_t, 0.0)

        # 5. Complementação da rede pública M_t (Eq. 5)
        m_t = max(d_t - y_t, 0.0)

        # Conservação estrita de massa: (V_(t-1) + Q_t) = (V_t + Y_t + O_t)
        residuo = (v_ant + q_t) - (v_t + y_t + o_t)
        if abs(residuo) > max_residuo:
            max_residuo = abs(residuo)

        if abs(residuo) > 1e-6:
            raise RuntimeError(f"Violação de conservação de massa no dia {t}: resíduo={residuo}")

        if y_t >= d_t - 1e-9 and d_t > 0:
            dias_plenos += 1

        passos.append(ResultadoPasso(
            t=t,
            chuva_mm=p_t,
            afluente_m3=q_t,
            demanda_m3=d_t,
            atendimento_m3=y_t,
            extravasado_m3=o_t,
            rede_publica_m3=m_t,
            volume_final_m3=v_t,
            residuo_massa=residuo,
        ))

        soma_q += q_t
        soma_d += d_t
        soma_dt += dt_total
        soma_y += y_t
        soma_o += o_t
        soma_m += m_t
        v_ant = v_t

    # Indicadores consolidados (Eqs. 6 a 10)
    e = (soma_y / soma_dt * 100.0) if soma_dt > 0 else 0.0
    r_v = (soma_y / soma_d * 100.0) if soma_d > 0 else 0.0
    r_t = (dias_plenos / n_dias * 100.0) if n_dias > 0 else 0.0
    eta = (soma_y / soma_q * 100.0) if soma_q > 0 else 0.0
    epsilon = (soma_o / soma_q * 100.0) if soma_q > 0 else 0.0

    indicadores = IndicadoresDesempenho(
        total_dias=n_dias,
        chuva_total_mm=sum(chuva_diaria_mm),
        afluente_total_m3=soma_q,
        demanda_total_m3=soma_d,
        atendimento_total_m3=soma_y,
        extravasamento_total_m3=soma_o,
        rede_publica_total_m3=soma_m,
        economia_agua_potavel_pct=e,
        confiabilidade_volumetrica_pct=r_v,
        confiabilidade_temporal_pct=r_t,
        eficiencia_armazenamento_pct=eta,
        razao_extravasamento_pct=epsilon,
        max_residuo_massa=max_residuo,
    )

    return indicadores, passos


# ==============================================================================
# TESTES FORMALIZADOS (PYTEST)
# ==============================================================================

def test_conservacao_de_massa_estrita_yas():
    """Valida que o balanço YAS (theta=0) conserva massa com resíduo zero absoluto."""
    params = ParametrosRWH(
        area_captacao_m2=150.0,
        coef_runoff=0.85,
        capacidade_cisterna_m3=5.0,
        first_flush_mm=2.0,
        theta=0.0,
    )
    chuvas = [0.0, 1.5, 10.0, 50.0, 0.0, 5.0, 100.0, 0.0, 0.0, 12.0]
    demandas = [0.4] * len(chuvas)

    ind, passos = simular_balanco(params, chuvas, demandas)

    assert ind.max_residuo_massa < 1e-9
    for p in passos:
        assert abs(p.residuo_massa) < 1e-9
        # Demanda = Atendimento + Complementação da rede
        assert math.isclose(p.demanda_m3, p.atendimento_m3 + p.rede_publica_m3, abs_tol=1e-9)


def test_conservacao_de_massa_estrita_ybs():
    """Valida que o balanço YBS (theta=1) conserva massa com resíduo zero absoluto."""
    params = ParametrosRWH(
        area_captacao_m2=150.0,
        coef_runoff=0.85,
        capacidade_cisterna_m3=5.0,
        first_flush_mm=2.0,
        theta=1.0,
    )
    chuvas = [0.0, 1.5, 10.0, 50.0, 0.0, 5.0, 100.0, 0.0, 0.0, 12.0]
    demandas = [0.4] * len(chuvas)

    ind, passos = simular_balanco(params, chuvas, demandas)

    assert ind.max_residuo_massa < 1e-9
    for p in passos:
        assert abs(p.residuo_massa) < 1e-9


def test_conservacao_de_massa_estrita_intermediaria():
    """Valida regras intermediárias (0 < theta < 1) com conservação de massa estrita."""
    for theta in [0.25, 0.5, 0.75]:
        params = ParametrosRWH(
            area_captacao_m2=200.0,
            coef_runoff=0.9,
            capacidade_cisterna_m3=3.0,
            first_flush_mm=1.0,
            theta=theta,
        )
        chuvas = [20.0, 0.0, 40.0, 5.0, 80.0, 0.0]
        demandas = [0.6] * len(chuvas)

        ind, _ = simular_balanco(params, chuvas, demandas)
        assert ind.max_residuo_massa < 1e-9


def test_relacao_teorica_ybs_maior_ou_igual_yas():
    """Teorema de Jenkins/Fewkes: YBS sempre atende igual ou mais que YAS sob mesma série."""
    chuvas = [0.0, 5.0, 20.0, 0.0, 15.0, 50.0, 2.0, 0.0, 30.0]
    demandas = [0.5] * len(chuvas)

    params_yas = ParametrosRWH(area_captacao_m2=100.0, coef_runoff=0.8, capacidade_cisterna_m3=2.0, theta=0.0)
    params_ybs = ParametrosRWH(area_captacao_m2=100.0, coef_runoff=0.8, capacidade_cisterna_m3=2.0, theta=1.0)

    ind_yas, _ = simular_balanco(params_yas, chuvas, demandas)
    ind_ybs, _ = simular_balanco(params_ybs, chuvas, demandas)

    assert ind_ybs.atendimento_total_m3 >= ind_yas.atendimento_total_m3 - 1e-9
    assert ind_ybs.economia_agua_potavel_pct >= ind_yas.economia_agua_potavel_pct - 1e-9


def test_indicadores_adimensionais_coerencia():
    """Valida que soma de eficiência de armazenamento (eta) + extravasamento (epsilon) não excede afluente."""
    params = ParametrosRWH(area_captacao_m2=100.0, coef_runoff=0.8, capacidade_cisterna_m3=2.0, theta=0.0)
    chuvas = [10.0, 20.0, 30.0, 40.0, 50.0]
    demandas = [0.5] * len(chuvas)

    ind, _ = simular_balanco(params, chuvas, demandas)

    assert 0.0 <= ind.economia_agua_potavel_pct <= 100.0
    assert 0.0 <= ind.confiabilidade_volumetrica_pct <= 100.0
    assert 0.0 <= ind.confiabilidade_temporal_pct <= 100.0
    # eta + epsilon <= 100% (com o restante retido no reservatório)
    assert ind.eficiencia_armazenamento_pct + ind.razao_extravasamento_pct <= 100.0 + 1e-6


def test_subtracao_first_flush_descarte_inicial():
    """Valida a equação canônica Q_t = A * C * max(P_t - F, 0) * 10^-3."""
    params = ParametrosRWH(
        area_captacao_m2=100.0,
        coef_runoff=0.8,
        capacidade_cisterna_m3=10.0,
        first_flush_mm=2.0,
        theta=0.0,
    )
    # Dia 1: chuva 1.5 mm <= 2.0 mm -> afluente deve ser 0
    # Dia 2: chuva 5.0 mm > 2.0 mm -> efetivo = 3.0 mm -> 100 * 0.8 * 3.0 / 1000 = 0.24 m³
    chuvas = [1.5, 5.0]
    demandas = [0.1, 0.1]

    _, passos = simular_balanco(params, chuvas, demandas)

    assert passos[0].afluente_m3 == 0.0
    assert math.isclose(passos[1].afluente_m3, 0.24, abs_tol=1e-9)


def test_validacao_parametros_fisicos_invalidos():
    """Valida que entradas fisicamente inconsistentes disparam ValueError explicativo."""
    with pytest.raises(ValueError, match="Área de captação"):
        ParametrosRWH(area_captacao_m2=-10.0, coef_runoff=0.8, capacidade_cisterna_m3=5.0)

    with pytest.raises(ValueError, match="runoff"):
        ParametrosRWH(area_captacao_m2=100.0, coef_runoff=1.5, capacidade_cisterna_m3=5.0)

    with pytest.raises(ValueError, match="cisterna"):
        ParametrosRWH(area_captacao_m2=100.0, coef_runoff=0.8, capacidade_cisterna_m3=-2.0)

    with pytest.raises(ValueError, match="theta"):
        ParametrosRWH(area_captacao_m2=100.0, coef_runoff=0.8, capacidade_cisterna_m3=5.0, theta=1.2)


def test_aviso_limite_fisico_demanda_volume():
    """Valida que a simulação dispara PhysicalLimitWarning quando D/S > 0.7 e silencia quando D/S <= 0.7."""
    from triton.core.simulation import validar_parametros_fisicos, PhysicalLimitWarning

    # Caso 1: D_pluvial = 1000 * 0.4 = 400 L/dia, S = 500 L -> D/S = 0.8 > 0.7 (Deve disparar warning)
    with pytest.warns(PhysicalLimitWarning, match="D/S = 0.80 > 0,7"):
        validar_parametros_fisicos(
            lower_tank_vol=500.0,
            area=100.0,
            runoff_coeff=0.8,
            discard_mm=1.0,
            total_demand_per_day=1000.0,
            rainwater_share=0.4,
        )

    # Caso 2: D_pluvial = 1000 * 0.4 = 400 L/dia, S = 1000 L -> D/S = 0.4 <= 0.7 (Não deve disparar warning)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("error", category=PhysicalLimitWarning)
        validar_parametros_fisicos(
            lower_tank_vol=1000.0,
            area=100.0,
            runoff_coeff=0.8,
            discard_mm=1.0,
            total_demand_per_day=1000.0,
            rainwater_share=0.4,
        )
