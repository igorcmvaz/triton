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

from netuno.core.economic import calculate_water_bill
from netuno.core.tariff_regimes import (
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
from netuno.core.tariffs_database import load_tariffs_db

CIDADES = load_tariffs_db()["cities"]


def conta(faixas, m3: float) -> float:
    """Conta só de água, sem esgoto nem tributos."""
    return calculate_water_bill(m3 * 1000.0, faixas, sewage_mode=1, sewage_rate=0.0)


# ═══════════════════════ os quatro regimes, um a um ═══════════════════════════

FRANQUIA = [[0.0, 0.0, 40.0, -1], [0.0, 10.0, 0.0, 1], [10.0, 999999.0, 5.0, 1]]
DISPON = [[0.0, 0.0, 40.0, -1], [0.0, 999999.0, 5.0, 1]]
PISO = [[0.0, 0.0, 40.0, -3], [0.0, 999999.0, 5.0, 1]]
LIVRE = [[0.0, 999999.0, 5.0, 1]]


def test_franquia_no_minimo_nao_da_economia_abaixo_do_minimo():
    """É o caso que o professor teme, e o mais comum no Brasil.

    Pagam-se R$ 40 que já dão direito a 10 m³. Consumir 3 ou 10 custa o mesmo,
    de modo que economizar dentro da franquia não reduz a conta em nada.
    """
    assert conta(FRANQUIA, 0) == pytest.approx(40.0)
    assert conta(FRANQUIA, 3) == pytest.approx(40.0)
    assert conta(FRANQUIA, 10) == pytest.approx(40.0)
    # Economizar 6 m³ partindo de 9 m³ não economiza nada.
    assert conta(FRANQUIA, 9) - conta(FRANQUIA, 3) == pytest.approx(0.0)
    # Partindo de 20 m³, economiza-se só o que exceder a franquia.
    assert conta(FRANQUIA, 20) - conta(FRANQUIA, 14) == pytest.approx(30.0)


def test_disponibilidade_converte_toda_economia_em_desconto():
    """Instituto distinto do consumo mínimo: a taxa soma POR CIMA do medido."""
    assert conta(DISPON, 0) == pytest.approx(40.0)
    assert conta(DISPON, 3) == pytest.approx(55.0)
    assert conta(DISPON, 9) - conta(DISPON, 3) == pytest.approx(30.0)


def test_a_diferenca_entre_franquia_e_disponibilidade_e_a_economia_do_primeiro_bloco():
    """As duas têm a MESMA forma e diferem só pela tarifa da primeira faixa.

    Um erro de digitação numa casa decimal troca um regime pelo outro em
    silêncio, e a diferença é a economia inteira do primeiro bloco.
    """
    economia_franquia = conta(FRANQUIA, 10) - conta(FRANQUIA, 0)
    economia_dispon = conta(DISPON, 10) - conta(DISPON, 0)
    assert economia_franquia == pytest.approx(0.0)
    assert economia_dispon == pytest.approx(50.0)


def test_piso_de_pagamento_limita_por_baixo_sem_somar_por_cima():
    """Era o regime que faltava ao motor.

    O custo fixo SOMA; o piso LIMITA. Com piso de R$ 40, consumir 8 m³ custa
    R$ 40 e não R$ 80.
    """
    assert conta(PISO, 0) == pytest.approx(40.0)
    assert conta(PISO, 8) == pytest.approx(40.0)     # tarifado R$ 40, piso alcançado
    assert conta(PISO, 10) == pytest.approx(50.0)
    assert conta(PISO, 20) == pytest.approx(100.0)
    # E é diferente de taxa fixa no mesmo valor.
    assert conta(PISO, 20) < conta(DISPON, 20)


def test_o_piso_zera_a_economia_ate_alcanca_lo():
    assert conta(PISO, 8) - conta(PISO, 4) == pytest.approx(0.0)
    assert conta(PISO, 20) - conta(PISO, 14) == pytest.approx(30.0)


def test_sem_minimo_toda_economia_vira_desconto():
    assert conta(LIVRE, 0) == pytest.approx(0.0)
    assert conta(LIVRE, 9) - conta(LIVRE, 3) == pytest.approx(30.0)


# ═══════════════════════ leitura e classificação ══════════════════════════════

@pytest.mark.parametrize(
    ("faixas", "esperado"),
    [
        (FRANQUIA, FRANQUIA_NO_MINIMO),
        (DISPON, DISPONIBILIDADE),
        (PISO, PISO_DE_PAGAMENTO),
        (LIVRE, SEM_MINIMO),
        ([[0.0, 6.0, 14.3, -2], [6.0, 999999.0, 3.49, 1]], FRANQUIA_RETROATIVA),
    ],
)
def test_o_regime_e_lido_da_forma_da_tabela(faixas, esperado):
    assert ler_estrutura(faixas).regime == esperado


def test_a_franquia_lida_e_o_volume_de_tarifa_nula():
    est = ler_estrutura(FRANQUIA)
    assert est.consumo_minimo_m3 == pytest.approx(10.0)
    assert est.custo_fixo_mensal == pytest.approx(40.0)


def test_o_resumo_diz_ao_projetista_o_que_ele_precisa_saber():
    """Não o nome do regime: se economizar reduz a conta, e a partir de quanto."""
    franquia = resumo_do_regime({"faixas": FRANQUIA})
    assert "10 m³" in franquia and "não cai" in franquia
    assert "vira desconto" in resumo_do_regime({"faixas": DISPON})
    assert "piso" in resumo_do_regime({"faixas": PISO}).lower()


# ═══════════════════════════ o validador ══════════════════════════════════════

def test_a_tabela_truncada_e_erro():
    """Acima do teto a conta não cresce, e o programa não vê economia nenhuma."""
    truncada = [[0.0, 0.0, 30.0, -1], [0.0, 6.0, 0.0, 1]]
    codigos = {a.codigo for a in validar_estrutura({"faixas": truncada})}
    assert "tabela_truncada" in codigos
    assert conta(truncada, 30) == conta(truncada, 6)   # o sintoma


def test_o_minimo_diluido_em_tarifa_e_erro():
    """R$ 52,89 gravado como 5,289 R$/m³ até 10 m³ faz a franquia virar faixa cobrada."""
    diluido = {"tarifa_fixa_mensal": 52.89, "faixas": [[0.0, 10.0, 5.289, 1], [10.0, 999999.0, 9.8, 1]]}
    codigos = {a.codigo for a in validar_estrutura(diluido)}
    assert "minimo_diluido_em_tarifa" in codigos


def test_o_minimo_declarado_e_nao_cobrado_e_erro():
    reg = {"tarifa_fixa_mensal": 50.0, "faixas": [[0.0, 999999.0, 5.0, 1]]}
    codigos = {a.codigo for a in validar_estrutura(reg)}
    assert "minimo_declarado_e_nao_cobrado" in codigos


def test_a_lacuna_entre_faixas_e_erro():
    reg = {"faixas": [[0.0, 10.0, 3.0, 1], [15.0, 999999.0, 5.0, 1]]}
    assert "lacuna_entre_faixas" in {a.codigo for a in validar_estrutura(reg)}


def test_a_tarifa_nao_progressiva_e_aviso_e_nao_erro():
    """Existe em tarifa social, então merece conferência e não rejeição."""
    reg = {"faixas": [[0.0, 5.0, 8.0, 1], [5.0, 999999.0, 3.0, 1]]}
    achados = [a for a in validar_estrutura(reg) if a.codigo == "nao_progressiva"]
    assert achados and achados[0].gravidade == "aviso"


def test_uma_estrutura_correta_nao_gera_erro():
    assert validar_estrutura({"tarifa_fixa_mensal": 40.0, "faixas": FRANQUIA}) == []


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


def test_toda_conta_cresce_com_o_consumo():
    """Conta que não cresce é cadastro quebrado, e o efeito é grave.

    Se a conta não sobe com o consumo, economizar água não a reduz, e o
    aproveitamento pluvial aparece sem retorno nenhum por defeito de dado.
    """
    quebrados = []
    for c in CIDADES.values():
        if c.get("estrutura_incompleta"):
            continue   # já sinalizados, e o usuário é avisado na interface
        faixas = c.get("faixas") or []
        if not faixas:
            continue
        anterior = -1.0
        for m3 in (0, 5, 10, 15, 20, 30, 50, 80):
            atual = conta(faixas, m3)
            if atual < anterior - 1e-6:
                quebrados.append(f"{c.get('uf')}/{c.get('municipio')} caiu em {m3} m³")
                break
            anterior = atual
    assert not quebrados, quebrados[:5]


def test_economizar_nunca_aumenta_a_conta():
    """Invariante mais forte: a economia creditada nunca é negativa."""
    negativas = []
    for c in CIDADES.values():
        faixas = c.get("faixas") or []
        if not faixas:
            continue
        for base in (12, 20, 30):
            economia = conta(faixas, base) - conta(faixas, base - 6)
            if economia < -1e-6:
                negativas.append(f"{c.get('uf')}/{c.get('municipio')} em {base} m³: {economia:.2f}")
    assert not negativas, negativas[:5]


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


def test_o_minimo_usual_brasileiro_e_referencia_e_nao_regra():
    """A conta mínima é o produto da tarifa mínima pelo consumo mínimo.

    O regulamento fala em no mínimo 10 m³ mensais por economia residencial, mas
    a base tem municípios com 6 e com 15: é referência de conferência, não valor
    a impor.
    """
    minimos = {
        float(c.get("consumo_minimo_faturado_m3", 0.0))
        for c in CIDADES.values()
        if c.get("regime_tarifario") == FRANQUIA_NO_MINIMO
    }
    assert CONSUMO_MINIMO_USUAL_M3 in minimos
    assert len(minimos) > 1, "todos os mínimos iguais indicaria valor imposto, não coletado"


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
