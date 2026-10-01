"""Quantitativo do arranjo 3D, e onde cada item entra no custo e no carbono.

O arranjo organizado na Planta 3D (ou, sem organização salva, o arranjo usual que o
programa monta a partir do estudo) é a descrição física do sistema. Este módulo o
converte num quantitativo — tubos por DN, curvas, conexões de extremidade, peças e
cabos de comando — e diz, item por item, **onde ele é contado**:

* cisterna, caixa superior e motobomba têm linha própria no CAPEX e na ACV;
* filtro e descarte são do subsistema de descarte e da linha de tratamento
  (`etap_integration.py`, `water_quality.py`), quando esse subsistema está ativo;
* todo o resto — registros, válvulas, solenoide, hidrômetro, chaves de nível,
  quadro, freio d'água, sucção flutuante, respiros, ladrão, air gap, ponto de
  consumo, curvas, conexões e cabos — é orçado e inventariado aqui, peça a peça.

`conferir_cobertura` é a garantia verificável: devolve a lista do que ficou sem
destino, e o teste de cobertura exige que ela seja vazia para qualquer arranjo.

Os **preços** e as **massas** das peças são cenário de referência interno, na mesma
condição da verba de acessórios que substituem: servem para que nada fique de fora
e para que a ordem de grandeza esteja certa, e devem ser trocados pelo orçamento da
obra. Estão todos em `CATALOGO_DE_PECAS`, cada um com a origem declarada, e podem
ser sobrescritos em `netuno/data/costs_database.json`, chave ``pecas_do_arranjo``.
Os **fatores de emissão** vêm de fontes nomeadas, por material.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

# ── fatores de emissão por material (kg CO2e por kg de peça) ───────────────

#: Material → (fator, fonte). O PVC e o eletromecânico repetem os valores já
#: adotados em `environmental.py`, para que peça e tubo usem a mesma régua.
FATORES_POR_MATERIAL: Dict[str, Tuple[float, str]] = {
    "pvc": (2.36, "EPD Australasia S-P-05503 (RXP PVC Pipes, 2022, EN 15804+A2), A1-A3, 1 kg de tubo "
                  "instalado — o mesmo fator dos tubos em environmental.py; aplicado a conexões e peças de PVC"),
    "latao": (2.64, "Inventário de carbono incorporado de materiais de construção do CIDB (Malásia), "
                    "conexões de latão; valor obtido em fonte secundária, documento primário não consultado"),
    "ferro_fundido": (2.11, "ICM Embodied Carbon Life Cycle Inventory, ferro fundido; valor obtido em fonte "
                            "secundária, documento primário não consultado"),
    "eletromecanico": (4.77, "EPD Grundfos ALPHA1 GO 25-40 180 (EPD-GRU-20250340-CBA1-EN, 2025), A1-A3: "
                             "10,4 kg CO2e / 2,179 kg — a intensidade adotada para a motobomba em "
                             "environmental.py, aplicada a produto eletromecânico pequeno"),
    "cabo": (4.77, "cabo PP de cobre e PVC; adota-se a intensidade eletromecânica por falta de EPD de cabo"),
}


@dataclass(frozen=True)
class Peca:
    """Uma entrada do catálogo: preço e massa na bitola de referência."""

    nome: str
    material: str
    preco_brl: float
    massa_kg: float
    escala_pelo_dn: bool       # peça de linha, que cresce com a bitola
    origem: str


_ORIGEM_PADRAO = ("cenário de referência interno (preço de varejo e massa típica de catálogo, 2026), "
                  "na bitola de 25 mm quando a peça escala; substituir pelo orçamento da obra")

#: Peças avulsas do arranjo. Tanques, motobomba, filtro e descarte ficam de fora
#: porque têm linha própria (ver `DESTINO_PROPRIO`).
CATALOGO_DE_PECAS: Dict[str, Peca] = {
    "registro_gaveta": Peca("Registro de gaveta (bronze)", "latao", 75.0, 0.45, True, _ORIGEM_PADRAO),
    "registro_esfera": Peca("Registro de esfera (PVC)", "pvc", 25.0, 0.20, True, _ORIGEM_PADRAO),
    "valvula_retencao": Peca("Válvula de retenção (bronze)", "latao", 85.0, 0.50, True, _ORIGEM_PADRAO),
    "valvula_solenoide": Peca("Válvula solenoide", "eletromecanico", 140.0, 0.60, True, _ORIGEM_PADRAO),
    "hidrometro": Peca("Hidrômetro com cavalete", "latao", 160.0, 0.90, True, _ORIGEM_PADRAO),
    "valvula_pe_crivo": Peca("Válvula de pé com crivo", "pvc", 45.0, 0.30, True, _ORIGEM_PADRAO),
    "filtro_pluvial": Peca("Filtro pluvial", "pvc", 650.0, 3.0, False,
                           "preço do filtro autolimpante DN 100 de water_quality.py; massa típica"),
    "first_flush": Peca("Reservatório de descarte com válvula de purga", "pvc", 180.0, 6.0, False, _ORIGEM_PADRAO),
    "succao_flutuante": Peca("Sucção flutuante (boia e mangote)", "pvc", 280.0, 1.20, False, _ORIGEM_PADRAO),
    # Peças de PVC da captação e do extravasor: preço e massa já na bitola usual, DN 100.
    "freio_dagua": Peca("Freio d'água (entrada calma), DN 100", "pvc", 70.0, 0.60, False, _ORIGEM_PADRAO),
    "ladrao_sifonado": Peca("Ladrão sifonado com tela, DN 100", "pvc", 110.0, 1.50, False, _ORIGEM_PADRAO),
    "respiro": Peca("Respiro com tela", "pvc", 40.0, 0.50, False, _ORIGEM_PADRAO),
    "sensor_nivel": Peca("Chave de nível (boia elétrica)", "eletromecanico", 65.0, 0.40, False, _ORIGEM_PADRAO),
    "quadro_comando": Peca("Quadro de comando", "eletromecanico", 480.0, 3.50, False, _ORIGEM_PADRAO),
    "air_gap": Peca("Separação atmosférica (air gap)", "pvc", 150.0, 0.40, False,
                    "verba de air gap já usada pelo estimador de custos (air_gap_supplement_cost); massa típica"),
    "ponto_nao_potavel": Peca("Ponto de consumo não potável com placa", "latao", 55.0, 0.40, False, _ORIGEM_PADRAO),
}

#: Tipos que têm linha própria no CAPEX e na ACV, e qual.
DESTINO_PROPRIO: Dict[str, str] = {
    "cisterna_inferior": "reservatório inferior (CAPEX e ACV)",
    "reservatorio_superior": "reservatório superior (CAPEX e ACV)",
    "motobomba": "motobombas (CAPEX e ACV)",
}

#: Filtro e descarte: onde entram depende das escolhas da etapa de qualidade.
#: A ETAP orça o filtro de entrada sempre que está ligada, e o descarte quando o
#: subsistema de descarte também está; a ACV conta os dois só com o descarte ligado.
_LINHA_DA_ETAP = "linha de tratamento (CAPEX, pela ETAP)"
_LINHA_DO_DESCARTE = "subsistema de descarte (ACV)"

#: Curva de 90° e conexão de extremidade (luva ou adaptador), na bitola de 25 mm.
CURVA = Peca("Curva 90° PVC", "pvc", 3.0, 0.03, True, _ORIGEM_PADRAO)
CONEXAO = Peca("Conexão de extremidade PVC (luva/adaptador)", "pvc", 2.5, 0.025, True, _ORIGEM_PADRAO)
TE = Peca("Tê 90° PVC", "pvc", 4.5, 0.045, True, _ORIGEM_PADRAO)
CABO = Peca("Cabo PP 3 × 1,5 mm² (por metro)", "cabo", 6.0, 0.12, False, _ORIGEM_PADRAO)

_DN_REFERENCIA = 25.0


def _catalogo() -> Dict[str, Peca]:
    """O catálogo, com os preços sobrescritos em costs_database.json, se houver."""
    catalogo = dict(CATALOGO_DE_PECAS)
    try:
        from netuno.core.cost_estimates import COSTS_FILE_PATH

        dados = json.loads(COSTS_FILE_PATH.read_text(encoding="utf-8")).get("pecas_do_arranjo") or {}
    except (OSError, ValueError, ImportError):
        dados = {}
    for tipo, valores in dados.items():
        if tipo in catalogo and isinstance(valores, dict):
            base = catalogo[tipo]
            catalogo[tipo] = Peca(base.nome, valores.get("material", base.material),
                                  float(valores.get("preco_brl", base.preco_brl)),
                                  float(valores.get("massa_kg", base.massa_kg)),
                                  base.escala_pelo_dn, valores.get("origem", "costs_database.json"))
    return catalogo


def _escala(peca: Peca, dn: Optional[float], expoente_preco: float = 0.9, expoente_massa: float = 1.3) -> Tuple[float, float]:
    """Fatores de preço e massa pela bitola: peças de linha crescem com o DN."""
    if not peca.escala_pelo_dn or not dn:
        return 1.0, 1.0
    razao = max(0.5, float(dn) / _DN_REFERENCIA)
    return razao ** expoente_preco, razao ** expoente_massa


# ── o quantitativo ──────────────────────────────────────────────────────────

@dataclass
class ItemDoQuantitativo:
    """Uma linha do quantitativo, com o destino no CAPEX e na ACV."""

    item: str               # «CI-01», «Tubo DN 32», «Curvas DN 100», «Cabo SN-01 → QC-01»
    tipo: str
    quantidade: float
    unidade: str
    dn_mm: Optional[float]
    custo_brl: float        # 0 quando contado em linha própria
    massa_kg: float
    co2e_kg: float          # incorporado, A1-A3
    destino: str            # onde entra no CAPEX e na ACV
    origem: str             # de onde vêm preço, massa e fator
    no_capex: str = ""      # a linha do CAPEX que o conta
    na_acv: str = ""        # o item da ACV que o conta

    def __post_init__(self) -> None:
        self.no_capex = self.no_capex or self.destino
        self.na_acv = self.na_acv or self.destino


@dataclass
class Quantitativo:
    itens: List[ItemDoQuantitativo] = field(default_factory=list)
    tubos_m_por_dn: Dict[int, float] = field(default_factory=dict)
    componentes: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def custo_de_tubulacao(self) -> float:
        return round(sum(i.custo_brl for i in self.itens if i.no_capex == DESTINO_TUBULACAO), 2)

    @property
    def custo_de_acessorios(self) -> float:
        return round(sum(i.custo_brl for i in self.itens if i.no_capex == DESTINO_ACESSORIOS), 2)

    @property
    def co2e_de_conexoes(self) -> float:
        return sum(i.co2e_kg for i in self.itens if i.tipo == "conexao")

    @property
    def co2e_de_acessorios(self) -> float:
        return sum(i.co2e_kg for i in self.itens if i.na_acv == DESTINO_ACESSORIOS)

    def pipes_list(self) -> List[Tuple[int, float]]:
        return [(dn, round(m, 3)) for dn, m in sorted(self.tubos_m_por_dn.items())]


DESTINO_TUBULACAO = "tubulação e conexões (CAPEX «Tubulação»; ACV «Tubulação PVC» por DN)"
DESTINO_ACESSORIOS = "acessórios do arranjo (CAPEX «Acessórios»; ACV «Acessórios do arranjo»)"


def _dn_comercial(dn: float) -> int:
    """A bitola da tabela de preços e de massa mais próxima, sem ficar abaixo."""
    from netuno.core.cost_estimates import PIPE_COST_PER_METER

    tabela = sorted(int(d) for d in PIPE_COST_PER_METER)
    return next((d for d in tabela if d >= float(dn) - 0.5), tabela[-1])


def _curvas(run: Dict[str, Any]) -> int:
    """Mudanças de direção entre segmentos consecutivos do trecho."""
    direcoes = []
    for seg in run.get("segments") or []:
        a, b = seg["start_mm"], seg["end_mm"]
        v = (b["x"] - a["x"], b["y"] - a["y"], b["z"] - a["z"])
        n = math.sqrt(sum(c * c for c in v))
        if n > 1.0:
            direcoes.append(tuple(c / n for c in v))
    return sum(1 for u, w in zip(direcoes, direcoes[1:]) if sum(p * q for p, q in zip(u, w)) < 0.999)


def _tes(runs: Sequence[Dict[str, Any]]) -> Dict[int, int]:
    """Tês: ponta solta de um trecho que cai no meio de outro (a reserva da bomba).

    A bitola é a maior das duas. Ponta solta que não encontra tubo é descarga livre.
    """
    def distancia(p, a, b) -> float:
        ab = [bj - aj for aj, bj in zip(a, b)]
        n2 = sum(c * c for c in ab)
        t = 0.0 if n2 <= 0 else max(0.0, min(1.0, sum((pj - aj) * c for pj, aj, c in zip(p, a, ab)) / n2))
        return math.dist(p, [aj + t * c for aj, c in zip(a, ab)])

    tes: Dict[int, int] = {}
    for run in runs:
        vertices = [(v["x"], v["y"], v["z"]) for v in run.get("vertices_mm") or []]
        if len(vertices) < 2:
            continue
        pontas = ([vertices[0]] if not run.get("start_ref") else []) + ([vertices[-1]] if not run.get("end_ref") else [])
        for ponta in pontas:
            for outro in runs:
                if outro is run:
                    continue
                vs = [(v["x"], v["y"], v["z"]) for v in outro.get("vertices_mm") or []]
                if any(distancia(ponta, a, b) <= 1.0 for a, b in zip(vs, vs[1:])):
                    dn = _dn_comercial(max(float(run["dn_mm"]), float(outro["dn_mm"])))
                    tes[dn] = tes.get(dn, 0) + 1
                    break
    return tes


def arranjo_do_projeto(config: Any = None, project_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """O arranjo organizado, ou o usual montado a partir do estudo."""
    layout = dict(getattr(config, "bim_layout", None) or {})
    dados = dict(project_data or {})
    if dados.get("bim_components") or dados.get("pipe_runs"):
        layout = {k: dados.get(k) for k in ("bim_components", "pipe_runs", "building_volume")}
    if layout.get("bim_components") or layout.get("pipe_runs"):
        return layout
    from netuno.core.study_layout import generate_study_layout

    return generate_study_layout(dados_do_estudo(config, dados))


def volume_do_estudo(config: Any) -> float:
    """O volume da cisterna que o projeto analisa: o fixo, ou o escolhido na varredura."""
    if config is None:
        return 0.0
    if int(getattr(config, "lower_tank_mode", 1) or 0) == 0 and float(getattr(config, "lower_tank_fixed", 0.0) or 0.0) > 0:
        return float(config.lower_tank_fixed)
    return float(getattr(config, "econ_lower_tank_vol", 0.0) or 0.0)


def dados_do_estudo(config: Any = None, project_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """O que o gerador do arranjo usual lê, com a mesma regra para o CAPEX e o desenho.

    Os dados do desenho (``project_data``), quando há, prevalecem: são o volume e a
    área que a prancha documenta. Sem eles vale o projeto. O número de pavimentos,
    que o projeto não guarda, fica com o padrão do gerador nos dois casos.
    """
    estudo: Dict[str, Any] = {}
    if config is not None:
        estudo = {
            "lower_vol": volume_do_estudo(config),
            "upper_vol": float(getattr(config, "upper_tank_vol", 0.0) or 0.0),
            "area": float(getattr(config, "area", 0.0) or 0.0),
            "discard": float(getattr(config, "discard", 0.0) or 0.0),
            "pump_count": float(getattr(config, "pump_count", 1) or 1),
        }
        estudo = {k: v for k, v in estudo.items() if v > 0}
        from netuno.core.supply_arrangement import arranjo_de

        estudo["supply_arrangement"] = arranjo_de(config)
    for chave, valor in dict(project_data or {}).items():
        vazio = valor in (None, "", "-") or (isinstance(valor, (int, float)) and not isinstance(valor, bool) and valor <= 0)
        if not vazio or chave not in estudo:
            estudo[chave] = valor
    return estudo


def levantar(layout: Dict[str, Any], project_data: Optional[Dict[str, Any]] = None,
             subsistema_de_descarte: bool = True, etap: bool = True) -> Quantitativo:
    """Quantitativo completo do arranjo, com preço, massa, carbono e destino."""
    from netuno.core.bim_exporter import build_bim_manifest
    from netuno.core.cost_estimates import PIPE_COST_PER_METER
    from netuno.core.environmental import PIPE_EMISSION_FACTORS_PER_METER, PIPE_LINEAR_MASS_KG_PER_M
    from netuno.core.volumetry import trajetos_de_comando

    dados = dict(project_data or {})
    dados.update({k: layout.get(k) for k in ("bim_components", "pipe_runs", "building_volume") if layout.get(k) is not None})
    dados.setdefault("project_name", "Quantitativo")
    manifesto = build_bim_manifest(dados)
    catalogo = _catalogo()
    q = Quantitativo(componentes=list(manifesto["instances"]))

    # Tubos, curvas e conexões, por DN comercial.
    curvas: Dict[int, int] = {}
    conexoes: Dict[int, int] = {}
    for run in manifesto["pipe_runs"]:
        dn = _dn_comercial(run["dn_mm"])
        q.tubos_m_por_dn[dn] = q.tubos_m_por_dn.get(dn, 0.0) + run["length_mm"] / 1000.0
        curvas[dn] = curvas.get(dn, 0) + _curvas(run)
        conexoes[dn] = conexoes.get(dn, 0) + sum(1 for ref in (run.get("start_ref"), run.get("end_ref")) if ref)
    for dn, metros in sorted(q.tubos_m_por_dn.items()):
        massa = metros * PIPE_LINEAR_MASS_KG_PER_M.get(dn, 0.0)
        q.itens.append(ItemDoQuantitativo(
            f"Tubo PVC DN {dn}", "tubo", round(metros, 3), "m", dn,
            round(metros * PIPE_COST_PER_METER.get(dn, 35.0), 2), round(massa, 3),
            metros * PIPE_EMISSION_FACTORS_PER_METER.get(dn, 3.92), DESTINO_TUBULACAO,
            "preço por metro de cost_estimates.py (SINAPI); massa e fator de environmental.py"))
    fator_pvc = FATORES_POR_MATERIAL["pvc"][0]
    for nome, peca, contagem in (("Curvas", CURVA, curvas), ("Conexões de extremidade", CONEXAO, conexoes),
                                 ("Tês", TE, _tes(manifesto["pipe_runs"]))):
        for dn, n in sorted(contagem.items()):
            if n <= 0:
                continue
            fp, fm = _escala(peca, dn, 1.6, 1.8)
            q.itens.append(ItemDoQuantitativo(
                f"{nome} DN {dn}", "conexao", n, "un", dn, round(n * peca.preco_brl * fp, 2),
                round(n * peca.massa_kg * fm, 3), n * peca.massa_kg * fm * fator_pvc, DESTINO_TUBULACAO, peca.origem,
                DESTINO_TUBULACAO, "ACV «Arranjo 3D: Conexões e curvas (PVC)»"))

    # Peças.
    for inst in manifesto["instances"]:
        tipo = inst["type_id"]
        if tipo in DESTINO_PROPRIO:
            q.itens.append(ItemDoQuantitativo(inst["instance_id"], tipo, 1, "un", None, 0.0, 0.0, 0.0,
                                              DESTINO_PROPRIO[tipo], "contado na linha própria"))
            continue
        peca = catalogo.get(tipo)
        if peca is None:
            continue  # sem destino: `conferir_cobertura` aponta
        no_capex, na_acv = DESTINO_ACESSORIOS, DESTINO_ACESSORIOS
        if tipo == "filtro_pluvial" and etap:
            no_capex = _LINHA_DA_ETAP
        if tipo == "first_flush" and etap and subsistema_de_descarte:
            no_capex = _LINHA_DA_ETAP
        if tipo in ("filtro_pluvial", "first_flush") and subsistema_de_descarte:
            na_acv = _LINHA_DO_DESCARTE
        dn = (inst.get("parameters") or {}).get("DN_MM")
        dn = float(dn) if dn not in (None, "") else None
        fp, fm = _escala(peca, dn)
        fator, fonte = FATORES_POR_MATERIAL[peca.material]
        massa = peca.massa_kg * fm
        custo = round(peca.preco_brl * fp, 2) if no_capex == DESTINO_ACESSORIOS else 0.0
        co2e = massa * fator if na_acv == DESTINO_ACESSORIOS else 0.0
        destino = no_capex if no_capex == na_acv else f"CAPEX: {no_capex}; ACV: {na_acv}"
        q.itens.append(ItemDoQuantitativo(
            inst["instance_id"], tipo, 1, "un", dn, custo, round(massa, 3), co2e, destino,
            f"{peca.nome}: {peca.origem}; fator: {fonte}", no_capex, na_acv))

    # Cabos de comando, pelo traçado que a volumetria desenha.
    for origem, destino, _papel, caminho in trajetos_de_comando(manifesto["instances"], dados):
        metros = sum(math.dist(a, b) for a, b in zip(caminho, caminho[1:])) / 1000.0
        fator, fonte = FATORES_POR_MATERIAL[CABO.material]
        q.itens.append(ItemDoQuantitativo(
            f"Cabo {origem} → {destino}", "cabo", round(metros, 2), "m", None,
            round(metros * CABO.preco_brl, 2), round(metros * CABO.massa_kg, 3),
            metros * CABO.massa_kg * fator, DESTINO_ACESSORIOS, f"{CABO.nome}: {CABO.origem}; fator: {fonte}"))
    return q


def quantitativo_do_projeto(config: Any = None, project_data: Optional[Dict[str, Any]] = None) -> Quantitativo:
    """Atalho: o arranjo do projeto, levantado com a escolha de descarte do estudo."""
    descarte = bool(getattr(config, "first_flush_system_enabled", False)) if config is not None else False
    etap = bool(getattr(config, "etap_enabled", True)) if config is not None else True
    return levantar(arranjo_do_projeto(config, project_data), project_data,
                    subsistema_de_descarte=descarte, etap=etap)


def aplicar_ao_projeto(config: Any, q: Optional[Quantitativo] = None) -> Quantitativo:
    """Leva o quantitativo ao CAPEX e à ACV do projeto.

    A tubulação da ACV (``pipes_list``) passa a ser a do arranjo, e o custo de
    tubulação e o de acessórios passam a ser a soma dos itens. É o que o estimador
    usa quando há arranjo; o projetista pode sobrescrever os valores depois.
    """
    q = q or quantitativo_do_projeto(config)
    config.pipes_list = q.pipes_list()
    config.cost_piping = q.custo_de_tubulacao
    config.cost_accessories = q.custo_de_acessorios
    return q


def conferir_cobertura(q: Quantitativo) -> List[str]:
    """O que do arranjo não tem destino no CAPEX e na ACV. Vazio é a garantia."""
    contados = {i.item for i in q.itens}
    faltam = [f"{c['instance_id']} ({c['type_id']})" for c in q.componentes if c["instance_id"] not in contados]
    total_tubos = sum(q.tubos_m_por_dn.values())
    tubos_itens = sum(i.quantidade for i in q.itens if i.tipo == "tubo")
    if abs(total_tubos - tubos_itens) > 0.01:
        faltam.append(f"tubos: {total_tubos:.3f} m no arranjo e {tubos_itens:.3f} m no quantitativo")
    proprios = set(DESTINO_PROPRIO.values()) | {_LINHA_DA_ETAP, _LINHA_DO_DESCARTE}
    for i in q.itens:
        if i.no_capex not in proprios and i.custo_brl <= 0:
            faltam.append(f"{i.item} sem custo no CAPEX")
        if i.na_acv not in proprios and i.co2e_kg <= 0:
            faltam.append(f"{i.item} sem carbono na ACV")
    return faltam


def divergencias_com_o_projeto(config: Any, q: Quantitativo) -> List[str]:
    """O que o arranjo desenha e o projeto não declara, ou o contrário.

    O arranjo usual sai do projeto e não diverge; um arranjo organizado à mão pode
    ficar para trás quando o projeto muda de abastecimento ou de número de bombas.
    """
    if config is None:
        return []
    from netuno.core.supply_arrangement import GRAVIDADE, NAO_INFORMADO, RECALQUE, arranjo_de

    arranjo = arranjo_de(config)
    if arranjo == NAO_INFORMADO:
        return ["o projeto não declara o arranjo de abastecimento (recalque, pressurização ou gravidade); "
                "o arranjo usual desenhado é o de recalque"]
    tipos = [c["type_id"] for c in q.componentes]
    avisos = []
    bombas = tipos.count("motobomba")
    esperadas = 0 if arranjo == GRAVIDADE else int(getattr(config, "pump_count", 1) or 0)
    if bombas != esperadas:
        avisos.append(f"o arranjo tem {bombas} motobomba(s) e o projeto declara {esperadas}")
    tem_caixa = "reservatorio_superior" in tipos
    if tem_caixa != (arranjo == RECALQUE):
        avisos.append("o arranjo tem caixa superior e o abastecimento do projeto não a usa" if tem_caixa
                      else "o projeto declara caixa superior e o arranjo não a tem")
    return avisos


# ── sincronização com o projeto ─────────────────────────────────────────────

_CACHE: Dict[str, Quantitativo] = {}


def _chave(config: Any) -> str:
    campos = ("first_flush_system_enabled", "etap_enabled")
    return json.dumps([getattr(config, "bim_layout", None) or {}, dados_do_estudo(config)]
                      + [getattr(config, c, None) for c in campos], sort_keys=True, default=str)


def _quantitativo_em_cache(config: Any) -> Optional[Quantitativo]:
    chave = _chave(config)
    q = _CACHE.get(chave)
    if q is None:
        try:
            q = quantitativo_do_projeto(config)
        except Exception:
            return None  # arranjo inválido: fica o que o projeto já tinha
        if len(_CACHE) > 64:
            _CACHE.clear()
        _CACHE[chave] = q
    return q


def sincronizar_com_o_arranjo(config: Any) -> Optional[Quantitativo]:
    """Leva o arranjo ao CAPEX e à ACV, se o projeto o usa como fonte.

    É chamada no início do motor econômico, da aba econômica e da montagem da ACV,
    para que nenhum deles leia uma tubulação ou uma verba de acessórios que não
    corresponda ao arranjo. Com ``capex_do_arranjo`` desligado — o projetista
    digitou os próprios valores —, nada muda. A mão de obra automática é refeita
    em seguida, sobre os materiais que ficaram.
    """
    if config is None:
        return None
    q = None
    if bool(getattr(config, "capex_do_arranjo", False)):
        q = _quantitativo_em_cache(config)
        if q is not None:
            aplicar_ao_projeto(config, q)
    if bool(getattr(config, "mao_de_obra_automatica", False)):
        config.cost_labor = mao_de_obra_do_projeto(config)
    return q


# ── mão de obra ─────────────────────────────────────────────────────────────

def materiais_do_projeto(config: Any, custo_cisterna: Optional[float] = None,
                         custo_tubulacao: Optional[float] = None, custo_acessorios: Optional[float] = None) -> float:
    """Soma dos materiais que a mão de obra instala: reservatórios, motobombas e arranjo."""
    from netuno.core.supply_arrangement import arranjo_de, usa_bomba

    bombas = 0.0 if not usa_bomba(arranjo_de(config)) else (
        float(getattr(config, "pump_unit_cost", 0.0) or 0.0) * int(getattr(config, "pump_count", 1) or 0))
    return (float(config.cost_lower_tank if custo_cisterna is None else custo_cisterna)
            + float(getattr(config, "cost_upper_tank", 0.0) or 0.0) + bombas
            + float(config.cost_piping if custo_tubulacao is None else custo_tubulacao)
            + float(config.cost_accessories if custo_acessorios is None else custo_acessorios))


def mao_de_obra_do_projeto(config: Any, custo_cisterna: Optional[float] = None,
                           custo_tubulacao: Optional[float] = None, custo_acessorios: Optional[float] = None) -> float:
    """Mão de obra como fração dos materiais: cresce com a cisterna e com o arranjo.

    É a regra do estimador (``labor_percentage`` de costs_database.json, 30 %, com
    piso de R$ 1.400), aplicada aos materiais do projeto, e não às verbas genéricas.
    """
    from netuno.core.cost_estimates import mao_de_obra_estimada

    return round(mao_de_obra_estimada(materiais_do_projeto(config, custo_cisterna, custo_tubulacao,
                                                           custo_acessorios)), 2)


def capex_do_volume(config: Any, volume_l: float, custo_cisterna: float) -> Tuple[float, float, float]:
    """``(tubulação, acessórios, mão de obra)`` de um volume da varredura.

    Com o arranjo usual, cada volume tem a sua cisterna e os seus percursos; com o
    arranjo organizado pelo projetista, ou com valores digitados, eles não mudam.
    A mão de obra automática acompanha o custo da cisterna de cada volume.
    """
    tubulacao, acessorios = float(config.cost_piping), float(config.cost_accessories)
    organizado = bool((getattr(config, "bim_layout", None) or {}).get("bim_components"))
    if bool(getattr(config, "capex_do_arranjo", False)) and not organizado and volume_l > 0:
        import copy

        do_volume = copy.copy(config)
        do_volume.lower_tank_mode, do_volume.econ_lower_tank_vol = 1, float(volume_l)
        q = _quantitativo_em_cache(do_volume)
        if q is not None:
            tubulacao, acessorios = q.custo_de_tubulacao, q.custo_de_acessorios
    if bool(getattr(config, "mao_de_obra_automatica", False)):
        mao = mao_de_obra_do_projeto(config, custo_cisterna, tubulacao, acessorios)
    else:
        mao = float(config.cost_labor)
    return tubulacao, acessorios, mao


def itens_para_acv(q: Optional[Quantitativo]) -> List[Tuple[str, str, float, float, str]]:
    """``(categoria, quantidade, massa_kg, co2e_kg, fonte)`` por tipo, para a ACV.

    Os tubos não entram: a ACV já os conta pela ``pipes_list``, que o quantitativo
    define. Entram as conexões e as peças que não têm linha própria.
    """
    if q is None:
        return []
    grupos: Dict[str, List[ItemDoQuantitativo]] = {}
    for item in q.itens:
        if item.tipo == "tubo" or item.co2e_kg <= 0:
            continue
        chave = "Conexões e curvas (PVC)" if item.tipo == "conexao" else (
            "Cabos de comando" if item.tipo == "cabo" else _NOMES.get(item.tipo, item.tipo))
        grupos.setdefault(chave, []).append(item)
    saida = []
    for nome, itens in grupos.items():
        unidade = "m" if itens[0].tipo == "cabo" else "un"
        quantidade = sum(i.quantidade for i in itens)
        ids = ", ".join(i.item for i in itens if i.tipo not in ("conexao", "cabo"))
        texto = f"{quantidade:g} {unidade}" + (f" ({ids})" if ids else "")
        saida.append((nome, texto, sum(i.massa_kg for i in itens), sum(i.co2e_kg for i in itens), itens[0].origem))
    return saida


_NOMES = {tipo: peca.nome for tipo, peca in CATALOGO_DE_PECAS.items()}


def itens_de_acv_do_projeto(config: Any) -> List[Tuple[str, str, float, float, str]]:
    """Sincroniza o projeto com o arranjo e devolve os itens da ACV.

    Chamada antes de ler a tubulação do projeto, porque é ela que a define.
    """
    return itens_para_acv(sincronizar_com_o_arranjo(config))
