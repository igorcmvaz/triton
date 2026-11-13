"""O laudo em português de Portugal acerta género e número ao trocar vocabulário (premissa → pressuposto etc.)."""
import pytest

from triton.ui.laudo_em_ingles import laudo_em_portugal


@pytest.mark.parametrize(
    "brasil, portugal",
    [
        ("<p>Nas premissas registradas</p>", "<p>Nos pressupostos registados</p>"),
        ("<p>As premissas executivas</p>", "<p>Os pressupostos executivos</p>"),
        ("<p>aos premissas financeiras</p>", "<p>aos pressupostos financeiros</p>"),
        ("<p>premissas físicas e operacionais</p>", "<p>pressupostos físicos e operacionais</p>"),
        ("<p>Premissas adotadas</p>", "<p>Pressupostos adotados</p>"),
        ("<p>a vazão da edificação</p>", "<p>o caudal do edifício</p>"),
        ("<p>o uso do reúso</p>", "<p>o uso da reutilização</p>"),
        ("<p>Uma premissa e das vazões</p>", "<p>Um pressuposto e dos caudais</p>"),
    ],
)
def test_concordancia_do_vocabulario_de_portugal(brasil, portugal):
    assert laudo_em_portugal(brasil) == portugal


def test_palavras_sem_mudanca_de_genero_ficam_como_estao():
    assert laudo_em_portugal("<p>a economia</p>") == "<p>a poupança</p>"


def test_escore_vira_pontuacao_com_concordancia():
    """Em Portugal, «pontuação» (feminino): o artigo, a preposição e o adjetivo concordam."""
    from triton.ui.portugues_de_portugal import para_portugal
    linha = ("TOPSIS: volumes de {0} a {1} L com escores semelhantes (até {2}% da amplitude, a partir do maior) "
             "| maior escore em {3} L ({4})")
    assert para_portugal(linha) == ("TOPSIS: volumes de {0} a {1} L com pontuações semelhantes (até {2}% da "
                                    "amplitude, a partir da maior) | maior pontuação em {3} L ({4})")
    assert para_portugal("sem outro volume a até 5% da amplitude do maior escore (0.68)") == \
        "sem outro volume a até 5% da amplitude da maior pontuação (0.68)"
    assert para_portugal("não substituem o escore TOPSIS ponderado.") == "não substituem a pontuação TOPSIS ponderada."
    assert para_portugal("que o escore normalizado, sozinho, não comunica") == \
        "que a pontuação normalizada, sozinha, não comunica"
    assert para_portugal("volumes cujo escore fica a até esta fração da amplitude dos escores, contada do maior") == \
        "volumes cuja pontuação fica a até esta fração da amplitude das pontuações, contada da maior"
    assert para_portugal("📊 Escore TOPSIS") == "📊 Pontuação TOPSIS"
    assert para_portugal("Maior escore TOPSIS") == "Maior pontuação TOPSIS"
