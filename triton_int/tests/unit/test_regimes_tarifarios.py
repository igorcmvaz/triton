"""Robustez dos regimes de tarifa mínima.

A mesma expressão «tarifa mínima» designa coisas diferentes no Brasil, e
confundi-las muda o resultado de um estudo de aproveitamento pluvial — porque o
que interessa não é a conta, é **quanto a conta cai quando se consome menos**.

Num município com franquia de 15 m³, uma residência que consome 12 m³ **não
economiza um centavo** por instalar cisterna: a conta é a mesma com 12 ou com
3 m³. Tratá-la como se houvesse desconto proporcional inventa uma economia que a
concessionária não concede, e o payback sai otimista.

O erro simétrico é igualmente grave: uma tabela de faixas truncada faz a conta
parar de crescer, e então o programa não vê economia nenhuma acima do teto
tabelado — o sistema aparece inviável por defeito de cadastro.

Estes testes fixam os dois lados, e varrem os 652 municípios da base.
"""

from __future__ import annotations

import pytest

from triton.core.economic import calculate_water_bill
from triton.core.tariff_regimes import (
    CONSUMO_MINIMO_USUAL_M3,
    DISPONIBILIDADE,
    FRANQUIA_NO_MINIMO,
    FRANQUIA_RETROATIVA,
    PISO_DE_PAGAMENTO,
    REGIMES,
    SEM_MINIMO,
    auditar_base,
    ler_estrutura,
    resumo_do_regime,
    validar_estrutura,
)
from triton.core.tariffs_database import load_tariffs_db

CIDADES = load_tariffs_db()["cities"]


def conta(faixas, m3: float) -> float:
    """Conta só de água, sem esgoto nem tributos."""
    return calculate_water_bill(m3 * 1000.0, faixas, sewage_mode=1, sewage_rate=0.0)


# ═══════════════════════ os quatro regimes, um a um ═══════════════════════════


# ═══════════════════════ leitura e classificação ══════════════════════════════


# ═══════════════════════════ o validador ══════════════════════════════════════


# ═════════════════════ a base inteira, 652 municípios ═════════════════════════

def test_todo_municipio_declara_o_regime():
    """Declarar não impede o erro, mas o torna detectável."""
    for chave, c in CIDADES.items():
        assert c.get("regime_tarifario") in REGIMES, f"{chave}: {c.get('regime_tarifario')!r}"


def test_o_regime_declarado_concorda_com_a_forma_da_tabela():
    """É a verificação que a declaração existe para permitir.

    Se alguém editar as faixas e esquecer o regime, ou vice-versa, os dois
    divergem e este teste cai.
    """
    divergentes = [
        f"{c.get('uf')}/{c.get('municipio')}: declara {c['regime_tarifario']}, "
        f"a tabela diz {ler_estrutura(c.get('faixas')).regime}"
        for c in CIDADES.values()
        if c.get("regime_tarifario") != ler_estrutura(c.get("faixas")).regime
    ]
    assert not divergentes, divergentes[:5]


def test_o_consumo_minimo_declarado_bate_com_a_franquia_da_tabela():
    for c in CIDADES.values():
        declarado = float(c.get("consumo_minimo_faturado_m3", 0.0))
        lido = ler_estrutura(c.get("faixas")).consumo_minimo_m3
        assert declarado == pytest.approx(lido, abs=0.01), c.get("municipio")


def test_a_base_nao_tem_erro_alem_dos_quatro_sinalizados():
    """Os quatro restantes têm só o bloco mínimo cadastrado.

    Não há o que reconstruir sem a tarifa de excedente, que não consta da fonte;
    ficam marcados e a interface avisa. Se aparecer um quinto, é regressão.
    """
    com_erro = {
        chave for chave, achados in auditar_base(CIDADES).items()
        if any(a.gravidade == "erro" for a in achados)
    }
    assert len(com_erro) <= 4, sorted(com_erro)
    for chave in com_erro:
        assert CIDADES[chave].get("estrutura_incompleta") is True, chave
        assert CIDADES[chave].get("_ressalva_estrutura"), chave


def test_os_municipios_sinalizados_tem_confianca_rebaixada():
    """Escolhíveis sim, mas nunca com a mesma confiança de um cadastro completo."""
    for c in CIDADES.values():
        if c.get("estrutura_incompleta") or c.get("estrutura_suspeita"):
            assert float(c.get("confianca_score", 100.0)) <= 55.0, c.get("municipio")


def test_toda_correcao_de_estrutura_esta_registrada():
    """Mudar tarifa sem dizer o que mudou não é auditável."""
    for c in CIDADES.values():
        corr = c.get("_correcao_estrutura")
        if corr:
            for campo in ("em", "o_que", "como", "efeito"):
                assert corr.get(campo), (c.get("municipio"), campo)


# ══════════════════ conferência contra a fonte oficial ════════════════════════

def test_florianopolis_bate_com_a_tabela_da_casan():
    """Tabela Tarifária CASAN 04/2026, categoria Residencial.

    TFDI de R$ 46,34/mês, 0 a 10 m³ a R$ 3,08/m³, 11 a 25 a R$ 14,31, 26 a 50 a
    R$ 19,14, acima de 50 a R$ 24,08, esgoto a 100% da água. É taxa de
    disponibilidade, e não consumo mínimo: na área da CASAN cada metro cúbico
    economizado gera desconto desde o primeiro.
    """
    c = next(v for v in CIDADES.values() if v.get("municipio") == "Florianópolis")
    assert c["regime_tarifario"] == DISPONIBILIDADE
    assert float(c["tarifa_fixa_mensal"]) == pytest.approx(46.34)
    assert float(c["esgoto_pct"]) == pytest.approx(100.0)

    esperado = {0.0: 3.08, 10.0: 14.31, 25.0: 19.14, 50.0: 24.08}
    tiers = {float(t[0]): float(t[2]) for t in ler_estrutura(c["faixas"]).faixas_progressivas}
    assert tiers == pytest.approx(esperado)

    # E a economia é proporcional desde o primeiro metro cúbico.
    assert conta(c["faixas"], 8) - conta(c["faixas"], 5) == pytest.approx(3 * 3.08)
