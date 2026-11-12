# -*- coding: utf-8 -*-
"""Calculadora de peso e cargas estruturais do sistema pluvial.

Calcula a massa a seco (peso próprio permanente de reservatórios, tubulações,
equipamentos e acessórios), a carga hidrostática máxima de água em operação
e a carga total solicitada à estrutura da edificação, discriminada por posição
física:
  - Subsolo / Nível Inferior: cisterna inferior, motobomba, quadro elétrico,
    dispositivos de descarte e conexões de base.
  - Cobertura / Nível Superior: reservatório superior, barrilete superior,
    dispositivo de separação atmosférica (air gap) e conexões de topo.
  - Prumadas e Rede: tubulações de sucção, recalque e distribuição,
    conexões e curvas entre níveis.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from triton.core.lca.environmental import (
    MATERIAL_PRESETS,
    PIPE_LINEAR_MASS_KG_PER_M,
    PUMP_MASS_KG,
    PipeInput,
    PumpInput,
    massa_do_reservatorio_kg,
    normalize_material_key,
)

DENSIDADE_AGUA_KG_L: float = 1.0  # 1.0 kg/L = 1000 kg/m³
ACELERACAO_GRAVIDADE_M_S2: float = 9.80665

#: Limiares de atenção do programa para os alertas (não são limites de norma).
LIMIAR_COBERTURA_KG: float = 500.0
LIMIAR_RESERVATORIO_SUPERIOR_L: float = 1500.0
LIMIAR_SUBSOLO_SECO_KG: float = 3000.0

ZONE_SUBSOLO: str = "subsolo"
ZONE_SUPERIOR: str = "superior"
ZONE_REDE: str = "rede"

ZONE_LABELS: Dict[str, str] = {
    ZONE_SUBSOLO: "Subsolo / Nível Inferior",
    ZONE_SUPERIOR: "Cobertura / Nível Superior",
    ZONE_REDE: "Prumadas e Rede",
}



def _rotulo(zona: str) -> str:
    """O nome da zona no idioma da edição."""
    from triton.cli_textos import t as _t
    return _t(ZONE_LABELS[zona])


@dataclass
class ComponentWeight:
    """Peso de um componente do sistema com discriminação de carga seca e de água."""

    name: str
    category: str
    zone: str
    zone_label: str
    dry_mass_kg: float
    water_capacity_l: float
    water_mass_kg: float
    total_operating_mass_kg: float
    total_operating_weight_kn: float
    details: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ZoneWeightBreakdown:
    """Consolidação das cargas para uma posição física/estrutural."""

    zone: str
    zone_label: str
    dry_mass_kg: float
    water_mass_kg: float
    total_operating_mass_kg: float
    total_operating_weight_kn: float
    pct_of_total_mass: float = 0.0
    components: List[ComponentWeight] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["components"] = [c.to_dict() if hasattr(c, "to_dict") else c for c in self.components]
        return data


@dataclass
class SystemWeightResult:
    """Resultado consolidado da calculadora de peso do sistema."""

    total_dry_mass_kg: float
    total_water_mass_kg: float
    total_operating_mass_kg: float
    total_operating_weight_kn: float
    substructure: ZoneWeightBreakdown
    superstructure: ZoneWeightBreakdown
    network: ZoneWeightBreakdown
    components: List[ComponentWeight] = field(default_factory=list)
    structural_alerts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_dry_mass_kg": round(self.total_dry_mass_kg, 2),
            "total_water_mass_kg": round(self.total_water_mass_kg, 2),
            "total_operating_mass_kg": round(self.total_operating_mass_kg, 2),
            "total_operating_weight_kn": round(self.total_operating_weight_kn, 3),
            "substructure": self.substructure.to_dict(),
            "superstructure": self.superstructure.to_dict(),
            "network": self.network.to_dict(),
            "components": [c.to_dict() for c in self.components],
            "structural_alerts": list(self.structural_alerts),
        }


def _pipe_internal_diameter_m(dn_mm: float) -> float:
    """Estima o diâmetro interno útil da tubulação a partir do DN comercial em PVC."""
    dn = float(dn_mm)
    tab = {
        20: 0.016, 25: 0.0216, 32: 0.0278, 40: 0.0352, 50: 0.044,
        60: 0.053, 75: 0.067, 85: 0.076, 100: 0.095, 110: 0.105,
        150: 0.143, 200: 0.190,
    }
    return tab.get(int(dn), max(0.010, (dn * 0.90) / 1000.0))


def calculate_system_weight(
    lower_tank_vol_l: float,
    lower_material_key: str = "PEAD",
    upper_tank_vol_l: float = 0.0,
    upper_material_key: str = "PEAD",
    pipes: Optional[Sequence[Any]] = None,
    pump_power_cv: Optional[float] = 0.5,
    pump_count: int = 1,
    first_flush_enabled: bool = False,
    first_flush_vol_l: float = 0.0,
    custom_lower_density: Optional[float] = None,
    custom_upper_density: Optional[float] = None,
    itens_do_arranjo: Optional[Sequence[Tuple[str, str, float, float, str]]] = None,
) -> SystemWeightResult:
    """Calcula detalhadamente as cargas estruturais do sistema pluvial.

    Parâmetros:
      - lower_tank_vol_l: Volume da cisterna inferior em litros.
      - lower_material_key: Material da cisterna (PEAD, CONCRETO, FIBRA, ACO).
      - upper_tank_vol_l: Volume da caixa d'água superior em litros.
      - upper_material_key: Material da caixa d'água superior.
      - pipes: Lista de trechos de tubulação (PipeInput ou dicionários com diameter_mm e length_m).
      - pump_power_cv: Potência da motobomba em CV (ex: 0.5, 0.75, 1.0, 1.5, 2.0, 3.0).
      - pump_count: Quantidade de bombas (padrão 1).
      - first_flush_enabled: Se há descarte de primeiras águas.
      - first_flush_vol_l: Volume do descarte em litros.
      - custom_lower_density: Densidade personalizada do material inferior (kg/m³).
      - custom_upper_density: Densidade personalizada do material superior (kg/m³).
      - itens_do_arranjo: Componentes adicionais do arranjo 3D (quantitativo).
    """
    components: List[ComponentWeight] = []
    alerts: List[str] = []

    v_low = max(0.0, float(lower_tank_vol_l or 0.0))
    v_up = max(0.0, float(upper_tank_vol_l or 0.0))

    # 1. Cisterna Inferior (Zona Subsolo)
    norm_mat_low = normalize_material_key(lower_material_key, "PEAD")
    if v_low > 0:
        den_low = custom_lower_density if (custom_lower_density and custom_lower_density > 0) else MATERIAL_PRESETS[norm_mat_low].material_density_kg_per_m3_tank
        dry_low = float(massa_do_reservatorio_kg(v_low, norm_mat_low, den_low))
        w_low = v_low * DENSIDADE_AGUA_KG_L
        tot_low = dry_low + w_low
        kn_low = tot_low * ACELERACAO_GRAVIDADE_M_S2 / 1000.0

        components.append(ComponentWeight(
            name=f"Cisterna Inferior ({norm_mat_low}, {v_low:,.0f} L)".replace(",", "."),
            category="cisterna",
            zone=ZONE_SUBSOLO,
            zone_label=_rotulo(ZONE_SUBSOLO),
            dry_mass_kg=round(dry_low, 2),
            water_capacity_l=round(v_low, 2),
            water_mass_kg=round(w_low, 2),
            total_operating_mass_kg=round(tot_low, 2),
            total_operating_weight_kn=round(kn_low, 3),
            details=f"Densidade de material: {den_low:.1f} kg/m³ útil. Carga permanente + acidental da água.",
        ))

        # Acessórios de base da cisterna
        acc_dry = 3.0  # Freio d'água (0.6kg) + Ladrão sifonado (1.5kg) + Válvula crivo (0.3kg) + Chave nível (0.4kg) + Registro (0.2kg)
        components.append(ComponentWeight(
            name="Acessórios e Conexões da Cisterna",
            category="acessorios",
            zone=ZONE_SUBSOLO,
            zone_label=_rotulo(ZONE_SUBSOLO),
            dry_mass_kg=acc_dry,
            water_capacity_l=0.0,
            water_mass_kg=0.0,
            total_operating_mass_kg=acc_dry,
            total_operating_weight_kn=round(acc_dry * ACELERACAO_GRAVIDADE_M_S2 / 1000.0, 3),
            details="Freio d'água DN 100, ladrão sifonado, válvula de sucção com crivo e sensor de nível.",
        ))

    # 2. Reservatório Superior (Zona Superior / Cobertura)
    norm_mat_up = normalize_material_key(upper_material_key, "PEAD")
    if v_up > 0:
        den_up = custom_upper_density if (custom_upper_density and custom_upper_density > 0) else MATERIAL_PRESETS[norm_mat_up].material_density_kg_per_m3_tank
        dry_up = float(massa_do_reservatorio_kg(v_up, norm_mat_up, den_up))
        w_up = v_up * DENSIDADE_AGUA_KG_L
        tot_up = dry_up + w_up
        kn_up = tot_up * ACELERACAO_GRAVIDADE_M_S2 / 1000.0

        components.append(ComponentWeight(
            name=f"Reservatório Superior ({norm_mat_up}, {v_up:,.0f} L)".replace(",", "."),
            category="reservatorio_superior",
            zone=ZONE_SUPERIOR,
            zone_label=_rotulo(ZONE_SUPERIOR),
            dry_mass_kg=round(dry_up, 2),
            water_capacity_l=round(v_up, 2),
            water_mass_kg=round(w_up, 2),
            total_operating_mass_kg=round(tot_up, 2),
            total_operating_weight_kn=round(kn_up, 3),
            details=f"Densidade de material: {den_up:.1f} kg/m³ útil. Carga atuante sobre a laje de cobertura.",
        ))

        # Acessórios de topo
        acc_up_dry = 1.0  # Air gap (0.4kg) + Chave de nível (0.4kg) + Registro (0.2kg)
        components.append(ComponentWeight(
            name="Acessórios do Reservatório Superior",
            category="acessorios",
            zone=ZONE_SUPERIOR,
            zone_label=_rotulo(ZONE_SUPERIOR),
            dry_mass_kg=acc_up_dry,
            water_capacity_l=0.0,
            water_mass_kg=0.0,
            total_operating_mass_kg=acc_up_dry,
            total_operating_weight_kn=round(acc_up_dry * ACELERACAO_GRAVIDADE_M_S2 / 1000.0, 3),
            details="Separação atmosférica (air gap), boia/chave de nível e registros do barrilete.",
        ))

    # 3. Conjunto Motobomba (Zona Subsolo)
    if v_low > 0 and pump_power_cv is not None and float(pump_power_cv) > 0:
        cv = float(pump_power_cv)
        n_pumps = max(1, int(pump_count or 1))
        unit_pump_mass = PUMP_MASS_KG.get(cv, 10.5)
        dry_pump = unit_pump_mass * n_pumps
        w_pump = 2.0 * n_pumps  # Água na voluta
        tot_pump = dry_pump + w_pump
        kn_pump = tot_pump * ACELERACAO_GRAVIDADE_M_S2 / 1000.0

        components.append(ComponentWeight(
            name=f"Motobomba de Recalque ({cv:.2f} CV, {n_pumps} un.)".replace(".00", ""),
            category="motobomba",
            zone=ZONE_SUBSOLO,
            zone_label=_rotulo(ZONE_SUBSOLO),
            dry_mass_kg=round(dry_pump, 2),
            water_capacity_l=round(w_pump, 2),
            water_mass_kg=round(w_pump, 2),
            total_operating_mass_kg=round(tot_pump, 2),
            total_operating_weight_kn=round(kn_pump, 3),
            details=f"Massa de catálogo Dancor 60 Hz (linha CAM W). {n_pumps} bomba(s) com quadro elétrico.",
        ))

        # Quadro de comando e válvulas da casa de bombas
        q_dry = 4.6  # Quadro (3.5kg) + Válvula retenção (0.5kg) + Solenoide (0.6kg)
        components.append(ComponentWeight(
            name="Quadro Elétrico e Válvulas do Recalque",
            category="acessorios",
            zone=ZONE_SUBSOLO,
            zone_label=_rotulo(ZONE_SUBSOLO),
            dry_mass_kg=q_dry,
            water_capacity_l=0.0,
            water_mass_kg=0.0,
            total_operating_mass_kg=q_dry,
            total_operating_weight_kn=round(q_dry * ACELERACAO_GRAVIDADE_M_S2 / 1000.0, 3),
            details="Quadro de proteção/comando, válvula de retenção e válvula solenoide.",
        ))

    # 4. Descarte Inicial / First Flush (Zona Subsolo)
    if v_low > 0 and first_flush_enabled and first_flush_vol_l > 0:
        ff_vol = float(first_flush_vol_l)
        ff_dry = 6.0 + 0.05 * ff_vol  # Reservatório de descarte com válvula de purga
        ff_filter = 3.0  # Filtro pluvial autolimpante
        dry_ff_tot = ff_dry + ff_filter
        w_ff = ff_vol * DENSIDADE_AGUA_KG_L
        tot_ff = dry_ff_tot + w_ff
        kn_ff = tot_ff * ACELERACAO_GRAVIDADE_M_S2 / 1000.0

        components.append(ComponentWeight(
            name=f"Subsistema de Descarte Inicial / First Flush ({ff_vol:,.0f} L)".replace(",", "."),
            category="descarte",
            zone=ZONE_SUBSOLO,
            zone_label=_rotulo(ZONE_SUBSOLO),
            dry_mass_kg=round(dry_ff_tot, 2),
            water_capacity_l=round(ff_vol, 2),
            water_mass_kg=round(w_ff, 2),
            total_operating_mass_kg=round(tot_ff, 2),
            total_operating_weight_kn=round(kn_ff, 3),
            details="Filtro de folhas autolimpante e coluna de descarte inicial com válvula de purga.",
        ))

    # 5. Tubulações e Prumadas (Zona Rede)
    pipe_list = list(pipes or [])
    if not pipe_list and v_low > 0:
        # Tubulações padrão da instalação pluvial
        pipe_list = [
            PipeInput(diameter_mm=100, length_m=20.0),  # Captação / Extravasor
            PipeInput(diameter_mm=32, length_m=20.0),   # Recalque vertical
            PipeInput(diameter_mm=40, length_m=5.0),    # Sucção / Barrilete
        ]

    for p in pipe_list:
        if isinstance(p, dict):
            dn = int(p.get("diameter_mm", 100))
            length = float(p.get("length_m", 0.0))
        elif hasattr(p, "diameter_mm") and hasattr(p, "length_m"):
            dn = int(p.diameter_mm)
            length = float(p.length_m)
        else:
            continue

        if length <= 0:
            continue

        lin_mass = PIPE_LINEAR_MASS_KG_PER_M.get(dn, (dn / 1000.0)**2 * 245.0)
        p_dry = length * lin_mass
        di_m = _pipe_internal_diameter_m(dn)
        p_water_l = (math.pi * (di_m / 2.0)**2 * length) * 1000.0
        p_water_kg = p_water_l * DENSIDADE_AGUA_KG_L
        p_tot = p_dry + p_water_kg
        p_kn = p_tot * ACELERACAO_GRAVIDADE_M_S2 / 1000.0

        components.append(ComponentWeight(
            name=f"Tubulação PVC DN {dn} ({length:.1f} m)",
            category="tubulacao",
            zone=ZONE_REDE,
            zone_label=_rotulo(ZONE_REDE),
            dry_mass_kg=round(p_dry, 2),
            water_capacity_l=round(p_water_l, 2),
            water_mass_kg=round(p_water_kg, 2),
            total_operating_mass_kg=round(p_tot, 2),
            total_operating_weight_kn=round(p_kn, 3),
            details=f"Massa linear {lin_mass:.3f} kg/m; volume interno retido {p_water_l:.1f} L.",
        ))

    # 6. Itens adicionais do quantitativo do arranjo 3D
    if itens_do_arranjo:
        for categoria, quantidade, massa_kg, _, fonte in itens_do_arranjo:
            massa = float(massa_kg or 0.0)
            if massa <= 0:
                continue
            cat_lower = categoria.lower()
            if any(k in cat_lower for k in ("superior", "air gap", "caixa")):
                zone = ZONE_SUPERIOR
            elif any(k in cat_lower for k in ("cisterna", "bomba", "succao", "pocinho", "descarte")):
                zone = ZONE_SUBSOLO
            else:
                zone = ZONE_REDE

            components.append(ComponentWeight(
                name=f"Arranjo: {categoria} ({quantidade})",
                category="acessorios",
                zone=zone,
                zone_label=ZONE_LABELS[zone],
                dry_mass_kg=round(massa, 2),
                water_capacity_l=0.0,
                water_mass_kg=0.0,
                total_operating_mass_kg=round(massa, 2),
                total_operating_weight_kn=round(massa * ACELERACAO_GRAVIDADE_M_S2 / 1000.0, 3),
                details=f"Item do quantitativo do arranjo 3D. Origem: {fonte}",
            ))

    # Agregação por Zonas
    sub_comps = [c for c in components if c.zone == ZONE_SUBSOLO]
    sup_comps = [c for c in components if c.zone == ZONE_SUPERIOR]
    net_comps = [c for c in components if c.zone == ZONE_REDE]

    def _aggregate_zone(zone_code: str, comps: List[ComponentWeight]) -> ZoneWeightBreakdown:
        dry = sum(c.dry_mass_kg for c in comps)
        water = sum(c.water_mass_kg for c in comps)
        tot = dry + water
        kn = tot * ACELERACAO_GRAVIDADE_M_S2 / 1000.0
        return ZoneWeightBreakdown(
            zone=zone_code,
            zone_label=_rotulo(zone_code),
            dry_mass_kg=round(dry, 2),
            water_mass_kg=round(water, 2),
            total_operating_mass_kg=round(tot, 2),
            total_operating_weight_kn=round(kn, 3),
            components=comps,
        )

    substructure = _aggregate_zone(ZONE_SUBSOLO, sub_comps)
    superstructure = _aggregate_zone(ZONE_SUPERIOR, sup_comps)
    network = _aggregate_zone(ZONE_REDE, net_comps)

    total_dry = round(substructure.dry_mass_kg + superstructure.dry_mass_kg + network.dry_mass_kg, 2)
    total_water = round(substructure.water_mass_kg + superstructure.water_mass_kg + network.water_mass_kg, 2)
    total_operating = round(total_dry + total_water, 2)
    total_kn = round(total_operating * ACELERACAO_GRAVIDADE_M_S2 / 1000.0, 3)

    if total_operating > 0:
        substructure.pct_of_total_mass = round((substructure.total_operating_mass_kg / total_operating) * 100.0, 1)
        superstructure.pct_of_total_mass = round((superstructure.total_operating_mass_kg / total_operating) * 100.0, 1)
        network.pct_of_total_mass = round((network.total_operating_mass_kg / total_operating) * 100.0, 1)

    # 7. Alertas: limiares de atenção do próprio programa (não são limites de norma).
    # Indicam quando vale confirmar a carga com o projeto estrutural ou de fundações.
    from triton.cli_textos import t as _t
    from triton.core.numero import formatar
    if superstructure.total_operating_mass_kg >= LIMIAR_COBERTURA_KG:
        alerts.append(_t(
            "Carga no nível superior: com o reservatório cheio, {0} kg ({1} kN) sobre a cobertura, acima do "
            "limiar de atenção do programa ({2} kg). Confirme o apoio com o projeto estrutural."
        ).format(formatar(superstructure.total_operating_mass_kg, 0), formatar(superstructure.total_operating_weight_kn, 2),
                 formatar(LIMIAR_COBERTURA_KG, 0)))
    if v_up > LIMIAR_RESERVATORIO_SUPERIOR_L:
        alerts.append(_t(
            "Reservatório superior de {0} L: acima de {1} L, confirme com o projeto estrutural a base de apoio na cobertura."
        ).format(formatar(v_up, 0), formatar(LIMIAR_RESERVATORIO_SUPERIOR_L, 0)))
    if substructure.dry_mass_kg >= LIMIAR_SUBSOLO_SECO_KG:
        alerts.append(_t(
            "Peso próprio da cisterna: {0} kg a seco ({1}), acima do limiar de atenção do programa ({2} kg). "
            "Confirme o apoio no solo com o projeto de fundações."
        ).format(formatar(substructure.dry_mass_kg, 0), norm_mat_low, formatar(LIMIAR_SUBSOLO_SECO_KG, 0)))
    if norm_mat_low == "CONCRETO" and v_low > 0:
        alerts.append(_t(
            "Cisterna de concreto: {0} kg a seco e {1} kg cheia. Considere essa carga no projeto de fundações."
        ).format(formatar(substructure.dry_mass_kg, 0), formatar(substructure.total_operating_mass_kg, 0)))

    return SystemWeightResult(
        total_dry_mass_kg=total_dry,
        total_water_mass_kg=total_water,
        total_operating_mass_kg=total_operating,
        total_operating_weight_kn=total_kn,
        substructure=substructure,
        superstructure=superstructure,
        network=network,
        components=components,
        structural_alerts=alerts,
    )


def calculate_system_weight_from_config(
    cfg: Any,
    lower_tank_vol_l: Optional[float] = None,
    environmental_raw: Optional[Dict[str, Any]] = None,
) -> SystemWeightResult:
    """Extrai premissas da configuração do Triton e calcula o peso completo do sistema."""
    raw = environmental_raw or {}

    v_low = float(lower_tank_vol_l if lower_tank_vol_l is not None else getattr(cfg, "lower_tank_vol", 0.0) or 0.0)
    # Material: o da etapa ambiental; sem ele, o do projeto (`lower_tank_material`, como a ACV lê).
    mat_low = (raw.get("lower_material_key") or getattr(cfg, "lower_tank_material", None)
               or getattr(cfg, "lower_material_key", None) or "PEAD")

    v_up = float(getattr(cfg, "upper_tank_vol", 0.0) or 0.0) if getattr(cfg, "upper_tank_used", True) else 0.0
    mat_up = (raw.get("upper_material_key") or getattr(cfg, "upper_tank_material", None)
              or getattr(cfg, "upper_material_key", None) or "PEAD")

    pipes_raw = raw.get("pipes")
    if pipes_raw is None:
        pipes_raw = [
            PipeInput(diameter_mm=100, length_m=20.0),
            PipeInput(diameter_mm=32, length_m=20.0),
            PipeInput(diameter_mm=40, length_m=5.0),
        ]

    pump_dict = raw.get("pump") or {}
    pump_power = float(pump_dict.get("power_cv", 0.5) if isinstance(pump_dict, dict) else getattr(pump_dict, "power_cv", 0.5))

    ff_enabled = bool(raw.get("first_flush_system_enabled", False) or (getattr(cfg, "discard", 0.0) > 0 and getattr(cfg, "discard_mode", 0) != 0))
    ff_vol = 0.0
    if ff_enabled:
        area = float(getattr(cfg, "area", 100.0) or 100.0)
        discard_mm = float(getattr(cfg, "discard", 1.0) or 1.0)
        ff_vol = area * discard_mm

    itens_arr = raw.get("itens_do_arranjo")

    return calculate_system_weight(
        lower_tank_vol_l=v_low,
        lower_material_key=mat_low,
        upper_tank_vol_l=v_up,
        upper_material_key=mat_up,
        pipes=pipes_raw,
        pump_power_cv=pump_power,
        pump_count=1,
        first_flush_enabled=ff_enabled,
        first_flush_vol_l=ff_vol,
        custom_lower_density=raw.get("custom_lower_density_kg_m3"),
        custom_upper_density=raw.get("custom_upper_density_kg_m3"),
        itens_do_arranjo=itens_arr,
    )
