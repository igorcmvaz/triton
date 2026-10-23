"""Envoltória dos componentes e seus pontos de conexão.

Um só lugar decide o tamanho de cada componente, para que a volumetria e os
pontos de conexão dos trechos concordem: o tubo que chega a ``RS-01:topo``
encosta exatamente no topo do prisma desenhado.

Pontos de conexão (sufixo após ``:`` na origem ou no destino de um trecho):

* ``fundo`` (ou ``base``) — centro da base; é o padrão sem sufixo;
* ``topo`` — centro do topo;
* ``sup+x``, ``sup-x``, ``sup+y``, ``sup-y`` — na lateral, a 85 % da altura,
  do lado indicado (eixos locais do componente, que giram com ``rotation_deg``);
* ``inf+x`` … ``inf-y`` — na lateral, a 12 % da altura.

Na prática: o recalque chega pelo topo ou pela lateral superior do
reservatório superior e a distribuição sai pelo fundo ou pela lateral inferior,
sem que os dois tubos disputem o mesmo ponto.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

Point = Tuple[float, float, float]

# Proporção altura/diâmetro quando o projetista não informa as dimensões:
# cisterna enterrada tende ao cubo; caixa d'água superior é baixa e larga.
TANK_HEIGHT_RATIO = {"cisterna_inferior": 1.0, "reservatorio_superior": 0.55}
_UPPER_SIDE, _LOWER_SIDE = 0.85, 0.12
PORT_NAMES = ("fundo", "base", "topo", *(f"{level}{axis}" for level in ("sup", "inf") for axis in ("+x", "-x", "+y", "-y")))


@dataclass
class Envelope:
    """Forma em planta (polígono local, anti-horário), altura e origem das medidas."""

    shape: str  # cylinder, rhombus, box
    outline: List[Tuple[float, float]]
    half_x: float
    half_y: float
    height: float
    estimated: bool = False
    capacity_l: Optional[float] = None
    diameter: Optional[float] = None


def _number(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) and number > 0 else default


def regular_polygon(radius: float, sides: int, phase: float = 0.0) -> List[Tuple[float, float]]:
    return [(radius * math.cos(phase + 2 * math.pi * i / sides), radius * math.sin(phase + 2 * math.pi * i / sides)) for i in range(sides)]


def tank_dimensions_mm(type_id: str, parameters: Dict[str, Any], fallback_volume_l: float) -> Tuple[float, float, float, bool]:
    """Diâmetro, altura, capacidade e se as dimensões foram estimadas.

    Com ``DIAMETRO_MM`` e ``ALTURA_MM`` informados, valem eles. Sem eles, o
    cilindro com a capacidade (do componente ou, na falta, a calculada pelo
    Triton) e a proporção típica do tipo: V = π·D²/4·H, H = k·D.
    """
    capacity = _number(parameters.get("CAPACIDADE_L"), None) or fallback_volume_l
    diameter = _number(parameters.get("DIAMETRO_MM"), None)
    height = _number(parameters.get("ALTURA_MM"), None)
    if diameter and height:
        return diameter, height, capacity, False
    ratio = TANK_HEIGHT_RATIO.get(type_id, 1.0)
    volume_mm3 = max(capacity, 1.0) * 1e6
    if diameter:
        return diameter, volume_mm3 / (math.pi * diameter ** 2 / 4), capacity, True
    if height:
        return math.sqrt(4 * volume_mm3 / (math.pi * height)), height, capacity, True
    diameter = (4 * volume_mm3 / (math.pi * ratio)) ** (1 / 3)
    return diameter, ratio * diameter, capacity, True


def fallback_volumes(project_data: Dict[str, Any]) -> Dict[str, float]:
    """Volumes calculados pelo Triton, usados quando o componente não informa."""
    area = _number(project_data.get("area"), 150.0) or 150.0
    discard = _number(project_data.get("discard"), 2.0) or 2.0
    return {
        "cisterna_inferior": _number(project_data.get("lower_vol"), 1000.0) or 1000.0,
        "reservatorio_superior": _number(project_data.get("upper_vol"), 1000.0) or 1000.0,
        "first_flush": max(10.0, discard * area),
    }


def component_envelope(item: Dict[str, Any], fallbacks: Optional[Dict[str, float]] = None) -> Envelope:
    type_id = item["type_id"]
    params = item.get("parameters") or {}
    if type_id in TANK_HEIGHT_RATIO:
        fallback = (fallbacks or {}).get(type_id, 1000.0)
        diameter, height, capacity, estimated = tank_dimensions_mm(type_id, params, fallback)
        r = diameter / 2
        return Envelope("cylinder", regular_polygon(r, 32), r, r, height, estimated, capacity, diameter)
    if type_id == "motobomba":
        power = _number(params.get("POTENCIA_KW"), None)
        scale = 1.0 if power is None else min(1.8, max(0.8, (power / 0.37) ** (1 / 3)))
        hx, hy = 300 * scale, 200 * scale
        return Envelope("rhombus", [(hx, 0), (0, hy), (-hx, 0), (0, -hy)], hx, hy, 320 * scale)
    if type_id == "filtro_pluvial":
        dn = _number(params.get("DN_MM"), 100.0) or 100.0
        diam = _number(params.get("DIAMETRO_MM"), None) or (320.0 if dn <= 100 else 420.0)
        h = _number(params.get("ALTURA_MM"), None) or 600.0
        r = diam / 2
        return Envelope("cylinder", regular_polygon(r, 20), r, r, h, False, None, diam)
    if type_id == "first_flush":
        vol = _number(params.get("VOLUME_L"), None) or (fallbacks or {}).get("first_flush", 300.0)
        diam = _number(params.get("DIAMETRO_MM"), None)
        alt = _number(params.get("ALTURA_MM"), None)
        if diam and alt:
            r = diam / 2
            return Envelope("cylinder", regular_polygon(r, 20), r, r, alt, False, vol, diam)
        vol_mm3 = max(vol, 10.0) * 1e6
        ratio = 3.0 if vol <= 250.0 else 1.8
        d = max(200.0, (4 * vol_mm3 / (math.pi * ratio)) ** (1 / 3))
        h = max(600.0, ratio * d)
        d = round(d / 10.0) * 10.0
        h = round(h / 10.0) * 10.0
        r = d / 2
        return Envelope("cylinder", regular_polygon(r, 20), r, r, h, True, vol, d)
    if type_id == "ponto_nao_potavel":
        return Envelope("box", regular_polygon(110.0, 4, math.pi / 4), 110 / math.sqrt(2), 110 / math.sqrt(2), 220.0)
    # Peças do arranjo normativo, dimensionadas pela bitola quando cabe.
    dn = _number(params.get("DN_MM"), None) or 25.0
    sizes = {
        "freio_dagua": (max(220.0, dn * 2.2), max(200.0, dn * 2.0)),        # curva 90° com bocal voltado para cima
        "succao_flutuante": (max(220.0, dn * 6.0), max(200.0, dn * 5.0)),   # boia com crivo suspenso
        "sensor_nivel": (120.0, 160.0),                                     # chave de nível (boia elétrica)
        "valvula_solenoide": (max(160.0, dn * 5.0), max(200.0, dn * 7.0)),  # corpo e bobina
        "hidrometro": (max(220.0, dn * 8.0), max(160.0, dn * 5.0)),         # cavalete com mostrador
        "valvula_pe_crivo": (max(160.0, dn * 4.0), max(240.0, dn * 6.0)),   # válvula de pé com o crivo abaixo
        "respiro": (max(160.0, dn * 3.2), 600.0),                           # pescoço de ganso com tela
        "quadro_comando": (450.0, 1500.0),                                  # quadro em pedestal
    }
    if type_id in sizes:
        side, height = sizes[type_id]
        height = _number(params.get("ALTURA_MM"), None) or height
        return Envelope("box", regular_polygon(side / math.sqrt(2), 4, math.pi / 4), side / 2, side / 2, height)
    side = max(140.0, (_number(params.get("DN_MM"), None) or 25.0) * 3)
    return Envelope("box", regular_polygon(side / math.sqrt(2), 4, math.pi / 4), side / 2, side / 2, side)


def split_reference(text: str) -> Tuple[str, Optional[str]]:
    """``"RS-01:topo"`` → ``("RS-01", "topo")``; sem sufixo, porta ``None``."""
    name, _, port = text.partition(":")
    return name.strip(), (port.strip().lower() or None) if _ else None


def port_position(item: Dict[str, Any], port: Optional[str], fallbacks: Optional[Dict[str, float]] = None) -> Point:
    """Coordenada do ponto de conexão; ``ValueError`` para porta desconhecida."""
    pos = item["position_mm"]
    base = (float(pos["x"]), float(pos["y"]), float(pos["z"]))
    if port in (None, "fundo", "base"):
        return base
    env = component_envelope(item, fallbacks)
    if port == "topo":
        return (base[0], base[1], base[2] + env.height)
    if port not in PORT_NAMES:
        raise ValueError(f"ponto de conexão '{port}' desconhecido (use {', '.join(PORT_NAMES)})")
    level, sign, axis = port[:3], port[3], port[4]
    offset = (env.half_x if axis == "x" else env.half_y) * (1 if sign == "+" else -1)
    local = (offset, 0.0) if axis == "x" else (0.0, offset)
    angle = math.radians(float(item.get("rotation_deg") or 0.0))
    dx = local[0] * math.cos(angle) - local[1] * math.sin(angle)
    dy = local[0] * math.sin(angle) + local[1] * math.cos(angle)
    fraction = _UPPER_SIDE if level == "sup" else _LOWER_SIDE
    return (base[0] + dx, base[1] + dy, base[2] + env.height * fraction)
