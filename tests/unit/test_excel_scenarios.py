"""
Cenários em planilha: geração do modelo, leitura, grade fatorial e exportação.

`netuno/core/excel_scenarios.py` estava com 14% de cobertura — o menor índice do
núcleo de cálculo. É o caminho pelo qual o usuário descreve lotes de simulação numa
planilha, e um erro aqui corrompe silenciosamente todo um estudo, sem se manifestar
como exceção.

O teste central é de **ida e volta**: o modelo gerado pelo próprio programa precisa
ser legível pelo próprio programa. Um descompasso entre o que se escreve e o que se lê
é o modo de falha mais provável nesta família de funções, e não seria detectado
testando as duas metades isoladamente.
"""

import io
from pathlib import Path

import pytest

from netuno.core.excel_scenarios import (
    export_scenarios_to_excel_bytes,
    generate_factorial_grid,
    generate_sample_scenario_excel,
    parse_excel_scenarios,
    run_parsed_scenarios,
)

SERIES = Path(__file__).resolve().parents[2] / "data" / "rainfall"


# ---------------------------------------------------------------------------------
# Ida e volta: gerar o modelo e relê-lo
# ---------------------------------------------------------------------------------

def test_modelo_gerado_pelo_programa_e_legivel_pelo_programa(tmp_path):
    """O modelo de planilha distribuído ao usuário precisa ser lido de volta.

    Se gerador e leitor divergirem nos nomes de coluna, o usuário recebe um modelo
    que o próprio programa não entende.
    """
    destino = tmp_path / "modelo.xlsx"
    caminho = generate_sample_scenario_excel(str(destino))
    assert Path(caminho).exists(), "o modelo de cenários não foi gravado"

    cenarios = parse_excel_scenarios(str(destino))
    assert cenarios, "o modelo gerado pelo programa não produziu nenhum cenário ao ser lido"

    for cenario in cenarios:
        assert cenario.get("scenario_name"), "cenário sem nome após a leitura"
        assert float(cenario.get("area", 0)) > 0, f"área inválida em {cenario}"


def test_modelo_gerado_pelo_programa_roda_com_as_series_distribuidas(tmp_path):
    """Cada série citada no modelo existe em data/rainfall, e o modelo roda.

    O modelo já apontou para uma série que não era distribuída: o exemplo
    entregue ao usuário falhava na primeira execução.
    """
    destino = tmp_path / "modelo.xlsx"
    cenarios = parse_excel_scenarios(generate_sample_scenario_excel(str(destino)))
    for cenario in cenarios:
        assert (SERIES / Path(cenario["precip_file"]).name).exists(), cenario["precip_file"]
    resultados = run_parsed_scenarios(cenarios[:1])
    assert len(resultados) == 1


def test_serie_ausente_e_erro_claro_e_nunca_troca_silenciosa(tmp_path):
    """Sem a série do cenário, o erro diz qual cenário e qual arquivo.

    Trocar em silêncio pela chuva de outra cidade daria um resultado plausível
    e errado.
    """
    destino = tmp_path / "modelo.xlsx"
    cenarios = parse_excel_scenarios(generate_sample_scenario_excel(str(destino)))[:1]
    cenarios[0]["precip_file"] = "Cidade_Inexistente.csv"
    with pytest.raises(FileNotFoundError, match=r"Cenário '.+': série de chuva 'Cidade_Inexistente.csv' não encontrada"):
        run_parsed_scenarios(cenarios)


def test_leitura_aceita_planilha_em_memoria(tmp_path):
    """A leitura funciona a partir de bytes, e não apenas de caminho em disco."""
    destino = tmp_path / "modelo.xlsx"
    generate_sample_scenario_excel(str(destino))

    do_disco = parse_excel_scenarios(str(destino))
    da_memoria = parse_excel_scenarios(destino.read_bytes())

    assert len(da_memoria) == len(do_disco)
    assert [c["scenario_name"] for c in da_memoria] == [c["scenario_name"] for c in do_disco]


def test_leitura_de_csv_com_separador_detectado(tmp_path):
    """Planilhas exportadas como CSV também são aceitas."""
    csv = tmp_path / "cenarios.csv"
    csv.write_text(
        "cenario;area;moradores;demanda;percentual;reservatorio\n"
        "Residencial A;120;4;150;40;5000\n"
        "Residencial B;250;6;150;50;8000\n",
        encoding="utf-8",
    )
    cenarios = parse_excel_scenarios(str(csv))
    assert len(cenarios) == 2
    assert cenarios[0]["scenario_name"] == "Residencial A"
    assert float(cenarios[0]["area"]) == pytest.approx(120.0)


def test_leitura_usa_nome_padrao_quando_a_coluna_falta(tmp_path):
    """Sem coluna de nome, os cenários recebem identificação sequencial.

    Evita que linhas anônimas se confundam num relatório de lote.
    """
    csv = tmp_path / "sem_nome.csv"
    csv.write_text("area;moradores;demanda\n100;4;150\n200;4;150\n", encoding="utf-8")

    cenarios = parse_excel_scenarios(str(csv))
    assert len(cenarios) == 2
    nomes = [c["scenario_name"] for c in cenarios]
    assert len(set(nomes)) == 2, f"cenários sem nome não foram distinguidos: {nomes}"


# ---------------------------------------------------------------------------------
# Grade fatorial
# ---------------------------------------------------------------------------------

def test_grade_fatorial_tem_o_produto_cartesiano_completo():
    """A contagem de combinações é o produto das dimensões — sem faltar nem repetir."""
    grade = generate_factorial_grid(
        precip_files=[("Floripa", "Florianopolis1.csv"), ("Manaus", "Manaus1.csv")],
        areas=[100.0, 200.0, 300.0],
        residents_list=[2, 4],
        demands_per_capita=[150.0],
        rainwater_shares=[0.4, 0.5],
        lower_tanks=[5000.0],
    )
    esperado = 2 * 3 * 2 * 1 * 2
    assert len(grade) == esperado, (
        f"grade fatorial com {len(grade)} combinações, esperado {esperado}"
    )


def test_grade_fatorial_gera_nomes_unicos():
    """Nomes repetidos sobrescreveriam resultados na consolidação do lote."""
    grade = generate_factorial_grid(
        precip_files=[("Floripa", "Florianopolis1.csv")],
        areas=[100.0, 200.0],
        residents_list=[2, 4],
        demands_per_capita=[150.0, 200.0],
        rainwater_shares=[0.4],
        lower_tanks=[5000.0],
    )
    nomes = [c["scenario_name"] for c in grade]
    assert len(set(nomes)) == len(nomes), "a grade fatorial gerou nomes duplicados"


def test_grade_fatorial_preserva_os_valores_de_entrada():
    """Cada combinação carrega exatamente os parâmetros que a originaram."""
    areas = [80.0, 160.0]
    grade = generate_factorial_grid(
        precip_files=[("Floripa", "Florianopolis1.csv")],
        areas=areas,
        residents_list=[3],
        demands_per_capita=[180.0],
        rainwater_shares=[0.45],
        lower_tanks=[6000.0],
    )
    assert sorted({float(c["area"]) for c in grade}) == sorted(areas)
    for cenario in grade:
        assert cenario["city_label"] == "Floripa"
        assert cenario["precip_file"] == "Florianopolis1.csv"


def test_grade_fatorial_vazia_quando_uma_dimensao_e_vazia():
    """Produto cartesiano com fator vazio é vazio — não deve gerar combinação órfã."""
    grade = generate_factorial_grid(
        precip_files=[],
        areas=[100.0],
        residents_list=[4],
        demands_per_capita=[150.0],
        rainwater_shares=[0.4],
        lower_tanks=[5000.0],
    )
    assert grade == []


# ---------------------------------------------------------------------------------
# Exportação
# ---------------------------------------------------------------------------------

def test_exportacao_produz_planilha_legivel():
    """O que é exportado precisa ser reabrível como planilha."""
    resultados = [
        {"scenario_name": "Cenario A", "city_label": "Floripa", "area": 120.0,
         "potential_savings_pct": 42.5, "optimal_volume_l": 5000.0},
        {"scenario_name": "Cenario B", "city_label": "Manaus", "area": 250.0,
         "potential_savings_pct": 61.2, "optimal_volume_l": 8000.0},
    ]
    conteudo = export_scenarios_to_excel_bytes(resultados)
    assert isinstance(conteudo, (bytes, bytearray)) and len(conteudo) > 0

    import openpyxl

    planilha = openpyxl.load_workbook(io.BytesIO(conteudo))
    aba = planilha[planilha.sheetnames[0]]
    assert aba.max_row >= len(resultados), "a planilha exportada perdeu linhas"

    texto = " ".join(
        str(celula.value)
        for linha in aba.iter_rows()
        for celula in linha
        if celula.value is not None
    )
    assert "Cenario A" in texto and "Cenario B" in texto, (
        "os nomes dos cenários não sobreviveram à exportação"
    )


def test_exportacao_de_lista_vazia_nao_quebra():
    """Um lote sem resultados exporta planilha vazia em vez de estourar exceção."""
    conteudo = export_scenarios_to_excel_bytes([])
    assert isinstance(conteudo, (bytes, bytearray))
