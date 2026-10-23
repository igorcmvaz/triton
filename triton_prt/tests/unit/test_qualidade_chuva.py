# -*- coding: utf-8 -*-
"""Nível de qualidade da chuva (A, B, C): a fórmula única, em qualquer edição (sem o banco).

Os testes que leem o banco de Portugal estão em ``test_qualidade_chuva_prt.py`` (só a PRT).
"""
import itertools
import json
import os
import re

import pytest

from triton.core import qualidade_chuva as Q

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_os_limiares_sao_a_convencao_do_debate():
    assert Q.LIMIARES == {"A": {"dtot": 10.0, "drx": 15.0}, "B": {"dtot": 20.0, "drx": 25.0}}
    assert Q.NIVEIS == ("A", "B", "C") and Q.N_MINIMO_DE_CELULAS == 3


@pytest.mark.parametrize("dtot,drx,esperado", [
    (0, 0, "A"), (10, 15, "A"), (-10, -15, "A"), (10.01, 0, "B"), (0, 15.01, "B"), (-15.2, -15.5, "B"),
    (20, 25, "B"), (-20, 25, "B"), (20.01, 0, "C"), (0, 25.01, "C"), (-26.2, -37.6, "C"),
])
def test_concordancia_pelos_limiares(dtot, drx, esperado):
    assert Q.nivel_de_concordancia(dtot, drx) == esperado


@pytest.mark.parametrize("n,metodo,repetida,esperado", [
    (3, "dentro", False, "A"), (10, "dentro", False, "A"), (2, "dentro", False, "B"), (1, "dentro", False, "B"),
    (5, "centroide", False, "B"), (5, "dentro", True, "B"),
])
def test_geometria_so_rebaixa_ate_b(n, metodo, repetida, esperado):
    assert Q.nivel_de_geometria(n, metodo, repetida) == esperado


def test_a_geometria_nunca_produz_c():
    for n, metodo, rep in itertools.product(range(0, 8), ("dentro", "centroide"), (False, True)):
        assert Q.nivel_de_geometria(n, metodo, rep) in ("A", "B")


def test_nivel_e_o_pior_das_duas():
    assert Q.nivel(5, 5, 4, "dentro", False) == "A"
    assert Q.nivel(5, 5, 1, "dentro", False) == "B"          # concordância A, geometria B
    assert Q.nivel(15, 20, 4, "dentro", False) == "B"        # concordância B, geometria A
    assert Q.nivel(30, 5, 4, "dentro", False) == "C"         # a geometria não conserta a discrepância
    assert Q.nivel(30, 5, 1, "centroide", True) == "C"       # nem a pior geometria passa de B por si


def test_o_nivel_esta_sempre_em_a_b_c():
    valores = (-60, -26.2, -20, -10.01, -10, 0, 10, 15.2, 20, 25, 80)
    for dtot, drx, n, metodo, rep in itertools.product(valores, valores, (1, 2, 3, 6), ("dentro", "centroide"), (False, True)):
        assert Q.nivel(dtot, drx, n, metodo, rep) in Q.NIVEIS


def test_piorar_a_diferenca_nunca_melhora_o_nivel():
    ordem = {n: i for i, n in enumerate(Q.NIVEIS)}
    passos = [0, 4, 9.99, 10, 10.01, 14, 15, 15.01, 19.99, 20, 22, 25, 25.01, 40]
    for n, metodo, rep in itertools.product((1, 3), ("dentro", "centroide"), (False, True)):
        for dtot in passos:
            anterior = None
            for drx in passos:
                atual = ordem[Q.nivel(dtot, drx, n, metodo, rep)]
                assert anterior is None or atual >= anterior
                anterior = atual
        for drx in passos:
            anterior = None
            for dtot in passos:
                atual = ordem[Q.nivel(dtot, drx, n, metodo, rep)]
                assert anterior is None or atual >= anterior
                anterior = atual


def test_o_sinal_da_diferenca_nao_conta():
    assert Q.nivel(-9, 14, 3, "dentro") == Q.nivel(9, -14, 3, "dentro") == "A"


def test_o_motivo_diz_o_nivel_e_a_razao():
    assert Q.motivo(-3, -4, 5, "dentro").startswith("A:")
    m = Q.motivo(-5, -6, 1, "dentro")
    assert m.startswith("B:") and "uma só célula de 10 km" in m and "cabe no nível A" in m
    assert "centroide" in Q.motivo(-5, -6, 4, "centroide")
    assert "igual à de outro concelho" in Q.motivo(-5, -6, 4, "dentro", True)
    m = Q.motivo(-26.2, -37.6, 1, "dentro")
    assert m.startswith("C:") and "20 %" in m and "25 %" in m and "-26,2 %" in m
    assert Q.motivo(-15.2, -15.5, 3, "dentro").startswith("B:")


def test_o_motivo_usa_os_limiares_do_dicionario(monkeypatch):
    monkeypatch.setitem(Q.LIMIARES, "A", {"dtot": 7.0, "drx": 9.0})
    assert "7 %" in Q.motivo(-8, -2, 5, "dentro") and "9 %" in Q.motivo(-8, -2, 5, "dentro")
    assert Q.nivel(-8, -2, 5, "dentro") == "B"


def test_a_descricao_dos_niveis_e_gerada_dos_limiares(monkeypatch):
    texto = " ".join(Q.descricao_dos_niveis("pt"))
    for lim in (10, 15, 20, 25):
        assert f"{lim} %" in texto
    monkeypatch.setitem(Q.LIMIARES, "B", {"dtot": 22.0, "drx": 27.0})
    novo = " ".join(Q.descricao_dos_niveis("pt"))
    assert "22 %" in novo and "27 %" in novo and "20 %" not in novo
    assert "Iberia01" in " ".join(Q.descricao_dos_niveis("en"))


def test_os_textos_dizem_diferenca_para_o_iberia01_e_nao_vies():
    todos = " ".join(Q.descricao_dos_niveis("pt") + Q.descricao_dos_niveis("en")
                     + [Q.motivo(-26, -37, 1, "centroide", True), Q.motivo(-3, -4, 5, "dentro")])
    assert "viés" not in todos.lower() and "bias" not in todos.lower()
    assert "diferença para o Iberia01" in Q.descricao_dos_niveis("pt")[0]


def test_nenhum_outro_arquivo_do_nucleo_repete_os_limiares():
    """Os limiares moram em qualidade_chuva.py: nenhum outro módulo do pacote os redefine."""
    padrao = re.compile(r"LIMIARES\s*=\s*\{|\"drx\"\s*:\s*(15|25)\b")
    donos = []
    for raiz, _, nomes in os.walk(os.path.join(RAIZ, "triton")):
        for nome in nomes:
            if nome.endswith(".py") and "__pycache__" not in raiz:
                caminho = os.path.join(raiz, nome)
                if padrao.search(open(caminho, encoding="utf-8").read()):
                    donos.append(os.path.relpath(caminho, RAIZ).replace("\\", "/"))
    assert donos == ["triton/core/qualidade_chuva.py"], donos


def test_limiares_em_texto_e_json_dos_limiares():
    assert json.loads(Q.limiares_em_texto()) == Q.LIMIARES


def test_a_chuva_fora_da_edicao_com_o_banco_nao_tem_dado_de_portugal():
    """Em INT e BRL não há dado de Portugal: nem o banco, nem a tabela, nem a linha de cobertura inventada."""
    from triton.core import base_climatica_portugal as pt
    from triton.core.edition import get_current_edition
    if get_current_edition() == "PRT":
        pytest.skip("a PRT traz o banco")
    assert pt.caminho_da_base() is None and not pt.disponivel()
    assert not os.path.exists(os.path.join(RAIZ, "data", "portugal_eobs.db"))
    assert not Q.tem_qualidade() and Q.qualidade_do_concelho("Lisboa") is None and Q.contagem_por_nivel() == {}
    assert "Cobertura: sem a tabela" in Q.linha_de_cobertura()


def test_projeto_fora_da_e_obs_nao_grava_pacote_de_chuva(tmp_path):
    """A BRL (e qualquer chuva que não seja a E-OBS) grava o arquivo de sempre: sem o bloco do pacote."""
    import numpy as np
    from triton.core.parser import TritonConfig, export_triton_json
    cfg = TritonConfig()
    destino = tmp_path / "p.triton"
    export_triton_json(cfg, str(destino), precip_data=np.arange(30, dtype=float))
    chuva = json.loads(destino.read_text(encoding="utf-8"))["rainfall"]
    assert "pacote_chuva" not in chuva and len(chuva["precipitation_mm"]) == 30
