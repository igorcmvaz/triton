# -*- coding: utf-8 -*-
"""Porto e Funchal: o JSON transcrito bate com os PDFs oficiais, e as contas são refeitas à mão.

Os valores abaixo foram lidos, na rodada 4 da auditoria, dos documentos oficiais guardados fora do
Git (``tarifas_portugal/fontes/``):

- Águas e Energia do Porto, *Tarifário 2026* (``Tarifario_Geral_2026.pdf``): abastecimento de água e
  águas residuais, utilizadores domésticos, páginas 2 e 3;
- Câmara Municipal do Funchal, *Tabela de Taxas e Outras Receitas Municipais 2026*
  (``Tabela_de_Taxas_Municipais_2026_.pdf``): artigos 6.º, 10.º, 56.º e 57.º, «Valor final sem IVA».

As contas de conferência são refeitas com ``Decimal`` e a aritmética escrita aqui, sem passar
por nenhum código do Triton: assim o teste não repete o erro do código que verifica.
Só a Edição Ibérica traz os tarifários; os testes estão em ``tests/so_da_ibe.txt`` (arquivo inteiro).
"""

from decimal import Decimal as D

import pytest

from triton.core import tarifarios_portugal as T

# Mês de 30 dias, como nos escalões do tarifário do Porto («/30 dias»).
DIAS_DO_MES = 30


def _por_faixas(faixas, m3):
    """Cada m³ paga o preço da sua faixa; ``faixas`` = [(início, fim ou None, preço)]."""
    total = D(0)
    for inicio, fim, preco in faixas:
        topo = D(m3) if fim is None else min(D(m3), D(fim))
        if topo > D(inicio):
            total += (topo - D(inicio)) * D(preco)
    return total


# --- Porto -------------------------------------------------------------------------------

PORTO_AGUA = [(0, 5, "0.4945"), (5, 15, "0.9649"), (15, 25, "1.7657"), (25, None, "3.0016")]
PORTO_ESGOTO = [(0, 5, "0.3875"), (5, 15, "0.7606"), (15, 25, "1.4608"), (25, None, "2.4423")]
PORTO_DISPONIBILIDADE_AGUA_ATE_20MM = D("0.1242")   # €/dia, pág. 2, «Utilizadores domésticos»
PORTO_DISPONIBILIDADE_ESGOTO = D("0.0665")          # €/dia, pág. 3
PORTO_TRH_AGUA = D("0.0392")                        # €/m³, pág. 3
PORTO_IVA = D("1.06")


def _conta_do_porto(m3):
    agua = D(DIAS_DO_MES) * PORTO_DISPONIBILIDADE_AGUA_ATE_20MM + _por_faixas(PORTO_AGUA, m3)
    esgoto = D(DIAS_DO_MES) * PORTO_DISPONIBILIDADE_ESGOTO + _por_faixas(PORTO_ESGOTO, m3)
    trh = PORTO_TRH_AGUA * D(m3)
    return (agua + esgoto + trh) * PORTO_IVA


@pytest.fixture(scope="module")
def tarifarios():
    dados = T.carregar()
    if "Porto" not in dados or "Funchal" not in dados:
        pytest.skip("tarifários do Porto e do Funchal ausentes")
    return dados


def test_porto_transcreve_os_escaloes_e_as_tarifas_do_pdf(tarifarios):
    p = tarifarios["Porto"]
    assert [tuple(e) for e in p["agua"]["escaloes"]] == [(a, b, float(c)) for a, b, c in PORTO_AGUA]
    assert [tuple(e) for e in p["saneamento"]["escaloes"]] == [(a, b, float(c)) for a, b, c in PORTO_ESGOTO]
    assert D(str(p["agua"]["fixa_mes"])) == PORTO_DISPONIBILIDADE_AGUA_ATE_20MM * DIAS_DO_MES == D("3.726")
    assert D(str(p["saneamento"]["fixa_mes"])) == PORTO_DISPONIBILIDADE_ESGOTO * DIAS_DO_MES == D("1.995")
    assert [pa["por_m3"] for pa in p["parcelas"]] == [0.0392]
    assert p["agua"]["iva_pct"] == p["saneamento"]["iva_pct"] == 6.0


def test_porto_nao_usa_a_tarifa_de_disponibilidade_da_pagina_3_que_e_dos_nao_domesticos(tarifarios):
    """O PDF imprime 0,1242 €/dia (≤ 20 mm) sob «Utilizadores domésticos» e 0,1367 €/dia na tabela seguinte,
    que vem depois da tarifa variável dos não domésticos: aquela é a doméstica."""
    assert tarifarios["Porto"]["agua"]["fixa_mes"] != pytest.approx(0.1367 * DIAS_DO_MES)


@pytest.mark.parametrize("m3", [0, 3, 5, 10, 15, 20, 25, 30, 42])
def test_porto_a_fatura_do_programa_e_a_conta_refeita_a_mao(tarifarios, m3):
    from triton.core.fatura_portuguesa import conta_mensal
    esperado = float(_conta_do_porto(m3))
    assert conta_mensal(T.fatura("Porto"), m3) == pytest.approx(esperado, abs=1e-9)


def test_porto_as_contas_de_conferencia_do_json_batem_com_a_conta_a_mao(tarifarios):
    for c in tarifarios["Porto"]["conferencia"]:
        assert c["conta"] == pytest.approx(float(_conta_do_porto(c["m3"])), abs=5e-5)


# --- Funchal -----------------------------------------------------------------------------

FUNCHAL_AGUA = [(0, 5, "0.39"), (5, 15, "0.69"), (15, 25, "1.28"), (25, 50, "2.87"), (50, None, "5.02")]
FUNCHAL_DISPONIBILIDADE_ATE_15MM = D("4.12")        # art. 57.º, por mês
FUNCHAL_ESGOTO_FIXO = D("1.97")                     # art. 10.º, valor fixo mensal
FUNCHAL_ESGOTO = [(0, 5, "0"), (5, 15, "0.33"), (15, None, "0.41")]     # escalão 1 sem valor impresso
FUNCHAL_RESIDUOS_FIXO = D("2.19")                   # art. 6.º, valor fixo mensal
FUNCHAL_RESIDUOS = [(0, 5, "0"), (5, 15, "0.22"), (15, None, "0.60")]   # escalão 1 sem valor impresso


def _conta_do_funchal(m3, iva):
    sem_iva = (FUNCHAL_DISPONIBILIDADE_ATE_15MM + _por_faixas(FUNCHAL_AGUA, m3)
               + FUNCHAL_ESGOTO_FIXO + _por_faixas(FUNCHAL_ESGOTO, m3)
               + FUNCHAL_RESIDUOS_FIXO + _por_faixas(FUNCHAL_RESIDUOS, m3))
    return sem_iva * (1 + D(str(iva)) / 100)


def test_funchal_transcreve_os_artigos_56_57_10_e_6(tarifarios):
    f = tarifarios["Funchal"]
    assert [tuple(e) for e in f["agua"]["escaloes"]] == [(a, b, float(c)) for a, b, c in FUNCHAL_AGUA]
    assert f["agua"]["fixa_mes"] == float(FUNCHAL_DISPONIBILIDADE_ATE_15MM)
    assert f["saneamento"]["fixa_mes"] == float(FUNCHAL_ESGOTO_FIXO)
    assert [pa["fixa"] for pa in f["parcelas"]] == [float(FUNCHAL_RESIDUOS_FIXO)]


def test_funchal_a_parte_variavel_do_saneamento_inclui_a_dos_residuos(tarifarios):
    """Sem campo para resíduos por escalões, a parte variável deles foi somada à do saneamento (mesmos cortes e mesmo IVA)."""
    f = tarifarios["Funchal"]
    somado = [(a, b, float(D(s) + D(r))) for (a, b, s), (_, _, r) in zip(FUNCHAL_ESGOTO, FUNCHAL_RESIDUOS)]
    assert [tuple(e) for e in f["saneamento"]["escaloes"]] == somado
    assert f["saneamento"]["iva_pct"] == f["parcelas"][0]["iva_pct"] == f["agua"]["iva_pct"]


@pytest.mark.parametrize("m3", [0, 3, 5, 6, 10, 15, 16, 25, 30, 50, 60])
def test_funchal_a_fatura_do_programa_e_a_conta_refeita_a_mao(tarifarios, m3):
    from triton.core.fatura_portuguesa import conta_mensal
    iva = tarifarios["Funchal"]["agua"]["iva_pct"]
    assert conta_mensal(T.fatura("Funchal"), m3) == pytest.approx(float(_conta_do_funchal(m3, iva)), abs=1e-9)


def test_funchal_as_contas_de_conferencia_do_json_batem_com_a_conta_a_mao(tarifarios):
    iva = tarifarios["Funchal"]["agua"]["iva_pct"]
    for c in tarifarios["Funchal"]["conferencia"]:
        assert c["conta"] == pytest.approx(float(_conta_do_funchal(c["m3"], iva)), abs=5e-5)


def test_funchal_o_iva_esta_declarado_como_a_confirmar(tarifarios):
    """A taxa de IVA da Madeira não foi verificada em fonte oficial: o JSON diz isso, não a afirma."""
    notas = " ".join(tarifarios["Funchal"]["notas"])
    assert "IVA" in notas and "confirmar" in notas
