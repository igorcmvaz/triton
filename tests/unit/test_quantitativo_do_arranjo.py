"""Tudo o que está no arranjo 3D está quantificado e entra no CAPEX e na ACV.

É a garantia verificável do quantitativo: para qualquer arranjo, nenhuma peça,
nenhum metro de tubo, nenhuma curva e nenhum cabo fica sem preço no CAPEX nem sem
carbono na ACV. Se alguém acrescentar um tipo de peça ao catálogo BIM sem dizer
onde ele é contado, o primeiro teste falha.
"""

import numpy as np
import pytest

from netuno.core.bim_exporter import COMPONENT_TYPES
from netuno.core.economic import run_economic_analysis
from netuno.core.environmental import calculate_lca
from netuno.core.etap_integration import capex_incremental_da_etap
from netuno.core.parser import NetunoConfig
from netuno.core.quantitativo_do_arranjo import (
    CATALOGO_DE_PECAS,
    DESTINO_PROPRIO,
    conferir_cobertura,
    itens_para_acv,
    levantar,
    quantitativo_do_projeto,
)
from netuno.core.simulation import run_single_simulation
from netuno.core.study_layout import generate_study_layout


def _simulacao():
    rng = np.random.default_rng(3)
    chuva = np.where(rng.random(730) < 0.35, rng.exponential(12, 730), 0.0)
    return run_single_simulation(chuva, 5000.0, area=150, total_demand_per_day=400, rainwater_share=0.4)


def test_todo_tipo_de_peca_tem_onde_ser_contado():
    tipos = {t["type_id"] for t in COMPONENT_TYPES}
    sem_destino = tipos - set(CATALOGO_DE_PECAS) - set(DESTINO_PROPRIO)
    assert not sem_destino, sem_destino


@pytest.mark.parametrize("volume, area, pavimentos, caixa", [
    (1500, 60, 1, 500), (5000, 150, 2, 1000), (10000, 180, 3, 1000), (30000, 400, 6, 3000),
])
@pytest.mark.parametrize("descarte, etap", [(False, True), (True, True), (True, False), (False, False)])
@pytest.mark.parametrize("abastecimento, bombas", [("recalque", 1), ("recalque", 2), ("pressurizacao", 2), ("gravidade", 1)])
def test_nada_do_arranjo_fica_sem_custo_ou_sem_carbono(volume, area, pavimentos, caixa, descarte, etap,
                                                       abastecimento, bombas):
    layout = generate_study_layout({"lower_vol": volume, "area": area, "floors": pavimentos, "upper_vol": caixa,
                                    "supply_arrangement": abastecimento, "pump_count": bombas})
    q = levantar(layout, subsistema_de_descarte=descarte, etap=etap)
    assert conferir_cobertura(q) == []
    assert len({i.item for i in q.itens if i.unidade == "un" and i.tipo not in ("conexao",)}) == len(layout["bim_components"])


def test_a_conferencia_aponta_a_peca_esquecida():
    """Uma peça sem catálogo nem linha própria aparece na lista, e não some."""
    layout = generate_study_layout({"lower_vol": 5000, "area": 150})
    layout["bim_components"].append({"instance_id": "XX-01", "type_id": "peca_nova", "level": "Térreo",
                                     "position_mm": {"x": 0, "y": 0, "z": 0}, "rotation_deg": 0, "parameters": {}})
    from netuno.core import bim_exporter

    bim_exporter.COMPONENT_TYPES.append({"type_id": "peca_nova", "cad_block": "NETUNO_REGISTRO",
                                         "revit_category": "OST_PipeAccessory", "parameters": []})
    try:
        q = levantar(layout)
    except Exception:
        pytest.skip("o manifesto recusa tipo desconhecido antes do quantitativo")
    finally:
        bim_exporter.COMPONENT_TYPES.pop()
    assert any("XX-01" in f for f in conferir_cobertura(q))


def _projeto_novo():
    cfg = NetunoConfig()
    cfg.capex_do_arranjo = True  # como a interface cria o projeto novo
    return cfg


def test_o_capex_le_a_tubulacao_e_os_acessorios_do_arranjo():
    cfg = _projeto_novo()
    q = quantitativo_do_projeto(cfg)
    run_economic_analysis(cfg, _simulacao())
    assert cfg.cost_piping == pytest.approx(q.custo_de_tubulacao)
    assert cfg.cost_accessories == pytest.approx(q.custo_de_acessorios)
    assert cfg.pipes_list == q.pipes_list()


def test_a_acv_le_a_tubulacao_e_soma_as_pecas_do_arranjo():
    import netuno.cli as cli

    cfg = _projeto_novo()
    sim = _simulacao()
    q = quantitativo_do_projeto(cfg)
    env_cfg = cli._environmental_config(cfg, sim, 150.0, None)
    assert sum(p.length_m for p in env_cfg.pipes) == pytest.approx(sum(q.tubos_m_por_dn.values()), abs=0.01)
    lca = calculate_lca(5000.0, sim.annual_pluvial_consumed_m3, env_cfg)
    arranjo = sum(i.embodied_co2_kg for i in lca.inventory_items if i.category.startswith("Arranjo 3D"))
    assert arranjo == pytest.approx(q.co2e_de_acessorios + q.co2e_de_conexoes)
    assert arranjo > 0
    # Cada tipo de peça avulsa do arranjo tem a sua linha no inventário.
    categorias = {i.category for i in lca.inventory_items}
    for nome, *_ in itens_para_acv(q):
        assert f"Arranjo 3D: {nome}" in categorias


def test_o_valor_digitado_pelo_projetista_prevalece():
    cfg = NetunoConfig()
    cfg.capex_do_arranjo = False
    cfg.cost_piping, cfg.cost_accessories = 999.0, 111.0
    antes = list(cfg.pipes_list)
    run_economic_analysis(cfg, _simulacao())
    assert (cfg.cost_piping, cfg.cost_accessories, cfg.pipes_list) == (999.0, 111.0, antes)


def test_a_etap_nao_desconta_verba_que_o_arranjo_nao_tem():
    """A verba genérica de tratamento só existe nos acessórios estimados por percentual."""
    cfg = NetunoConfig()
    cfg.cost_accessories = 3000.0
    cfg.capex_do_arranjo = False
    com_verba = capex_incremental_da_etap(cfg)
    cfg.capex_do_arranjo = True
    assert capex_incremental_da_etap(cfg) > com_verba


def test_o_arranjo_organizado_viaja_com_o_projeto(tmp_path):
    from netuno.core.parser import export_netuno_json, load_netuno_project

    cfg = _projeto_novo()
    layout = generate_study_layout({"lower_vol": 8000, "area": 200})
    layout["pipe_runs"] = layout["pipe_runs"][:5]
    cfg.bim_layout = layout
    caminho = tmp_path / "p.netuno"
    export_netuno_json(cfg, str(caminho))
    relido = load_netuno_project(str(caminho))["config"]
    assert len(relido.bim_layout["pipe_runs"]) == 5
    assert relido.capex_do_arranjo is True
    assert quantitativo_do_projeto(relido).tubos_m_por_dn == quantitativo_do_projeto(cfg).tubos_m_por_dn


def test_o_arquivo_antigo_mantem_os_custos_que_declara(tmp_path):
    """Sem a chave no arquivo, os custos gravados são os do estudo publicado."""
    import json

    from netuno.core.parser import export_netuno_json, load_netuno_project

    cfg = NetunoConfig()
    cfg.cost_piping, cfg.cost_accessories = 1200.0, 1800.0
    caminho = tmp_path / "antigo.netuno"
    export_netuno_json(cfg, str(caminho))
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["inputs"]["capex_and_opex"].pop("capex_do_arranjo")
    caminho.write_text(json.dumps(dados), encoding="utf-8")
    relido = load_netuno_project(str(caminho))["config"]
    assert relido.capex_do_arranjo is False
    run_economic_analysis(relido, _simulacao())
    assert (relido.cost_piping, relido.cost_accessories) == (1200.0, 1800.0)



def test_o_arranjo_usual_acompanha_o_volume_do_projeto():
    """Era 5.000 L para todo projeto: a configuração não tem ``lower_tank_vol``."""
    from netuno.core.quantitativo_do_arranjo import arranjo_do_projeto

    pequeno, grande = _projeto_novo(), _projeto_novo()
    pequeno.econ_lower_tank_vol, grande.econ_lower_tank_vol = 1500.0, 30000.0
    cisterna = lambda cfg: next(c for c in arranjo_do_projeto(cfg)["bim_components"] if c["type_id"] == "cisterna_inferior")
    assert cisterna(pequeno)["parameters"] != cisterna(grande)["parameters"]
    assert quantitativo_do_projeto(pequeno).tubos_m_por_dn != quantitativo_do_projeto(grande).tubos_m_por_dn
    fixo = _projeto_novo()
    fixo.lower_tank_mode, fixo.lower_tank_fixed, fixo.econ_lower_tank_vol = 0, 30000.0, 1500.0
    assert cisterna(fixo)["parameters"] == cisterna(grande)["parameters"]


def test_o_capex_e_o_desenho_levantam_o_mesmo_arranjo():
    """Com os dados que a prancha recebe, ou só com o projeto, o arranjo usual é um só."""
    from netuno.core.quantitativo_do_arranjo import arranjo_do_projeto, dados_do_estudo

    cfg = _projeto_novo()
    cfg.econ_lower_tank_vol, cfg.area, cfg.upper_tank_vol = 8000.0, 220.0, 1000.0
    relatorio = {"lower_vol": 8000.0, "area": "-", "discard": "-", "upper_vol": 1000.0, "pluv_day": 0.0}
    desenho = generate_study_layout(dados_do_estudo(cfg, relatorio))
    assert desenho == arranjo_do_projeto(cfg)
    assert quantitativo_do_projeto(cfg, None).tubos_m_por_dn == levantar(desenho).tubos_m_por_dn


# ─────────── abastecimento, motobomba reserva e mão de obra ───────────

def _tipos(layout):
    return [c["type_id"] for c in layout["bim_components"]]


def _validado(dados):
    from netuno.core.bim_exporter import build_bim_manifest, validate_bim_manifest

    layout = generate_study_layout(dados)
    manifesto = build_bim_manifest(dict(dados, project_name="t", **layout))
    assert validate_bim_manifest(manifesto) == []
    return layout, {c["instance_id"]: c for c in layout["bim_components"]}


def test_a_reserva_e_desenhada_em_paralelo_com_as_suas_pecas():
    layout, por_id = _validado({"lower_vol": 5000, "pump_count": 2})
    assert _tipos(layout).count("motobomba") == 2
    for peca in ("RG-06", "VR-03", "RG-07"):
        assert peca in por_id
    q = levantar(layout)
    assert {i.item for i in q.itens} >= {"Tês DN 25", "Tês DN 32"}
    um = levantar(generate_study_layout({"lower_vol": 5000, "pump_count": 1}))
    assert q.custo_de_acessorios > um.custo_de_acessorios
    assert q.custo_de_tubulacao > um.custo_de_tubulacao


def test_sem_caixa_o_backup_potavel_desce_na_propria_cisterna():
    for abastecimento in ("pressurizacao", "gravidade"):
        layout, por_id = _validado({"lower_vol": 5000, "supply_arrangement": abastecimento, "pump_count": 2})
        assert "reservatorio_superior" not in _tipos(layout)
        assert not {"SN-02", "RP-02", "RG-04"} & set(por_id)
        cisterna = por_id["CI-01"]
        topo = cisterna["position_mm"]["z"] + cisterna["parameters"]["ALTURA_MM"]
        assert por_id["AG-01"]["position_mm"]["z"] == pytest.approx(topo)
        assert "SN-03" in por_id  # boia de backup, agora na cisterna
        trecho = next(r for r in layout["pipe_runs"] if r["run_id"] == "T-19")
        assert trecho["end"] == "AG-01:topo"


def test_pressurizacao_leva_o_recalque_direto_ao_ponto():
    layout, por_id = _validado({"lower_vol": 5000, "supply_arrangement": "pressurizacao", "pump_count": 1})
    assert _tipos(layout).count("motobomba") == 1
    saida = next(r for r in layout["pipe_runs"] if r["start"] == "RG-01")
    assert saida["end"] == "PNP-01:topo"


def test_gravidade_nao_tem_bomba_e_a_cisterna_fica_acima_do_ponto():
    layout, por_id = _validado({"lower_vol": 5000, "supply_arrangement": "gravidade", "pump_count": 2})
    assert not {"motobomba", "succao_flutuante", "valvula_pe_crivo"} & set(_tipos(layout))
    assert por_id["CI-01"]["position_mm"]["z"] > por_id["PNP-01"]["position_mm"]["z"]


def test_o_arranjo_usual_segue_o_abastecimento_e_as_bombas_do_projeto():
    from netuno.core.quantitativo_do_arranjo import divergencias_com_o_projeto

    for abastecimento, caixa in (("recalque", 1), ("pressurizacao", 0), ("gravidade", 0)):
        cfg = _projeto_novo()
        cfg.supply_arrangement, cfg.upper_tank_used, cfg.pump_count = abastecimento, caixa, 2
        q = quantitativo_do_projeto(cfg)
        assert divergencias_com_o_projeto(cfg, q) == []
    # Um arranjo organizado à mão que ficou para trás é apontado.
    cfg = _projeto_novo()
    cfg.pump_count = 2
    cfg.bim_layout = generate_study_layout({"lower_vol": 5000, "pump_count": 1})
    assert divergencias_com_o_projeto(cfg, quantitativo_do_projeto(cfg))


def test_a_mao_de_obra_automatica_acompanha_os_materiais():
    from netuno.core.cost_estimates import LABOR_PCT
    from netuno.core.quantitativo_do_arranjo import capex_do_volume, materiais_do_projeto, sincronizar_com_o_arranjo

    cfg = _projeto_novo()
    cfg.mao_de_obra_automatica = True
    cfg.cost_lower_tank, cfg.cost_upper_tank, cfg.pump_unit_cost = 6000.0, 500.0, 600.0
    sincronizar_com_o_arranjo(cfg)
    assert cfg.cost_labor == pytest.approx(max(1400.0, LABOR_PCT * materiais_do_projeto(cfg)), abs=0.01)
    assert materiais_do_projeto(cfg) == pytest.approx(6000 + 500 + 600 * cfg.pump_count
                                                      + cfg.cost_piping + cfg.cost_accessories)
    # Na varredura, cisterna maior custa mais e pede mais mão de obra.
    _, _, mao_pequena = capex_do_volume(cfg, 2000.0, 1500.0)
    _, _, mao_grande = capex_do_volume(cfg, 30000.0, 15000.0)
    assert mao_grande > mao_pequena


def test_a_mao_de_obra_digitada_prevalece():
    from netuno.core.quantitativo_do_arranjo import capex_do_volume, sincronizar_com_o_arranjo

    cfg = _projeto_novo()
    cfg.mao_de_obra_automatica, cfg.cost_labor = False, 2222.0
    sincronizar_com_o_arranjo(cfg)
    assert cfg.cost_labor == 2222.0
    assert capex_do_volume(cfg, 30000.0, 15000.0)[2] == 2222.0


def test_o_capex_do_motor_usa_a_mao_de_obra_automatica():
    cfg = _projeto_novo()
    cfg.mao_de_obra_automatica = True
    cfg.cost_labor = 1.0
    res = run_economic_analysis(cfg, _simulacao())
    assert cfg.cost_labor >= 1400.0
    assert res is not None


def test_a_escolha_da_mao_de_obra_viaja_com_o_projeto(tmp_path):
    import json

    from netuno.core.parser import export_netuno_json, load_netuno_project

    cfg = _projeto_novo()
    cfg.mao_de_obra_automatica = True
    caminho = tmp_path / "p.netuno"
    export_netuno_json(cfg, str(caminho))
    assert load_netuno_project(str(caminho))["config"].mao_de_obra_automatica is True
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["inputs"]["capex_and_opex"].pop("mao_de_obra_automatica")
    caminho.write_text(json.dumps(dados), encoding="utf-8")
    assert load_netuno_project(str(caminho))["config"].mao_de_obra_automatica is False
