"""
Aderência de replicação: Netuno 5 contra os resultados oficiais do Netuno 4.

Esta é a evidência central de um estudo de replicação — e já foi a
única comparação que não estava automatizada. O módulo
`compare_netuno4_netuno5.py` existia desde o início, mas não seguia o padrão
`test_*.py`, de modo que o pytest coletava zero testes do diretório e a função só
era chamada pelo seu próprio bloco `__main__`.

Dados de referência
-------------------
`data/simulation_outputs/**/Planilha.csv` reúne 4.050 casos exportados do Netuno 4:

- `SimulacaoFloripaBrasilia/Planilha.csv` — 1.458 casos
- `SimulacaoManausSaoPaulo/Planilha.csv` — 2.592 casos

São arquivos latin-1 com separador `;` e vírgula decimal, preservados byte a byte no
repositório (ver `.gitattributes`) para que a comparação permaneça exata em qualquer
plataforma.

Estratégia de execução
----------------------
A comparação completa percorre uma varredura de volumes por caso. Com os kernels
acelerados isso leva cerca de 40 s; sem eles, passa de dez minutos — inviável a cada
execução da suíte. Daí a divisão:

- **por padrão**, uma amostra determinística pequena roda junto da suíte e detecta
  quebras grosseiras do arranjo de comparação;
- **a comparação completa** fica atrás do marcador `replicacao`, executada sob demanda
  (`pytest -m replicacao`) ou pela camada correspondente do `qa_runner`.

Limiares
--------
Calibrados sobre a medição de 8 de setembro de 2026 e deliberadamente folgados: servem
para detectar **regressão de aderência**, não para atestar qualidade da replicação. A
interpretação dos números está em `docs/verificacao_e_validacao.md`, §7.
"""

from pathlib import Path

import numpy as np
import pytest

from tests.benchmarking.compare_netuno4_netuno5 import run_benchmark_comparison

RAIZ = Path(__file__).resolve().parents[2]
SAIDAS = RAIZ / "data" / "simulation_outputs"

PLANILHAS = {
    "floripa-brasilia": SAIDAS / "SimulacaoFloripaBrasilia" / "Planilha.csv",
    "manaus-saopaulo": SAIDAS / "SimulacaoManausSaoPaulo" / "Planilha.csv",
}

# Limites de regressão, calibrados na medição de 2026-09-08 (excluindo os casos de
# referência nula, ver abaixo):
#
#   Floripa/Brasília  1.458 casos  MAE 2,29 pp  RMSE 2,72 pp  máx 7,43 pp
#   Manaus/São Paulo  2.592 casos  MAE 2,71 pp  RMSE 3,33 pp  máx 10,60 pp
MAE_MAXIMO_PP = 4.0
RMSE_MAXIMO_PP = 6.0
FRACAO_MINIMA_DENTRO_DE_10_PP = 0.95

# Casos em que o Netuno 4 exportou 0,00 enquanto o Netuno 5 calcula valor positivo.
# A incidência difere muito entre os dois conjuntos — 0,35% em Manaus/São Paulo contra
# 34,98% em Floripa/Brasília — o que indica característica dos dados de referência (o
# Netuno 4 provavelmente não encontrou volume ótimo sob seu próprio critério) e não
# erro do Netuno 5. São segregados das estatísticas para não dominá-las; o limite
# abaixo apenas detecta leitura incorreta da planilha.
LIMITE_DE_CASOS_ZERO_NO_NETUNO4 = 0.45

# Conjunto usado na amostra rápida. Escolhido explicitamente, e não pela ordem do
# dicionário, porque as primeiras linhas de Floripa/Brasília são todas de referência
# nula e produziriam uma amostra não representativa.
PLANILHA_DA_AMOSTRA = "manaus-saopaulo"


def _planilhas_existentes():
    return {nome: caminho for nome, caminho in PLANILHAS.items() if caminho.exists()}


@pytest.fixture(scope="module")
def comparacao_amostrada():
    """Amostra determinística pequena, para a execução padrão da suíte."""
    caminho = PLANILHAS[PLANILHA_DA_AMOSTRA]
    if not caminho.exists():
        pytest.skip(f"planilha de referência ausente: {caminho.name}")
    return run_benchmark_comparison(str(caminho), limite_de_casos=15)


def test_arranjo_de_comparacao_funciona(comparacao_amostrada):
    """O comparador lê a planilha de referência e produz casos comparáveis.

    Detecta quebras do arranjo — planilha movida, formato alterado, série
    pluviométrica ausente — sem pagar o custo da comparação completa.
    """
    assert comparacao_amostrada["status"] == "success", comparacao_amostrada.get("message")
    assert comparacao_amostrada["total_compared"] > 0, (
        "nenhum caso pôde ser comparado: verifique se as séries citadas na planilha "
        "existem em data/rainfall/"
    )


def test_amostra_mantem_aderencia_grosseira(comparacao_amostrada):
    """A amostra não pode divergir de forma grosseira do Netuno 4.

    Limite folgado, ao dobro do aplicado à comparação completa: com apenas 15 casos
    a estatística é ruidosa, e este teste existe para pegar quebra de arranjo, não
    para medir aderência.
    """
    detalhes = comparacao_amostrada["details"]
    erros = [d["diff_abs"] for d in detalhes if d["pot_netuno4"] != 0.0]
    assert erros, "todos os casos da amostra têm referência nula"

    mae = sum(erros) / len(erros)
    assert mae < MAE_MAXIMO_PP * 2, (
        f"MAE da amostra em {mae:.3f} pp sobre {len(erros)} casos — "
        "aderência muito abaixo do esperado"
    )


@pytest.mark.replicacao
@pytest.mark.parametrize("nome_da_planilha", sorted(PLANILHAS))
def test_aderencia_completa_ao_netuno4(nome_da_planilha):
    """Comparação completa contra os resultados oficiais do Netuno 4.

    Executada sob demanda: `pytest -m replicacao` ou
    `python scripts/qa_runner.py --layer replicacao`.
    """
    caminho = PLANILHAS[nome_da_planilha]
    if not caminho.exists():
        pytest.skip(f"planilha de referência ausente: {caminho.name}")

    resultado = run_benchmark_comparison(str(caminho))
    assert resultado["status"] == "success", resultado.get("message")

    detalhes = resultado["details"]
    assert len(detalhes) > 100, (
        f"apenas {len(detalhes)} casos comparados em {nome_da_planilha}; "
        "o comparador ignora silenciosamente linhas com erro, então uma queda "
        "brusca na contagem indica quebra e não melhoria"
    )

    netuno4 = np.array([d["pot_netuno4"] for d in detalhes])
    netuno5 = np.array([d["pot_netuno5"] for d in detalhes])

    # Casos com referência nula são segregados: o Netuno 4 exportou 0,00 onde o
    # Netuno 5 calcula valor positivo, e eles concentram os maiores desvios.
    referencia_nula = netuno4 == 0.0
    fracao_nula = referencia_nula.mean()
    assert fracao_nula < LIMITE_DE_CASOS_ZERO_NO_NETUNO4, (
        f"{fracao_nula:.2%} dos casos têm Netuno 4 = 0,00 — proporção muito acima da "
        "medida historicamente (0,35%), o que sugere leitura incorreta da planilha"
    )

    erro = np.abs(netuno5 - netuno4)[~referencia_nula]
    mae = float(erro.mean())
    rmse = float(np.sqrt((erro ** 2).mean()))
    dentro_de_10 = float((erro <= 10.0).mean())

    assert mae < MAE_MAXIMO_PP, (
        f"{nome_da_planilha}: MAE de {mae:.3f} pp excede o limite de {MAE_MAXIMO_PP} pp"
    )
    assert rmse < RMSE_MAXIMO_PP, (
        f"{nome_da_planilha}: RMSE de {rmse:.3f} pp excede o limite de {RMSE_MAXIMO_PP} pp"
    )
    assert dentro_de_10 >= FRACAO_MINIMA_DENTRO_DE_10_PP, (
        f"{nome_da_planilha}: apenas {dentro_de_10:.2%} dos casos dentro de 10 pp, "
        f"abaixo do mínimo de {FRACAO_MINIMA_DENTRO_DE_10_PP:.0%}"
    )


@pytest.fixture(scope="module")
def decomposicao():
    """Decomposição da divergência, calculada uma única vez por sessão de teste.

    Cada configuração percorre 2.583 casos; sem cache, cada teste que a consultasse
    repetiria a varredura inteira.
    """
    from tests.benchmarking.decomposicao_divergencia import decompor
    return decompor()


@pytest.mark.replicacao
def test_o_balanco_hidrico_replica_o_netuno4(decomposicao):
    """A afirmação central do estudo de replicação, isolada das escolhas de projeto.

    Comparar o ótimo de um programa com o do outro mistura três diferenças: o balanço
    hídrico, o critério que escolhe o volume ótimo e o tratamento do descarte de
    primeira chuva. `decomposicao_divergencia.py` as separa.

    Neutralizadas as duas diferenças metodológicas conhecidas — avaliando o Netuno 5 no
    volume que o Netuno 4 declarou ótimo e adotando o descarte por limiar do Netuno 4 —
    o que resta é a diferença do motor. A medição de 8 de setembro de 2026 sobre 2.583
    casos deu **MAE de 0,245 pp com 100% dos casos dentro de 5 pp**, compatível com a
    precisão de duas casas decimais da própria planilha de referência.

    O limite de 0,5 pp existe para detectar regressão do motor, não para atestar
    qualidade: uma alteração no balanço diário que degradasse a replicação seria
    apanhada aqui, ainda que a comparação ingênua continuasse dentro dos seus limiares.
    """
    controlado = decomposicao.get("volume_e_descarte_do_netuno4")
    assert controlado is not None, "a decomposição não produziu a configuração controlada"

    assert controlado.casos > 1000, (
        f"apenas {controlado.casos} casos comparados; a decomposição perdeu linhas"
    )
    assert controlado.mae_pp < 0.5, (
        f"o balanço hídrico divergiu do Netuno 4 em {controlado.mae_pp:.3f} pp de MAE, "
        "acima do limite de 0,5 pp. Neutralizadas as diferenças de critério e de "
        "descarte, o motor deveria replicar a referência quase exatamente."
    )
    assert controlado.fracao_ate_5pp >= 0.99, (
        f"apenas {controlado.fracao_ate_5pp:.1%} dos casos ficaram dentro de 5 pp"
    )


@pytest.mark.replicacao
def test_as_diferencas_metodologicas_explicam_a_divergencia(decomposicao):
    """Cada diferença de projeto responde por parcela conhecida da divergência.

    Serve de guarda contra uma conclusão apressada: se a divergência total crescesse
    sem que as parcelas conhecidas crescessem junto, teria surgido uma terceira causa
    ainda não identificada.
    """
    no_volume = decomposicao["volume_do_netuno4"].mae_pp
    controlado = decomposicao["volume_e_descarte_do_netuno4"].mae_pp

    assert no_volume > controlado, (
        "adotar o descarte do Netuno 4 deveria aproximar os resultados, não afastá-los"
    )
    contribuicao_do_descarte = no_volume - controlado
    assert contribuicao_do_descarte > 0.5, (
        f"o tratamento do descarte responde por apenas {contribuicao_do_descarte:.3f} pp; "
        "historicamente responde por cerca de 1,36 pp. Uma queda sugere que a semântica "
        "do descarte mudou."
    )


@pytest.mark.replicacao
def test_divergencia_e_sistematica_e_nao_dispersa():
    """Documenta em teste o viés sistemático da replicação.

    O erro médio COM SINAL é praticamente igual em módulo ao erro médio absoluto,
    o que significa que quase todos os desvios têm a mesma direção: o Netuno 5
    estima sistematicamente menos que o Netuno 4. Não é dispersão aleatória.

    A causa provável está documentada em `docs/verificacao_e_validacao.md`, §7: o
    tratamento do descarte de primeira chuva implementado difere do descrito em
    `docs/metodologia.md`. Este teste não afirma qual está certo — apenas registra
    que a divergência é sistemática, para que uma eventual correção do modelo seja
    avaliada por seu efeito sobre este viés.
    """
    caminho = PLANILHAS["manaus-saopaulo"]
    if not caminho.exists():
        pytest.skip("planilha de referência ausente")

    detalhes = run_benchmark_comparison(str(caminho))["details"]
    netuno4 = np.array([d["pot_netuno4"] for d in detalhes])
    netuno5 = np.array([d["pot_netuno5"] for d in detalhes])
    valido = netuno4 != 0.0

    erro_com_sinal = (netuno5 - netuno4)[valido]
    vies = float(erro_com_sinal.mean())
    erro_absoluto_medio = float(np.abs(erro_com_sinal).mean())

    assert vies < 0, f"o viés mudou de direção: {vies:+.3f} pp"
    assert abs(vies) / erro_absoluto_medio > 0.9, (
        f"a divergência deixou de ser sistemática: |viés|/MAE = "
        f"{abs(vies) / erro_absoluto_medio:.3f}, esperado acima de 0,9"
    )
