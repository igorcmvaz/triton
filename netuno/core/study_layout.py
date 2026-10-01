"""Geração de traçado 3D e componentes BIM pré-preenchidos a partir do estudo.

Permite que o projetista visualize a planta e a volumetria 3D imediatamente a
partir dos parâmetros calculados na simulação e nas diretrizes normativas
(ABNT NBR 15527:2019, ABNT NBR 5626:2020 e ABNT NBR 10844:1989), sem ter que
começar de uma tela em branco ou digitar coordenadas manualmente.

O arranjo segue o padrão dessas instalações:

1. captação do telhado, filtro pluvial autolimpante (FP-01) e descarte das
   primeiras águas — first flush (FF-01);
2. cisterna enterrada (CI-01) com entrada calma pelo freio d'água (FR-01),
   captação pela sucção flutuante (SF-01) com válvula de pé e crivo (VP-01),
   chave de nível contra marcha a seco (SN-01), respiro com tela (RP-01) e
   extravasor com ladrão sifonado (LS-01) e antirrefluxo (VR-02) para a rede
   pluvial;
3. registro de manutenção dos dois lados da motobomba (RG-03 e RG-01),
   válvula de retenção no recalque (VR-01) e quadro de comando (QC-01);
4. caixa superior não potável (RS-01) com chave de nível (SN-02), respiro com
   tela (RP-02), extravasor com descarga visível (aviso), limpeza com registro
   (RG-04) e distribuição com registro na saída (RG-05) até o ponto de
   utilização identificado (PNP-01);
5. backup potável para a falta de chuva: hidrômetro (HD-01), registro (RG-02) e
   válvula solenoide (VS-01), descarregando por separação atmosférica (AG-01).

Com duas motobombas (``pump_count``), a reserva B-02 fica em paralelo, com o seu
registro na sucção (RG-06), retenção (VR-03) e registro no recalque (RG-07),
ligada por tês às linhas da principal.

O arranjo de abastecimento (``supply_arrangement``) muda o que existe:

* **recalque** — o descrito acima;
* **pressurização** — sem caixa superior: o pressurizador leva a água direto ao
  ponto de utilização, e o backup potável desce por separação atmosférica sobre a
  própria cisterna, que ganha a boia de backup (SN-03);
* **gravidade** — sem bomba: a cisterna fica sobre uma base, acima do ponto de
  utilização, que é atendido pela saída lateral baixa com registro (RG-05); o
  backup potável desce sobre a cisterna, como na pressurização.
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Optional, Tuple

from netuno.core.component_geometry import port_position, tank_dimensions_mm
from netuno.core.cad_exporter import _extract_upper_vol, calculate_forchheimer_pumping_diameters
from netuno.core.pump_energy import CV_TO_KW
from netuno.core.supply_arrangement import GRAVIDADE, PRESSAO_DE_TRABALHO_PADRAO_M, PRESSURIZACAO, RECALQUE


def _number(value: Any, default: float = 0.0) -> float:
    if value is None or value == "" or value == "-":
        return default
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        num = float(value)
        return num if math.isfinite(num) and num > 0 else default
    except (ValueError, TypeError):
        return default


#: Distância do ralo da cobertura à borda do telhado (mm), onde nasce a captação.
RECUO_DO_RALO_MM = 300.0

#: Declividade dos trechos horizontais por gravidade: o dobro do mínimo de 0,5 %.
DECLIVIDADE_PADRAO = 0.01

#: Arranjo por gravidade: a cisterna fica sobre uma base, com o fundo acima do
#: ponto de utilização, uma torneira de serviço baixa.
BASE_DA_CISTERNA_ELEVADA_MM = 600.0
PONTO_POR_GRAVIDADE_Z_MM = 300.0


def arranjo_do_estudo(data: Dict[str, Any]) -> str:
    """Recalque, pressurização ou gravidade; o que não for declarado é recalque."""
    valor = str(data.get("supply_arrangement") or "").strip()
    return valor if valor in (PRESSURIZACAO, GRAVIDADE) else RECALQUE


def _vertical(dz: float) -> str:
    return f"sobe {dz:g}" if dz >= 0 else f"desce {-dz:g}"


def desnivel_por_gravidade(comprimento_mm: float) -> float:
    """Desnível (mm) de um trecho por gravidade: 1 % do comprimento, e ao menos 20 mm.

    Com 20 mm fixos, um trecho de mais de 4 m ficava abaixo dos 0,5 % mínimos
    (cisterna grande afasta o filtro do telhado).
    """
    return round(max(20.0, abs(comprimento_mm) * DECLIVIDADE_PADRAO), 1)

#: Potência de placa usual (kW) dos motores de catálogo, por potência em CV.
_KW_DE_PLACA = {1 / 3: 0.25, 0.5: 0.37, 0.75: 0.55, 1.0: 0.75, 1.5: 1.1, 2.0: 1.5, 3.0: 2.2}


def cv_do_rotulo(rotulo: Any) -> Optional[float]:
    """Lê «1/2», «3/4», «1», «1 1/2», «1.1/2» ou «2» como potência em CV.

    O teste por substring (``"1/2" in rotulo``) lia «1 1/2» como meio CV e
    «1/3» como 1 CV.
    """
    texto = str(rotulo or "").strip().lower().replace("cv", "").replace("hp", "").replace(",", ".").strip()
    m = re.fullmatch(r"(?:(\d+)[\s.]+)?(\d+)/(\d+)", texto)
    if m:
        inteiro, num, den = int(m.group(1) or 0), int(m.group(2)), int(m.group(3))
        return inteiro + num / den if den else None
    try:
        valor = float(texto)
    except ValueError:
        return None
    return valor if valor > 0 else None


def potencia_da_motobomba(rotulo: Any, kw_informado: float = 0.0) -> Tuple[float, float]:
    """(CV, kW) da motobomba. O kW informado prevalece; sem nada, ½ CV (0,37 kW)."""
    cv = cv_do_rotulo(rotulo)
    if kw_informado and kw_informado > 0:
        return (cv if cv else kw_informado / CV_TO_KW), kw_informado
    if cv is None:
        cv = 0.5
    kw = next((k for c, k in _KW_DE_PLACA.items() if abs(c - cv) < 1e-6), round(cv * CV_TO_KW, 2))
    return cv, kw


def generate_study_layout(project_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Gera um layout BIM 3D completo e válido baseado nos dados do estudo.

    Parâmetros considerados:
    - ``lower_vol``: volume calculado da cisterna inferior (L).
    - ``upper_vol``: volume do reservatório superior (L).
    - ``area``: área de captação da cobertura (m²).
    - ``discard``: lâmina de descarte inicial (mm; padrão 2 mm conforme NBR 15527).
    - ``floors``: número de pavimentos (padrão 2).
    - Hidráulica da motobomba e diâmetros econômicos de Forchheimer (NBR 5626).
    """
    data = dict(project_data or {})

    # Volumes dimensionados
    lower_vol = _number(data.get("lower_vol"), 5000.0)
    # Arranjo de abastecimento: só o recalque tem caixa superior, e a gravidade
    # não tem bomba. A reserva, em paralelo, vem do número de motobombas.
    arranjo = arranjo_do_estudo(data)
    com_caixa, com_bomba = arranjo == RECALQUE, arranjo != GRAVIDADE
    n_bombas = int(_number(data.get("pump_count"), 1.0)) if com_bomba else 0
    upper_vol = _extract_upper_vol(data, 1000.0)
    area = _number(data.get("area"), 150.0)
    discard = _number(data.get("discard"), 2.0)

    # Volume de descarte inicial (NBR 15527:2019 item 4.3.5)
    ff_vol = round(discard * area, 1)

    # Pavimentos e dimensões da edificação
    bldg_vol = data.get("building_volume") or {}
    floors = int(_number(data.get("floors") or bldg_vol.get("floors"), 2.0))
    floors = max(1, min(floors, 40))
    bldg_h = float(floors * 3000.0)

    # Largura e profundidade proporcionais à área de captação
    bldg_w = max(8000.0, round(math.sqrt(area * 1.5) * 1000.0 / 500.0) * 500.0)
    bldg_d = max(6000.0, round((area / (bldg_w / 1000.0)) * 1000.0 / 500.0) * 500.0)

    # Geometria dos reservatórios (NBR 15527 / NBR 5626)
    d_ci, h_ci, _, _ = tank_dimensions_mm("cisterna_inferior", {}, lower_vol)
    d_rs, h_rs, _, _ = tank_dimensions_mm("reservatorio_superior", {}, upper_vol)
    alt_ci = max(1000.0, round(h_ci / 50.0) * 50.0)
    diam_ci = max(800.0, round(d_ci / 50.0) * 50.0)
    alt_rs = max(600.0, round(h_rs / 50.0) * 50.0)
    diam_rs = max(800.0, round(d_rs / 50.0) * 50.0)

    # Diâmetros de sucção e recalque (Forchheimer / NBR 5626)
    daily_l = _number(data.get("pluv_day"), 800.0)
    pump_hp = str(data.get("pump_hp") or "1/2")
    flow_m3_h = _number(data.get("pump_flow_rate_m3_h"), 0.0)
    pumping = calculate_forchheimer_pumping_diameters(
        pump_flow_rate_m3_h=flow_m3_h,
        daily_pumped_volume_l=daily_l,
        pump_hp=pump_hp
    )
    dn_rec = float(pumping.get("dn_recalque_comercial_mm") or 25.0)
    dn_suc = float(pumping.get("dn_succao_comercial_mm") or 32.0)

    # Potência do motor: a informada em kW prevalece; o rótulo completa o que faltar.
    pump_cv, pump_kw = potencia_da_motobomba(pump_hp, _number(data.get("pump_power_kw"), 0.0))

    flow_l_min = (flow_m3_h * 1000.0 / 60.0) if flow_m3_h > 0 else 60.0
    if com_caixa:
        head_mca = round((bldg_h + alt_ci + 500.0) / 1000.0 + 4.0, 1)
    else:
        head_mca = round(PRESSAO_DE_TRABALHO_PADRAO_M + (alt_ci + 780.0) / 1000.0, 1)

    # Coordenadas dos componentes (em mm, z para cima)
    # Cisterna enterrada no recuo externo
    x_ci = -1500.0 - diam_ci / 4.0
    y_ci = 1500.0 + diam_ci / 4.0
    z_ci = -alt_ci

    # Motobomba no abrigo térreo
    x_b = 500.0
    y_b = y_ci
    z_b = 0.0

    # Reservatório superior na cobertura (barrilete sobre a laje superior)
    x_rs = min(bldg_w - 2000.0, max(3000.0, bldg_w * 0.5))
    y_rs = min(bldg_d - 2000.0, max(2500.0, bldg_d * 0.5))
    z_rs = bldg_h + 500.0

    # Filtro pluvial e reservatório de descarte na descida da prumada pluvial
    x_fp = x_ci - 1500.0
    y_fp = y_ci
    z_fp = 1200.0
    h_fp = 600.0
    if arranjo == GRAVIDADE:
        # Cisterna sobre base, abaixo do filtro e acima do ponto de utilização. Em
        # edificação baixa, o filtro sobe até perto do telhado e a base encolhe.
        z_fp = min(max(z_fp, BASE_DA_CISTERNA_ELEVADA_MM + alt_ci + 300.0), bldg_h - h_fp - 400.0)
        z_ci = min(BASE_DA_CISTERNA_ELEVADA_MM, z_fp - 300.0 - alt_ci)
    diam_fp = 320.0

    x_ff = x_fp
    y_ff = y_fp - 900.0
    z_ff = 0.0
    h_ff = 900.0
    diam_ff = 400.0

    dn_capt = 150.0 if area > 200.0 else 100.0

    components: List[Dict[str, Any]] = [
        {
            "instance_id": "FP-01",
            "type_id": "filtro_pluvial",
            "level": "Área externa / Térreo",
            "position_mm": {"x": x_fp, "y": y_fp, "z": z_fp},
            "rotation_deg": 0.0,
            "parameters": {
                "DN_MM": dn_capt,
                "MALHA_MM": 0.35,
                "EFICIENCIA_PCT": 90.0,
                "DIAMETRO_MM": diam_fp,
                "ALTURA_MM": h_fp,
                "TIPO": "Filtro Pluvial Autolimpante Vórtex (Aço Inox 304)",
            },
        },
        {
            "instance_id": "FF-01",
            "type_id": "first_flush",
            "level": "Área externa / Térreo",
            "position_mm": {"x": x_ff, "y": y_ff, "z": z_ff},
            "rotation_deg": 0.0,
            "parameters": {
                "VOLUME_L": ff_vol,
                "DESCARTE_MM": discard,
                "DIAMETRO_MM": diam_ff,
                "ALTURA_MM": h_ff,
                "MECANISMO": "Boia flutuante de vedação por esfera e válvula de purga lenta calibrada",
            },
        },
        {
            "instance_id": "CI-01",
            "type_id": "cisterna_inferior",
            "level": "Térreo / Base elevada" if arranjo == GRAVIDADE else "Subsolo / Enterrada",
            "position_mm": {"x": x_ci, "y": y_ci, "z": z_ci},
            "rotation_deg": 0.0,
            "parameters": {
                "CAPACIDADE_L": lower_vol,
                "DIAMETRO_MM": diam_ci,
                "ALTURA_MM": alt_ci,
                "MATERIAL": "PEAD rotomoldado com proteção UV",
            },
        },
        {
            "instance_id": "B-01",
            "type_id": "motobomba",
            "level": "Térreo",
            "position_mm": {"x": x_b, "y": y_b, "z": z_b},
            "rotation_deg": 0.0,
            "parameters": {
                "POTENCIA_KW": round(pump_kw, 2),
                "POTENCIA_CV": round(pump_cv, 2),
                "POTENCIA_HP_LABEL": pump_hp,
                "VAZAO_L_MIN": round(flow_l_min, 1),
                "VAZAO_M3_H": round(flow_l_min * 0.06, 2),
                "ALTURA_MCA": head_mca,
                "DN_SUCCAO_MM": dn_suc,
                "DN_RECALQUE_MM": dn_rec,
            },
        },
        {
            "instance_id": "RS-01",
            "type_id": "reservatorio_superior",
            "level": f"Cobertura (+{bldg_h/1000:.1f} m)",
            "position_mm": {"x": x_rs, "y": y_rs, "z": z_rs},
            "rotation_deg": 0.0,
            "parameters": {
                "CAPACIDADE_L": upper_vol,
                "DIAMETRO_MM": diam_rs,
                "ALTURA_MM": alt_rs,
                "MATERIAL": "Polietileno de Alta Densidade (PEAD)",
            },
        },
    ]

    components = [c for c in components
                  if (c["type_id"] != "motobomba" or com_bomba) and (c["type_id"] != "reservatorio_superior" or com_caixa)]

    # ── Arranjo normativo completo (NBR 15527:2019 e NBR 5626:2020) ──────────
    r_ci, r_rs = diam_ci / 2.0, diam_rs / 2.0
    dn_backup, dn_ext_rs, dn_limpeza = 25.0, 50.0, 40.0
    h_topo = z_rs + alt_rs
    topo_ci = z_ci + alt_ci
    cota_cobertura = f"Cobertura (+{bldg_h/1000:.1f} m)"
    nivel_ci = "Térreo / Base elevada" if arranjo == GRAVIDADE else "Subsolo / Enterrada"
    # Freio d'água no fundo da cisterna, do lado do filtro; a sucção flutuante
    # do outro lado, para a entrada e a captação não disputarem o mesmo eixo.
    x_fr = x_ci - r_ci * 0.45
    x_sf = x_ci + r_ci * 0.45
    z_sf = z_ci + alt_ci * 0.55
    # Válvula de pé com crivo pendurada abaixo da boia.
    h_vp = max(240.0, dn_suc * 6.0)
    z_vp = z_sf - h_vp - 60.0
    # Extravasor: ladrão sifonado fora da cisterna, no lado -y, abaixo da saída.
    y_ls = y_ci - r_ci - 700.0
    z_ls = min(-600.0, z_ci + alt_ci * 0.85 - 450.0)
    # Registros dos dois lados da bomba (manutenção) e retenção no recalque.
    x_rg_suc = x_b - 450.0
    x_vr, x_rg = x_b + 700.0, x_b + 1100.0
    # Backup potável: cavalete na frente do lote (y < 0), solenoide e subida até
    # o air gap — sobre a caixa superior no recalque; sem caixa, sobre a própria
    # cisterna. As peças correm em y: giro de 90°.
    if com_caixa:
        x_ag, y_ag = x_rs + r_rs * 0.35, y_rs + r_rs * 0.35
        x_pot = x_rs + 1200.0
        y_cavalete = (-1500.0, -1000.0, -500.0)
    else:
        x_ag, y_ag = x_ci + r_ci * 0.3, y_ci - r_ci * 0.35
        x_pot = x_ag + 800.0
        y_cavalete = (y_ag - 2500.0, y_ag - 2000.0, y_ag - 1500.0)

    def peca(inst, tipo, nivel, x, y, z, rot=0.0, **parametros):
        return {"instance_id": inst, "type_id": tipo, "level": nivel,
                "position_mm": {"x": x, "y": y, "z": z}, "rotation_deg": rot, "parameters": parametros}

    # Cisterna
    if com_caixa:
        funcao_sn01 = "Nível mínimo da cisterna: desliga a motobomba (marcha a seco) e libera o backup"
    elif com_bomba:
        funcao_sn01 = "Nível mínimo da cisterna: desliga o pressurizador (marcha a seco) e abre a solenoide VS-01"
    else:
        funcao_sn01 = "Nível mínimo da cisterna: abre a solenoide VS-01 do backup potável"
    components.append(peca("FR-01", "freio_dagua", nivel_ci, x_fr, y_ci, z_ci + 60.0, DN_MM=dn_capt))
    if com_bomba:
        components += [
            peca("SF-01", "succao_flutuante", nivel_ci, x_sf, y_ci, z_sf, DN_MM=dn_suc, PROFUNDIDADE_MM=150),
            peca("VP-01", "valvula_pe_crivo", nivel_ci, x_sf, y_ci, z_vp, DN_MM=dn_suc),
        ]
    components.append(peca("SN-01", "sensor_nivel", nivel_ci, x_ci, y_ci + r_ci * 0.5, z_ci + alt_ci * 0.2,
                           FUNCAO=funcao_sn01))
    if not com_caixa:
        # Sem caixa, o backup enche a própria cisterna, e só até a boia de backup:
        # sobra volume para a próxima chuva.
        components.append(peca("SN-03", "sensor_nivel", nivel_ci, x_ci - r_ci * 0.35, y_ci + r_ci * 0.45,
                               z_ci + alt_ci * 0.35,
                               FUNCAO="Cisterna, nível de backup: fecha a solenoide VS-01; o potável enche só até aqui"))
    components += [
        peca("RP-01", "respiro", "Área externa / Térreo", x_ci, y_ci - r_ci * 0.55, topo_ci, DN_MM=50, ALTURA_MM=600),
        peca("LS-01", "ladrao_sifonado", "Área externa / Enterrado", x_ci, y_ls, z_ls, DN_MM=dn_capt, MALHA_MM=0.5),
    ]

    # Casa de bombas: principal e, havendo, a reserva em paralelo, cada uma com
    # registro na sucção, retenção e registro no recalque.
    y_reserva = y_b - 900.0
    if com_bomba:
        components += [
            peca("RG-03", "registro_gaveta", "Térreo", x_rg_suc, y_b, z_b, DN_MM=dn_suc,
                 FUNCAO="Bloqueio da sucção para retirar a motobomba"),
            peca("VR-01", "valvula_retencao", "Térreo", x_vr, y_b, z_b, DN_MM=dn_rec,
                 FUNCAO="Segura a coluna de recalque quando a bomba desliga"),
            peca("RG-01", "registro_gaveta", "Térreo", x_rg, y_b, z_b, DN_MM=dn_rec,
                 FUNCAO="Bloqueio do recalque para retirar a motobomba"),
        ]
        if n_bombas >= 2:
            reserva_b = dict(next(c for c in components if c["instance_id"] == "B-01"))
            reserva_b.update(instance_id="B-02", position_mm={"x": x_b, "y": y_reserva, "z": z_b},
                             parameters=dict(reserva_b["parameters"], FUNCAO="Reserva, em paralelo e em rodízio com B-01"))
            components += [
                reserva_b,
                peca("RG-06", "registro_gaveta", "Térreo", x_rg_suc, y_reserva, z_b, DN_MM=dn_suc,
                     FUNCAO="Bloqueio da sucção da motobomba reserva"),
                peca("VR-03", "valvula_retencao", "Térreo", x_vr, y_reserva, z_b, DN_MM=dn_rec,
                     FUNCAO="Retenção no recalque da motobomba reserva"),
                peca("RG-07", "registro_gaveta", "Térreo", x_rg, y_reserva, z_b, DN_MM=dn_rec,
                     FUNCAO="Bloqueio do recalque da motobomba reserva"),
            ]
    bombas = "B-01 e B-02" if (com_bomba and n_bombas >= 2) else "B-01"
    if com_caixa:
        funcao_qc = (f"Comando da motobomba {bombas} e da solenoide VS-01 pelas chaves SN-01 (cisterna), "
                     "SN-02 (partida) e SN-03 (backup)")
    elif com_bomba:
        funcao_qc = (f"Comando do pressurizador {bombas}, que parte pelo pressostato e para no nível mínimo "
                     "(SN-01), e da solenoide VS-01: SN-01 abre, SN-03 fecha")
    else:
        funcao_qc = "Comando da solenoide VS-01 do backup potável: SN-01 abre, SN-03 fecha"
    components.append(peca("QC-01", "quadro_comando", "Térreo", x_b + 300.0, y_b + 800.0, 0.0, TENSAO_V=220,
                           FUNCAO=funcao_qc))
    if com_caixa:
        # Duas boias na caixa: a de partida (alta) chama a motobomba; a de backup
        # (baixa) só abre a solenoide se a cisterna estiver no mínimo, e o backup
        # enche só até ela — sobra volume para a próxima chuva.
        components += [
            peca("SN-02", "sensor_nivel", cota_cobertura, x_rs - r_rs * 0.4, y_rs - r_rs * 0.4, z_rs + alt_rs * 0.55,
                 FUNCAO="Caixa superior, nível de partida: liga a motobomba com água de chuva"),
            peca("SN-03", "sensor_nivel", cota_cobertura, x_rs + r_rs * 0.4, y_rs - r_rs * 0.4, z_rs + alt_rs * 0.15,
                 FUNCAO="Caixa superior, nível de backup: sem água de chuva, abre a solenoide VS-01 e enche só até aqui"),
            peca("RP-02", "respiro", cota_cobertura, x_rs - r_rs * 0.35, y_rs + r_rs * 0.35, h_topo, DN_MM=50, ALTURA_MM=350),
            peca("AG-01", "air_gap", cota_cobertura, x_ag, y_ag, h_topo, DN_MM=dn_backup, FOLGA_MM=50),
        ]
    else:
        components.append(peca("AG-01", "air_gap", "Área externa / Térreo", x_ag, y_ag, topo_ci,
                               DN_MM=dn_backup, FOLGA_MM=50))
    # Backup potável
    components += [
        peca("HD-01", "hidrometro", "Área externa / Térreo", x_pot, y_cavalete[0], 0.0, 90.0, DN_MM=dn_backup,
             VAZAO_NOMINAL_M3_H=1.5),
        peca("RG-02", "registro_gaveta", "Área externa / Térreo", x_pot, y_cavalete[1], 0.0, 90.0, DN_MM=dn_backup,
             FUNCAO="Bloqueio do ramal potável de reserva"),
        peca("VS-01", "valvula_solenoide", "Área externa / Térreo", x_pot, y_cavalete[2], 0.0, 90.0, DN_MM=dn_backup,
             TENSAO_V=220),
    ]
    por_id = {c["instance_id"]: c for c in components}
    reserva = {"cisterna_inferior": lower_vol, "reservatorio_superior": upper_vol, "first_flush": ff_vol}

    def porta(ref: str) -> Tuple[float, float, float]:
        nome, _, lado = ref.partition(":")
        return port_position(por_id[nome], lado or None, reserva)

    saida_ls = porta("LS-01:sup-y")
    antirrefluxo = (
        peca("VR-02", "valvula_retencao", "Área externa / Enterrado", saida_ls[0], saida_ls[1] - 1000.0, saida_ls[2] - 20.0,
             90.0, DN_MM=dn_capt, FUNCAO="Antirrefluxo: a rede pluvial não volta para a cisterna"))
    if not com_caixa:
        components.append(antirrefluxo)
    if com_caixa:
        # Peças que dependem das portas da caixa superior.
        saida_dist = porta("RS-01:inf-y")       # distribuição
        saida_ext_rs = porta("RS-01:sup+y")     # extravasor e aviso
        saida_limpeza = porta("RS-01:inf+x")    # limpeza
        y_rg_dist = saida_dist[1] - 350.0
        y_pnp = y_rg_dist - 250.0 - 1200.0
        components += [
            peca("RG-05", "registro_gaveta", cota_cobertura, x_rs, y_rg_dist, saida_dist[2], 90.0, DN_MM=25,
                 FUNCAO="Registro na saída de distribuição da caixa superior"),
            peca("RG-04", "registro_gaveta", cota_cobertura, saida_limpeza[0] + 400.0, y_rs, saida_limpeza[2] - 8.0,
                 DN_MM=dn_limpeza, FUNCAO="Registro da tubulação de limpeza, junto à saída do reservatório"),
            antirrefluxo,
            peca("PNP-01", "ponto_nao_potavel", "Pavimento térreo", x_rs, y_pnp, 780.0,
                 DN_MM=25, USO="Bacias sanitárias, rega e lavagem de pisos"),
        ]
    elif com_bomba:
        # Pressurização: o recalque segue direto para o ponto de utilização.
        components.append(peca("PNP-01", "ponto_nao_potavel", "Pavimento térreo", x_rg + 600.0, y_b + 1800.0, 780.0,
                               DN_MM=25, USO="Bacias sanitárias, rega e lavagem de pisos"))
    else:
        # Gravidade: saída lateral baixa da cisterna, com registro, até um ponto
        # de utilização abaixo do fundo dela.
        saida_grav = porta("CI-01:inf+x")
        components += [
            peca("RG-05", "registro_gaveta", "Área externa / Térreo", saida_grav[0] + 350.0, y_ci, saida_grav[2],
                 DN_MM=25, FUNCAO="Registro na saída de distribuição da cisterna"),
            peca("PNP-01", "ponto_nao_potavel", "Área externa / Térreo", saida_grav[0] + 1850.0, y_ci,
                 PONTO_POR_GRAVIDADE_Z_MM, DN_MM=25, USO="Rega e lavagem de pisos (torneira de serviço)"),
        ]
    por_id = {c["instance_id"]: c for c in components}

    # Do filtro ao freio d'água: sai pela lateral, corre com declividade e desce
    # pela tampa até o bocal no fundo da cisterna.
    saida_fp = porta("FP-01:sup+x")
    dx_fp_fr = x_fr - saida_fp[0]
    queda_fp_fr = desnivel_por_gravidade(dx_fp_fr)
    dz_fp_fr = (saida_fp[2] - queda_fp_fr) - porta("FR-01:topo")[2]
    # Do ralo da cobertura até a vertical do filtro.
    dx_telhado = x_fp - RECUO_DO_RALO_MM
    queda_telhado = desnivel_por_gravidade(dx_telhado)
    saida_ci, entrada_ls = porta("CI-01:sup-y"), porta("LS-01:sup+y")
    saida_vs = porta("VS-01")
    topo_ag = porta("AG-01:topo")
    laje = bldg_h + 150.0  # descarga visível sobre a laje de cobertura (aviso)

    def trecho(run_id, sistema, dn, nivel, inicio, percurso, fim):
        return {"run_id": run_id, "system": sistema, "dn_mm": dn, "material": "PVC", "level": nivel,
                "start": inicio, "route": percurso, "end": fim}

    runs: List[Dict[str, Any]] = [
        # Nasce no ralo da cobertura, junto à borda do telhado do lado do filtro,
        # e corre para fora até a vertical do filtro.
        trecho("T-01", "captacao", dn_capt, "Cobertura", {"x": RECUO_DO_RALO_MM, "y": y_fp, "z": bldg_h},
               f"d {dx_telhado:g} 0 {-queda_telhado:g}; desce {(bldg_h - queda_telhado) - (z_fp + h_fp):g}", "FP-01:topo"),
        trecho("T-02", "descarte", dn_capt, "Térreo", "FP-01:fundo",
               f"d 0 -900 -15; desce {(z_fp - 15.0) - (z_ff + h_ff):g}", "FF-01:topo"),
        trecho("T-03", "captacao", dn_capt, "Térreo", "FP-01:sup+x",
               f"d {dx_fp_fr:g} 0 {-queda_fp_fr:g}; desce {dz_fp_fr:g}", "FR-01:topo"),
    ]
    if com_bomba:
        topo_vp = porta("VP-01:topo")
        runs += [
            # Sucção: válvula de pé → sobe pela boia e pela tampa → registro → bomba.
            trecho("T-04", "succao", dn_suc, "Térreo", "VP-01:topo",
                   f"sobe {z_b - topo_vp[2]:g}; +x {x_rg_suc - x_sf:g}", "RG-03"),
            trecho("T-05", "succao", dn_suc, "Térreo", "RG-03", f"+x {x_b - x_rg_suc:g}", "B-01"),
            # Recalque: bomba → retenção → registro.
            trecho("T-06", "recalque", dn_rec, "Térreo", "B-01", f"+x {x_vr - x_b:g}", "VR-01"),
            trecho("T-07", "recalque", dn_rec, "Térreo", "VR-01", f"+x {x_rg - x_vr:g}", "RG-01"),
        ]
    if com_caixa:
        offset_rec = 900.0
        dx_shaft = (x_rs - offset_rec) - x_rg
        dy_shaft = y_rs - y_b
        dz_sobe = h_topo + 300.0
        runs += [
            trecho("T-08", "recalque", dn_rec, "Prumada", "RG-01",
                   f"+x {dx_shaft:g}; +y {dy_shaft:g}; sobe {dz_sobe:g}; +x {offset_rec:g}; desce 300", "RS-01:topo"),
            # Distribuição: saída lateral com registro, até o ponto identificado.
            trecho("T-09", "distribuicao", 25.0, "Barrilete", "RS-01:inf-y", "-y 350", "RG-05"),
            trecho("T-10", "distribuicao", 25.0, "Barrilete", "RG-05",
                   f"-y 250; desce {saida_dist[2] - 1000.0:g}; -y {y_rg_dist - 250.0 - y_pnp:g}", "PNP-01:topo"),
        ]
    elif com_bomba:
        topo_pnp, saida_rg = porta("PNP-01:topo"), porta("RG-01")
        runs.append(trecho("T-08", "distribuicao", dn_rec, "Térreo", "RG-01",
                           f"+x {topo_pnp[0] - saida_rg[0]:g}; +y {topo_pnp[1] - saida_rg[1]:g}; "
                           f"{_vertical(topo_pnp[2] - saida_rg[2])}", "PNP-01:topo"))
    else:
        topo_pnp, saida_rg = porta("PNP-01:topo"), porta("RG-05")
        runs += [
            trecho("T-09", "distribuicao", 25.0, "Térreo", "CI-01:inf+x", "+x 350", "RG-05"),
            trecho("T-10", "distribuicao", 25.0, "Térreo", "RG-05",
                   f"+x 250; {_vertical(topo_pnp[2] - saida_rg[2])}; +x {topo_pnp[0] - saida_rg[0] - 250.0:g}",
                   "PNP-01:topo"),
        ]
    dy_ext, dz_ext = entrada_ls[1] - saida_ci[1], entrada_ls[2] - saida_ci[2]
    queda_ext = desnivel_por_gravidade(dy_ext)
    if arranjo == GRAVIDADE and -dz_ext > 2.0 * queda_ext:
        # Cisterna elevada: sai com declividade e desce pela vertical até o ladrão.
        percurso_extravasor = f"d 0 {dy_ext:g} {-queda_ext:g}; desce {-dz_ext - queda_ext:g}"
    else:
        percurso_extravasor = f"d 0 {dy_ext:g} {dz_ext:g}"
    runs += [
        # Extravasor da cisterna → ladrão sifonado → antirrefluxo → rede pluvial.
        trecho("T-11", "extravasor", dn_capt, "Área externa / Enterrado", "CI-01:sup-y", percurso_extravasor, "LS-01:sup+y"),
        trecho("T-12", "extravasor", dn_capt, "Área externa / Enterrado", "LS-01:sup-y", "d 0 -1000 -20", "VR-02"),
        trecho("T-13", "extravasor", dn_capt, "Área externa / Enterrado", "VR-02", "d 0 -600 -12", None),
    ]
    if com_caixa:
        runs += [
            # Caixa superior: extravasor com descarga visível (aviso) e limpeza com registro.
            trecho("T-14", "extravasor", dn_ext_rs, "Cobertura", "RS-01:sup+y",
                   f"d 0 600 -12; desce {saida_ext_rs[2] - 12.0 - laje:g}", None),
            trecho("T-15", "extravasor", dn_limpeza, "Cobertura", "RS-01:inf+x", "d 400 0 -8", "RG-04"),
            trecho("T-16", "extravasor", dn_limpeza, "Cobertura", "RG-04",
                   f"d 300 0 -6; desce {saida_limpeza[2] - 14.0 - laje:g}", None),
        ]
    # Backup potável: hidrômetro → registro → solenoide → air gap, sobre a caixa
    # ou sobre a cisterna. A água potável nunca toca a não potável (NBR 5626:2020).
    nivel_backup = "Prumada" if com_caixa else "Área externa / Térreo"
    runs += [
        trecho("T-17", "alimentacao_potavel", dn_backup, "Área externa / Térreo", "HD-01", "+y 500", "RG-02"),
        trecho("T-18", "alimentacao_potavel", dn_backup, "Área externa / Térreo", "RG-02", "+y 500", "VS-01"),
        trecho("T-19", "alimentacao_potavel", dn_backup, nivel_backup, "VS-01",
               f"+y {y_ag - saida_vs[1]:g}; sobe {topo_ag[2] + 400.0 - saida_vs[2]:g}; -x {x_pot - x_ag:g}; desce 400",
               "AG-01:topo"),
    ]
    if com_bomba and n_bombas >= 2:
        # Reserva em paralelo: tê na sucção, antes do registro da principal, e tê
        # no recalque, depois do registro da principal.
        runs += [
            trecho("T-20", "succao", dn_suc, "Térreo", {"x": x_rg_suc - 300.0, "y": y_b, "z": z_b},
                   "-y 900; +x 300", "RG-06"),
            trecho("T-21", "succao", dn_suc, "Térreo", "RG-06", f"+x {x_b - x_rg_suc:g}", "B-02"),
            trecho("T-22", "recalque", dn_rec, "Térreo", "B-02", f"+x {x_vr - x_b:g}", "VR-03"),
            trecho("T-23", "recalque", dn_rec, "Térreo", "VR-03", f"+x {x_rg - x_vr:g}", "RG-07"),
            trecho("T-24", "recalque", dn_rec, "Térreo", "RG-07", "+x 300; +y 900", None),
        ]

    building_volume: Dict[str, Any] = {
        "origin_mm": {"x": 0.0, "y": 0.0, "z": 0.0},
        "width_mm": bldg_w,
        "depth_mm": bldg_d,
        "height_mm": bldg_h,
        "floors": floors,
    }

    return {
        "bim_components": components,
        "pipe_runs": runs,
        "building_volume": building_volume,
    }
