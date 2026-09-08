"""
Matriz multi-cenários: execução fatorial e exportação no formato do Netuno 4.

`netuno/core/scenarios.py` estava com 33% de cobertura. É o módulo que executa lotes
fatoriais de simulação — a base dos estudos de tipologias — e o que exporta os
resultados no formato de planilha do Netuno 4.

O teste mais relevante aqui confronta a afirmação do próprio código. O docstring de
`export_matrix_planilha_csv` diz produzir um arquivo *"matching Netuno 4.0 exact matrix
format"*; como o repositório versiona planilhas reais exportadas do Netuno 4, essa
afirmação é verificável, e não precisa ser aceita por confiança.

Os testes rodam com `parallel=False`: a execução paralela usa `ProcessPoolExecutor`, e
forçar o caminho sequencial mantém a suíte determinística e rápida.
"""

from pathlib import Path

import pytest

from netuno.core.scenarios import (
    export_matrix_planilha_csv,
    run_multi_scenario_matrix,
)

RAIZ = Path(__file__).resolve().parents[2]
CHUVA = RAIZ / "data" / "rainfall"
REFERENCIA_NETUNO4 = (RAIZ / "data" / "simulation_outputs" /
                      "SimulacaoManausSaoPaulo" / "Planilha.csv")


def _series(*nomes):
    disponiveis = [(nome.split(".")[0], str(CHUVA / nome))
                   for nome in nomes if (CHUVA / nome).exists()]
    if not disponiveis:
        pytest.skip("séries pluviométricas ausentes em data/rainfall/")
    return disponiveis


@pytest.fixture(scope="module")
def matriz_pequena():
    """Matriz fatorial mínima, executada em modo sequencial."""
    return run_multi_scenario_matrix(
        precip_files=_series("Florianopolis1.csv"),
        areas=[100.0, 200.0],
        residents_list=[4],
        demands_per_capita=[150.0],
        rainwater_shares=[0.4],
        lower_tanks=[5000.0],
        run_as_sweeps=False,
        parallel=False,
    )


# ---------------------------------------------------------------------------------
# Execução da matriz
# ---------------------------------------------------------------------------------

def test_matriz_executa_o_produto_cartesiano(matriz_pequena):
    """Cada combinação de parâmetros vira exatamente um cenário executado."""
    assert matriz_pequena.total_scenarios_run == 2, (
        f"esperadas 2 combinações, obtidas {matriz_pequena.total_scenarios_run}"
    )
    assert len(matriz_pequena.outputs) == 2


def test_cada_cenario_produz_resultado(matriz_pequena):
    """Nenhum cenário pode voltar vazio: um lote silenciosamente incompleto é pior
    que um lote que falha, porque entra no estudo sem ser notado."""
    for saida in matriz_pequena.outputs:
        assert saida.result is not None or saida.sweep_result is not None, (
            f"cenário {saida.scenario.scenario_id} não produziu resultado"
        )


def test_parametros_do_cenario_sao_preservados(matriz_pequena):
    """Os parâmetros que definiram a combinação chegam íntegros ao resultado."""
    areas = sorted(saida.scenario.area for saida in matriz_pequena.outputs)
    assert areas == [100.0, 200.0]
    for saida in matriz_pequena.outputs:
        assert saida.scenario.residents == 4
        assert saida.scenario.demand_per_capita == pytest.approx(150.0)
        assert saida.scenario.total_demand_l_day == pytest.approx(600.0), (
            "demanda total deveria ser demanda per capita × moradores"
        )


def test_area_maior_nao_reduz_a_economia(matriz_pequena):
    """A matriz herda a monotonicidade do motor: mais captação, não menos economia."""
    por_area = {}
    for saida in matriz_pequena.outputs:
        resultado = saida.result or saida.sweep_result
        economia = getattr(resultado, "potential_potable_savings_pct", None)
        if economia is None:
            economia = getattr(resultado, "optimal_potential_pct", None)
        if economia is not None:
            por_area[saida.scenario.area] = economia

    if len(por_area) == 2:
        assert por_area[200.0] >= por_area[100.0] - 1e-9, (
            f"economia caiu com área maior: {por_area}"
        )


def test_callback_de_progresso_e_chamado_uma_vez_por_cenario():
    """A interface depende do callback para a barra de progresso do lote."""
    chamadas = []

    run_multi_scenario_matrix(
        precip_files=_series("Florianopolis1.csv"),
        areas=[100.0, 150.0, 200.0],
        residents_list=[4],
        demands_per_capita=[150.0],
        rainwater_shares=[0.4],
        lower_tanks=[5000.0],
        run_as_sweeps=False,
        parallel=False,
        progress_callback=lambda atual, total, saida, resumo: chamadas.append((atual, total)),
    )

    assert len(chamadas) == 3, f"callback chamado {len(chamadas)} vezes para 3 cenários"
    assert all(total == 3 for _, total in chamadas), "o total informado ao callback oscilou"
    assert [atual for atual, _ in chamadas] == [1, 2, 3], (
        f"a contagem de progresso não foi sequencial: {chamadas}"
    )


# ---------------------------------------------------------------------------------
# Exportação no formato do Netuno 4
# ---------------------------------------------------------------------------------

def test_exportacao_gera_arquivo_com_uma_linha_por_cenario(matriz_pequena, tmp_path):
    """O arquivo exportado tem cabeçalho mais uma linha por cenário."""
    destino = tmp_path / "Planilha.csv"
    export_matrix_planilha_csv(matriz_pequena, str(destino))

    assert destino.exists()
    linhas = [l for l in destino.read_text(encoding="latin-1").splitlines() if l.strip()]
    assert len(linhas) == 1 + len(matriz_pequena.outputs), (
        f"{len(linhas)} linhas para {len(matriz_pequena.outputs)} cenários mais cabeçalho"
    )


def test_cabecalho_exportado_coincide_com_a_planilha_real_do_netuno4(matriz_pequena, tmp_path):
    """Confronta a afirmação do código com os dados de referência.

    `export_matrix_planilha_csv` declara produzir o formato exato do Netuno 4. Como o
    repositório versiona planilhas realmente exportadas pelo Netuno 4, a afirmação é
    verificável: os cabeçalhos devem coincidir coluna a coluna.
    """
    if not REFERENCIA_NETUNO4.exists():
        pytest.skip("planilha de referência do Netuno 4 ausente")

    destino = tmp_path / "Planilha.csv"
    export_matrix_planilha_csv(matriz_pequena, str(destino))

    cabecalho_exportado = destino.read_text(encoding="latin-1").splitlines()[0]
    cabecalho_referencia = REFERENCIA_NETUNO4.read_text(encoding="latin-1").splitlines()[0]

    colunas_exportadas = [c.strip() for c in cabecalho_exportado.split(";") if c.strip()]
    colunas_referencia = [c.strip() for c in cabecalho_referencia.split(";") if c.strip()]

    assert colunas_exportadas == colunas_referencia, (
        "o cabeçalho exportado difere do produzido pelo Netuno 4.\n"
        f"  exportado : {colunas_exportadas}\n"
        f"  referência: {colunas_referencia}"
    )


def test_exportacao_usa_virgula_decimal(matriz_pequena, tmp_path):
    """O formato do Netuno 4 usa vírgula decimal; ponto quebraria a releitura."""
    destino = tmp_path / "Planilha.csv"
    export_matrix_planilha_csv(matriz_pequena, str(destino))

    primeira_linha_de_dados = destino.read_text(encoding="latin-1").splitlines()[1]
    campos = primeira_linha_de_dados.split(";")
    numericos = [c for c in campos if c and any(d.isdigit() for d in c)]
    assert numericos, "a linha exportada não contém campos numéricos"
    assert not any("." in campo and "," not in campo and campo.replace(".", "").isdigit()
                   for campo in numericos), (
        f"campo numérico com ponto decimal na exportação: {numericos}"
    )


def test_planilha_exportada_e_relida_pelo_comparador_de_replicacao(matriz_pequena, tmp_path):
    """Fecha o ciclo: o que o Netuno 5 exporta é lido pelo comparador de replicação.

    Garante que a exportação não é apenas parecida com o formato do Netuno 4, mas
    efetivamente consumível pelo mesmo leitor usado na comparação oficial.
    """
    import pandas as pd

    destino = tmp_path / "Planilha.csv"
    export_matrix_planilha_csv(matriz_pequena, str(destino))

    df = pd.read_csv(destino, sep=";", decimal=",", encoding="latin1", engine="python")
    assert len(df) == len(matriz_pequena.outputs)
    # Coluna 1 nomeia a série pluviométrica, como o comparador espera (row.iloc[1]).
    assert str(df.iloc[0, 1]).endswith(".csv"), (
        f"a segunda coluna deveria nomear a série pluviométrica, obtido {df.iloc[0, 1]!r}"
    )
