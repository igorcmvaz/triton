# -*- coding: utf-8 -*-
"""Pesos do TOPSIS: quatro pesos de eixo × partes no eixo, oito pesos diretos e o padrão do programa."""
import numpy as np
import pytest

from triton.core.topsis import (CRITERION_KEYS, PARTES_IGUAIS_NO_EIXO, PARTES_NO_EIXO_PADRAO, PESOS_PADRAO,
                                pesos_dos_criterios, validar_partes_no_eixo, _criterion_weights)


def test_padrao_balanceado_em_quatro_dimensoes():
    w = _criterion_weights(None)
    esperado = np.array([0.125, 0.125, 0.25 / 3.0, 0.25 / 3.0, 0.25 / 3.0, 0.25, 0.125, 0.125])
    assert w == pytest.approx(esperado)
    assert w.sum() == pytest.approx(1.0)
    assert _criterion_weights(PESOS_PADRAO) == pytest.approx(esperado)


def test_partes_iguais_distribuem_corretamente():
    w = _criterion_weights((0.25, 0.25, 0.25, 0.25), PARTES_IGUAIS_NO_EIXO)
    assert w == pytest.approx([1 / 8, 1 / 8, 1 / 12, 1 / 12, 1 / 12, 1 / 4, 1 / 8, 1 / 8])


def test_partes_so_importam_pela_proporcao_dentro_do_eixo():
    a = pesos_dos_criterios((0.4, 0.3, 0.2, 0.1), (1, 1, 1, 3, 0, 1, 1, 1))
    b = pesos_dos_criterios((0.4, 0.3, 0.2, 0.1), (10, 10, 10, 30, 0, 10, 10, 10))
    assert a == pytest.approx(b)
    assert a[2] == pytest.approx(0.3 * 0.25) and a[3] == pytest.approx(0.3 * 0.75)


def test_ligar_os_criterios_adicionais():
    w = _criterion_weights(PESOS_PADRAO, (1, 1, 1, 1, 1, 1, 1, 1))
    assert (w > 0).all()


def test_oito_pesos_diretos_valem_sem_repartir():
    w = _criterion_weights([1, 2, 3, 4, 5, 6, 7, 8], PARTES_IGUAIS_NO_EIXO)
    assert w == pytest.approx(np.arange(1, 9) / 36.0)


@pytest.mark.parametrize("partes", [
    (0, 0, 1, 1, 0, 1, 1, 1),
    (1, 1, 0, 0, 0, 1, 1, 1),
    (1, 1, 1, 1, 0, 0, 1, 1),
    (1, 1, 1, 1, 0, 1, 0, 0),
    (1, 2, 3),
    (1, -1, 1, 1, 0, 1, 1, 1),
])
def test_partes_invalidas(partes):
    with pytest.raises(ValueError):
        validar_partes_no_eixo(partes)


def test_a_ordem_das_partes_segue_os_criterios():
    assert len(PARTES_NO_EIXO_PADRAO) == len(CRITERION_KEYS) == 8


# ── linha de comando e arquivo de projeto ─────────────────────────────────────────────────────

def test_cli_le_as_partes_no_eixo():
    import argparse
    from triton import cli
    assert cli._parse_criterion_shares("1,1,1,1,1,1,1,1") == (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    for ruim in ("1,2,3", "0,0,1,1,0,1,1,1", "a,b,c,d,e,f,g,h"):
        with pytest.raises(argparse.ArgumentTypeError):
            cli._parse_criterion_shares(ruim)


def test_projeto_valida_pesos_e_partes():
    from triton import cli
    assert cli._validate_analysis_config({"topsis_weights": [1] * 8, "topsis_criterion_shares": [1] * 8}) == []
    assert cli._validate_analysis_config({"topsis_weights": [1] * 4, "topsis_criterion_shares": [1] * 8}) == []
    assert cli._validate_analysis_config({"topsis_criterion_shares": [0] * 8})
    assert cli._validate_analysis_config({"topsis_weights": [1, 2]})


def test_a_partes_da_interface_chegam_ao_projeto():
    from triton import cli
    estado = {"topsis": {"technical_weight": 25, "economic_weight": 25, "environmental_weight": 25, "structural_weight": 25, "criterion_shares": [100] * 8}}
    analise = cli._analysis_from_ui_state(estado)
    assert analise["topsis_criterion_shares"] == [100.0] * 8
    assert analise["topsis_weights"] == [25.0, 25.0, 25.0, 25.0]
    assert "topsis_criterion_shares" not in cli._analysis_from_ui_state({"topsis": {"technical_weight": 40}})


def test_template_do_projeto_traz_as_partes_padrao():
    from triton import cli
    assert cli._template_analysis()["topsis_criterion_shares"] == list(PARTES_NO_EIXO_PADRAO)
