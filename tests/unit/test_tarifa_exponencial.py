"""A fórmula exponencial da CORSAN: Água = PB × Cⁿ + serviço básico.

A CORSAN não cobra por faixas. O expoente ``n`` sai da tabela exponencial pelo
consumo do mês inteiro e se aplica a todo o volume; a fórmula vale até 1.000 m³ e o
excedente é cobrado pelo preço do m³. Até a 5.0.0 esses municípios estavam
gravados como uma reta, ``PB × C + SB``, que só coincide com a fórmula se n = 1.
"""

import importlib.util
import json
from pathlib import Path

import pytest

from netuno.core.economic import calculate_water_bill
from netuno.core.tariff_regimes import EXPONENCIAL, ler_estrutura, resumo_do_regime, validar_estrutura
from netuno.core.tariffs_database import get_city_data, get_city_tariffs_by_category
from netuno.core.tariffs_structure import (
    EXPOENTE_DE_CONSUMO,
    PRECO_BASE_EXPONENCIAL,
    diagnosticar,
    expoente_do_consumo,
    parcela_exponencial,
)

RAIZ = Path(__file__).resolve().parents[2]

#: Uma tabela com três linhas, para que o expoente mude com o consumo.
TABELA = [
    (0.0, 0.0, 43.39, -1),
    (0.0, 1000.0, 9.15, PRECO_BASE_EXPONENCIAL),
    (0.0, 10.0, 1.00, EXPOENTE_DE_CONSUMO),
    (10.0, 20.0, 1.05, EXPOENTE_DE_CONSUMO),
    (20.0, 1000.0, 1.10, EXPOENTE_DE_CONSUMO),
    (1000.0, 999999.0, 9.15, 1),
]


def _agua(m3, tabela=TABELA):
    return calculate_water_bill(m3 * 1000.0, tabela, sewage_mode=1, sewage_rate=0.0)


def test_o_expoente_e_lido_pelo_consumo_do_mes_inteiro():
    assert expoente_do_consumo(TABELA, 0.0) == 1.00
    assert expoente_do_consumo(TABELA, 10.0) == 1.00  # (0, 10] inclui o 10
    assert expoente_do_consumo(TABELA, 10.5) == 1.05
    assert expoente_do_consumo(TABELA, 25.0) == 1.10
    assert expoente_do_consumo([], 25.0) == 1.0  # sem tabela, a forma linear


@pytest.mark.parametrize("consumo, n", [(5.0, 1.00), (15.0, 1.05), (30.0, 1.10)])
def test_a_conta_e_pb_vezes_c_elevado_a_n_mais_o_servico_basico(consumo, n):
    assert _agua(consumo) == pytest.approx(9.15 * consumo ** n + 43.39)


def test_o_expoente_vale_para_o_volume_todo_e_nao_so_para_o_ultimo_m3():
    """Passar de 10 para 11 m³ muda a conta inteira, não só o 11º metro cúbico."""
    salto = _agua(11.0) - _agua(10.0)
    assert salto == pytest.approx(9.15 * 11 ** 1.05 - 9.15 * 10.0)
    assert salto > 9.15 * 1.5  # muito mais que o preço-base de um m³


def test_acima_do_teto_o_excedente_e_cobrado_pelo_preco_do_m3():
    no_teto = 9.15 * 1000.0 ** 1.10 + 43.39
    assert _agua(1000.0) == pytest.approx(no_teto)
    assert _agua(1200.0) == pytest.approx(no_teto + 200.0 * 9.15)


def test_o_esgoto_e_percentual_da_agua_inteira():
    total = calculate_water_bill(15_000.0, TABELA, sewage_mode=1, sewage_rate=70.0)
    assert total == pytest.approx(_agua(15.0) * 1.70)


def test_a_economia_e_a_diferenca_entre_as_duas_potencias():
    """O m³ poupado vale mais que o preço-base quando n > 1."""
    economia = _agua(30.0) - _agua(20.0)
    assert economia == pytest.approx(9.15 * (30 ** 1.10 - 20 ** 1.05))
    assert economia / 10.0 > 9.15


def test_micromedicao_aplica_a_formula_por_economia():
    """Vinte apartamentos de 15 m³ não são um consumidor de 300 m³."""
    predio = calculate_water_bill(300_000.0, TABELA, sewage_mode=1, sewage_rate=0.0, num_units=20)
    assert predio == pytest.approx(20 * _agua(15.0))


def test_a_estrutura_e_lida_e_validada_como_exponencial():
    est = ler_estrutura(TABELA)
    assert est.regime == EXPONENCIAL
    assert est.preco_base == 9.15 and est.teto_exponencial_m3 == 1000.0
    assert [n for *_, n in est.expoentes] == [1.00, 1.05, 1.10]
    assert validar_estrutura({"faixas": TABELA, "tarifa_fixa_mensal": 43.39}) == []
    assert diagnosticar(TABELA).responde_ao_consumo
    assert "PB × Cⁿ" in resumo_do_regime({"faixas": TABELA})


@pytest.mark.parametrize("defeito, codigo", [
    ([f for f in TABELA if f[3] != EXPOENTE_DE_CONSUMO], "sem_tabela_exponencial"),
    ([f for f in TABELA if f[:2] != (10.0, 20.0)], "lacuna_na_tabela_exponencial"),
    ([f if f[:2] != (20.0, 1000.0) else (20.0, 500.0, 1.1, 3) for f in TABELA], "tabela_exponencial_truncada"),
    ([f if f[:2] != (20.0, 1000.0) else (20.0, 1000.0, 3.0, 3) for f in TABELA], "expoente_implausivel"),
])
def test_a_validacao_aponta_a_tabela_exponencial_defeituosa(defeito, codigo):
    achados = {a.codigo: a.gravidade for a in validar_estrutura({"faixas": defeito})}
    assert achados.get(codigo) == "erro"


def test_os_34_municipios_da_corsan_estao_na_formula_exponencial():
    base = json.loads((RAIZ / "netuno" / "data" / "brazil_cities_tariffs.json").read_text(encoding="utf-8"))
    corsan = {k: v for k, v in base["cities"].items() if "CORSAN" in v["prestador_saneamento"].upper()}
    assert len(corsan) == 34
    for chave, dados in corsan.items():
        assert dados["regime_tarifario"] == EXPONENCIAL, chave
        assert ler_estrutura(dados["faixas"]).regime == EXPONENCIAL, chave
        erros = [a for a in validar_estrutura(dados) if a.gravidade == "erro"]
        assert erros == [], (chave, erros)


def test_a_tabela_pendente_e_declarada_e_nao_escondida():
    """Enquanto a tabela homologada não for transcrita, o aviso acompanha a cidade."""
    tabela = json.loads((RAIZ / "tarifas" / "tabela_exponencial_corsan.json").read_text(encoding="utf-8"))
    alegrete = get_city_data("RS", "Alegrete")
    assert alegrete["expoentes_verificados"] is bool(tabela["verificada"])
    avisos = {a.codigo for a in validar_estrutura(alegrete)}
    assert ("expoentes_pendentes" in avisos) is (not tabela["verificada"])


def test_as_faixas_da_base_reproduzem_a_tabela_unica():
    tabela = json.loads((RAIZ / "tarifas" / "tabela_exponencial_corsan.json").read_text(encoding="utf-8"))
    alegrete = get_city_data("RS", "Alegrete")
    gravados = [f[:3] for f in alegrete["faixas"] if int(f[3]) == EXPOENTE_DE_CONSUMO]
    assert gravados == [[float(a), float(b), float(n)] for a, b, n in tabela["expoentes"]]


def test_o_script_de_aplicacao_e_idempotente():
    spec = importlib.util.spec_from_file_location("aplicar", RAIZ / "scripts" / "aplicar_tarifa_exponencial.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    base = json.loads(modulo.BANCO.read_text(encoding="utf-8"))
    antes = json.dumps(base["cities"], sort_keys=True)
    assert len(modulo.aplicar(base["cities"], modulo.carregar_tabela())) == 34
    assert json.dumps(base["cities"], sort_keys=True) == antes


def test_a_categoria_escala_o_preco_base_e_nao_o_expoente():
    residencial = get_city_tariffs_by_category("RS", "Alegrete", "residencial")
    comercial = get_city_tariffs_by_category("RS", "Alegrete", "comercial")
    for r, c in zip(residencial["faixas"], comercial["faixas"]):
        if int(r[3]) == EXPOENTE_DE_CONSUMO:
            assert c[2] == r[2]
        elif int(r[3]) == PRECO_BASE_EXPONENCIAL:
            assert c[2] > r[2]


def test_parcela_exponencial_sem_preco_base_e_zero():
    assert parcela_exponencial([(0.0, 999999.0, 5.0, 1)], 10.0) == 0.0
    assert parcela_exponencial(TABELA, 0.0) == 0.0


# ── interface ────────────────────────────────────────────────────────────────

def test_o_gestor_mostra_a_formula_e_simula_com_o_motor(qapp):
    from netuno.ui.tab_tariffs_manager import TabTariffsManager

    tab = TabTariffsManager()
    tab.load_city_tariffs("RS", "Alegrete", "residencial")
    assert "Fórmula exponencial" in tab.lbl_disp_callout.text()
    tipos = [tab.table_tiers.item(r, 3).text() for r in range(tab.table_tiers.rowCount())]
    assert "Preço-base (PB × Cⁿ)" in tipos and "Expoente n" in tipos

    # Editar o expoente muda a conta simulada, pela fórmula.
    linha = tipos.index("Expoente n")
    tab.table_tiers.item(linha, 2).setText("1.1000")
    tab.spin_sim_vol.setValue(15.0)
    tab.update_bill_simulation()
    esperado = (43.39 + 9.15 * 15 ** 1.1) * 1.70
    assert f"Total: R$ {esperado:.2f}/mês" in tab.lbl_sim_result.text()
    assert "PB × Cⁿ" in tab.lbl_sim_result.text()
    assert tab._faixas_da_tabela()[linha] == [0.0, 1000.0, 1.1, EXPOENTE_DE_CONSUMO]


def test_a_etapa_economica_preserva_a_tabela_exponencial(qapp):
    from netuno.core.parser import NetunoConfig
    from netuno.ui.dialogs.dialog_economic import DialogTariffs

    cfg = NetunoConfig()
    cfg.water_tariffs = list(TABELA)
    dialogo = DialogTariffs(config=cfg)
    dialogo.populate_table_from_tariffs(TABELA)
    dialogo.on_accept()
    assert cfg.water_tariffs == TABELA


def test_o_manual_compoe_o_expoente_sobrescrito():
    """Com espaço em volta do ^, o mathtext punha o expoente na linha de base."""
    import sys

    sys.path.insert(0, str(RAIZ / "manual"))
    import gerar_equacoes

    assert gerar_equacoes.para_tex("T_agua = PB × C^n + SB").count("C^{n}") == 1
    assert "( 1 + i )^{m - 1}" in gerar_equacoes.para_tex("f_inf = ( 1 + i )^( m − 1 )")
    assert "^{2}" in gerar_equacoes.para_tex("A = x²")
