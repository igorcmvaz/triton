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
