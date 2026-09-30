"""O atualizador automático não pode reintroduzir defeito de estrutura.

O motor de atualização raspa fontes das concessionárias e grava o banco das 652
cidades. Ele já gravou o que raspasse sem conferir a **estrutura**,
de modo que um mínimo diluído em tarifa unitária ou uma tabela truncada voltavam
a cada rodada.

Isso é pior que o defeito original, porque é automático e periódico: corrigir o
dado à mão não adianta se a próxima atualização o desfaz.

A porta de validação não derruba a rodada. Conserva o registro anterior do
município cuja estrutura nova tem erro e o manda para revisão manual, e segue com
os demais — uma página que mudou de layout não pode nem derrubar a base nem
entrar nela em silêncio.
"""

from __future__ import annotations

import pytest

from netuno.core.tariff_regimes import validar_estrutura

# Estruturas que a porta tem de barrar, cada uma um defeito real encontrado na
# auditoria dos 652 municípios.
TRUNCADA = {
    "municipio": "Teste",
    "tarifa_fixa_mensal": 30.0,
    "faixas": [[0.0, 0.0, 30.0, -1], [0.0, 6.0, 0.0, 1]],
}
MINIMO_DILUIDO = {
    "municipio": "Teste",
    "tarifa_fixa_mensal": 52.89,
    "faixas": [[0.0, 10.0, 5.289, 1], [10.0, 999999.0, 9.8, 1]],
}
COM_LACUNA = {
    "municipio": "Teste",
    "faixas": [[0.0, 10.0, 3.0, 1], [15.0, 999999.0, 5.0, 1]],
}
BOA = {
    "municipio": "Teste",
    "tarifa_fixa_mensal": 40.0,
    "faixas": [[0.0, 0.0, 40.0, -1], [0.0, 10.0, 0.0, 1], [10.0, 999999.0, 5.0, 1]],
}


@pytest.mark.parametrize(
    ("registro", "codigo"),
    [
        (TRUNCADA, "tabela_truncada"),
        (MINIMO_DILUIDO, "minimo_diluido_em_tarifa"),
        (COM_LACUNA, "lacuna_entre_faixas"),
    ],
)
def test_a_porta_reconhece_cada_defeito_da_auditoria(registro, codigo):
    erros = [a for a in validar_estrutura(registro) if a.gravidade == "erro"]
    assert codigo in {a.codigo for a in erros}


def test_a_porta_deixa_passar_estrutura_correta():
    assert [a for a in validar_estrutura(BOA) if a.gravidade == "erro"] == []


def test_o_motor_de_atualizacao_chama_a_porta():
    """A ligação em si, que é o que faltava.

    Um validador que ninguém chama não protege nada, e foi assim que o
    atualizador passou a existir sem conferir o que grava.
    """
    import inspect

    from netuno.core.tariff_updater import updater_engine

    fonte = inspect.getsource(updater_engine)
    assert "validar_estrutura" in fonte
    # E antes de gravar, não depois.
    assert fonte.index("validar_estrutura(updated_city)") < fonte.index("json.dump(db_data")


def test_a_rejeicao_conserva_o_registro_anterior_e_pede_revisao():
    """Uma raspagem quebrada não pode derrubar a base nem entrar nela calada."""
    import inspect

    from netuno.core.tariff_updater import updater_engine

    fonte = inspect.getsource(updater_engine)
    trecho = fonte[fonte.index("PORTA DE VALIDACAO"):fonte.index("# Atualiza no dicionário mestre")]
    assert "manual_reviews.append" in trecho
    assert "anterior" in trecho
    assert "structure_rejected" in trecho


def test_um_aviso_nao_barra_a_atualizacao():
    """Tarifa não progressiva existe em tarifa social, e não é motivo de rejeição."""
    social = {"municipio": "Teste", "faixas": [[0.0, 5.0, 8.0, 1], [5.0, 999999.0, 3.0, 1]]}
    achados = validar_estrutura(social)
    assert achados
    assert [a for a in achados if a.gravidade == "erro"] == []
