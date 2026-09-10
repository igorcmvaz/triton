"""Um projeto salvo e reaberto tem de ser o mesmo projeto.

Trinta dos 87 parâmetros não sobreviviam ao ciclo de salvar e reabrir. O arquivo
`.netuno` gravava seis seções e deixava o resto de fora, de modo que os campos
ausentes voltavam ao padrão **em silêncio**:

| Perdia-se | Voltava como |
| :--- | :--- |
| desinfecção por ozônio | cloração |
| altura manométrica de 30 m | zero, «não informada» |
| cisterna de concreto | PEAD |
| irrigação configurada | sem irrigação |
| IPTU verde ativo | desativado |
| filtro de polimento | sem filtro |

Quem montasse um estudo, salvasse e reabrisse recebia **outro estudo**, e nada
avisava. É a mesma família de defeito que a revisão inteira persegue — o valor
existe, está certo, e não chega ao outro lado — só que no eixo do **tempo** em
vez do eixo dos módulos.

Este teste percorre todos os campos de `NetunoConfig`, marca cada um com um
valor distinto do padrão, grava, relê e confere. Acrescentar um campo à
configuração e esquecer de persistí-lo derruba a suíte.
"""

from __future__ import annotations

import os
import tempfile

import pytest

from netuno.core.parser import NetunoConfig, export_netuno_json, load_netuno_project

#: Campos que NÃO devem sobreviver, e por quê.
#:
#: `created_at` é carimbo de gravação e `precip_file` é o nome do arquivo de
#: origem: os dois descrevem o ato de salvar, não o projeto.
NAO_PERSISTIDOS = {"created_at", "precip_file"}

#: Campos declarados como número mas usados como bandeira. O arquivo os grava
#: como booleano, e reabri-los normaliza 8 para 1 — o que está certo.
BANDEIRAS_NUMERICAS = {"upper_tank_used"}


def _marcar(valor):
    """Devolve um valor distinto do padrão, do mesmo tipo."""
    if isinstance(valor, bool):
        return not valor
    if isinstance(valor, int):
        return int(valor) + 7
    if isinstance(valor, float):
        return round(float(valor) * 1.37 + 3.1, 4)
    if isinstance(valor, str) and valor:
        return valor + "_X"
    return None


@pytest.fixture(scope="module")
def ciclo():
    """Marca todos os campos, grava, relê e devolve (marcas, configuração lida)."""
    cfg = NetunoConfig()
    marcas = {}
    for nome in sorted(vars(cfg)):
        if nome in NAO_PERSISTIDOS:
            continue
        novo = _marcar(getattr(cfg, nome))
        if novo is None:
            continue
        marcas[nome] = novo
        setattr(cfg, nome, novo)

    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "projeto.netuno")
        export_netuno_json(cfg, caminho)
        pacote = load_netuno_project(caminho)

    lido = pacote["config"] if isinstance(pacote, dict) else pacote
    return marcas, lido


def test_o_ciclo_cobre_praticamente_toda_a_configuracao():
    """Se o teste cobrir poucos campos, ele não prova nada."""
    cfg = NetunoConfig()
    total = sum(1 for n in vars(cfg) if _marcar(getattr(cfg, n)) is not None)
    assert total >= 80, total


def test_todo_parametro_sobrevive_a_salvar_e_reabrir(ciclo):
    """A verificação central. Trinta campos falhavam aqui.

    Acrescentar um campo a `NetunoConfig` e esquecer de gravá-lo derruba este
    teste, que é exatamente o que se quer: o esquecimento é silencioso, a falha
    não pode ser.
    """
    marcas, lido = ciclo
    perdidos = []
    for nome, esperado in sorted(marcas.items()):
        if nome in BANDEIRAS_NUMERICAS:
            continue
        obtido = getattr(lido, nome, "<AUSENTE>")
        if isinstance(esperado, float) and isinstance(obtido, (int, float)):
            if abs(esperado - float(obtido)) < 1e-6:
                continue
        elif obtido == esperado:
            continue
        perdidos.append(f"{nome}: gravou {esperado!r}, voltou {obtido!r}")
    assert not perdidos, perdidos


# ────────── os grupos que faltavam, nomeados um a um ──────────

@pytest.mark.parametrize(
    "campo",
    [
        "water_quality_target_class",
        "water_quality_disinfection",
        "water_quality_polishing",
        "etap_enabled",
        "chlorine_treatment_enabled",
        "chlorine_dose_mg_l",
        "chlorine_product_purity",
        "chlorine_cost_per_kg",
        "chlorine_co2_kg_per_kg",
    ],
)
def test_a_linha_de_tratamento_sobrevive(ciclo, campo):
    """Escolher ozônio e reabrir com cloração invalida o estudo inteiro."""
    marcas, lido = ciclo
    assert getattr(lido, campo) == marcas[campo]


@pytest.mark.parametrize(
    "campo", ["building_template_id", "lower_tank_material", "upper_tank_material"]
)
def test_a_tipologia_e_os_materiais_sobrevivem(ciclo, campo):
    """Os materiais regem o carbono incorporado; a tipologia rege a demanda."""
    marcas, lido = ciclo
    assert getattr(lido, campo) == marcas[campo]


def test_a_altura_manometrica_do_assistente_sobrevive(ciclo):
    """É o resultado do assistente de motobomba, e governa a energia de recalque.

    Perdê-la ao reabrir devolvia o projeto ao valor de recurso, e a emissão de
    bombeamento voltava a ignorar o desnível informado.
    """
    marcas, lido = ciclo
    assert lido.pump_manometric_head_m == pytest.approx(marcas["pump_manometric_head_m"])


@pytest.mark.parametrize(
    "campo",
    [
        "irrigation_garden_area_m2",
        "irrigation_rate_l_m2_day",
        "irrigation_liters_per_day",
        "irrigation_rain_threshold_mm",
        "irrigation_potable_backup",
    ],
)
def test_a_irrigacao_sobrevive(ciclo, campo):
    marcas, lido = ciclo
    esperado, obtido = marcas[campo], getattr(lido, campo)
    if isinstance(esperado, float):
        assert obtido == pytest.approx(esperado)
    else:
        assert obtido == esperado


@pytest.mark.parametrize(
    "campo",
    [
        "iptu_green_enabled",
        "iptu_annual_value",
        "iptu_discount_pct",
        "tariff_flag",
        "num_economias",
        "potable_indoor_share",
        "non_potable_indoor_share",
    ],
)
def test_os_tributos_e_as_fracoes_sobrevivem(ciclo, campo):
    marcas, lido = ciclo
    esperado, obtido = marcas[campo], getattr(lido, campo)
    if isinstance(esperado, float):
        assert obtido == pytest.approx(esperado)
    else:
        assert obtido == esperado


# ────────── compatibilidade com arquivos anteriores ──────────

def test_um_arquivo_sem_as_secoes_novas_continua_legivel():
    """Projetos gravados antes da 5.0.8 não têm as quatro seções acrescentadas.

    Eles têm de continuar abrindo, com os campos ausentes caindo no padrão —
    que é o comportamento que já tinham.
    """
    import json

    cfg = NetunoConfig()
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "antigo.netuno")
        export_netuno_json(cfg, caminho)

        dados = json.loads(open(caminho, encoding="utf-8").read())
        for secao in ("water_quality_and_etap", "materials_and_typology",
                      "irrigation", "incentives_and_shares"):
            dados["inputs"].pop(secao, None)
        open(caminho, "w", encoding="utf-8").write(json.dumps(dados, ensure_ascii=False))

        pacote = load_netuno_project(caminho)

    lido = pacote["config"] if isinstance(pacote, dict) else pacote
    assert lido.water_quality_disinfection == "cloro"
    assert lido.lower_tank_material == "PEAD"
    assert lido.iptu_green_enabled is False


def test_o_estudo_reaberto_produz_o_mesmo_resultado():
    """A prova final: mesmos parâmetros, mesmos números.

    Preservar os campos só vale se o resultado voltar igual. Um campo lido no
    lugar errado passaria no teste de igualdade e falharia aqui.

    Usa valores plausíveis, e não os marcadores sintéticos: a pureza do cloro
    tem guarda de faixa em (0, 1], e o marcador a estouraria — o que está certo,
    e é verificado em `test_chlorination.py`.
    """
    from netuno.core.etap_integration import capex_incremental_da_etap
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca

    antes = NetunoConfig()
    antes.water_quality_target_class = "classe_4"
    antes.water_quality_disinfection = "ozonio"
    antes.water_quality_polishing = True
    antes.chlorine_dose_mg_l = 2.5
    antes.chlorine_product_purity = 0.325
    antes.chlorine_cost_per_kg = 38.0
    antes.lower_tank_material = "CONCRETO"
    antes.pump_manometric_head_m = 30.0
    antes.area = 250.0
    antes.cost_accessories = 800.0

    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "estudo.netuno")
        export_netuno_json(antes, caminho)
        pacote = load_netuno_project(caminho)
    depois = pacote["config"] if isinstance(pacote, dict) else pacote

    assert capex_incremental_da_etap(antes) == pytest.approx(capex_incremental_da_etap(depois))
    assert capex_incremental_da_etap(depois) > 0.0

    def _acv(cfg):
        return calculate_lca(5000.0, 120.0, EnvironmentalConfig(
            annual_water_saved_m3=120.0,
            lower_material_key=cfg.lower_tank_material,
            water_quality_target_class=cfg.water_quality_target_class,
            water_quality_disinfection=cfg.water_quality_disinfection,
            water_quality_polishing=cfg.water_quality_polishing,
            chlorine_dose_mg_l=cfg.chlorine_dose_mg_l,
            chlorine_product_purity=cfg.chlorine_product_purity,
        ))

    a, b = _acv(antes), _acv(depois)
    assert a.total_embodied_co2_kg == pytest.approx(b.total_embodied_co2_kg)
    assert a.annual_treatment_co2_kg == pytest.approx(b.annual_treatment_co2_kg)
