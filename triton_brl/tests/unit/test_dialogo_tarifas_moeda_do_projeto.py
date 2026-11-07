"""Os diálogos de tarifas e custos usam a moeda do projeto mesmo quando o pai é a aba Projeto."""
from triton.ui.dialogs.dialog_economic import _simbolo_da_moeda


class _Janela:
    class tab_tanks_simulation:
        @staticmethod
        def get_currency_symbol():
            return "€"


class _AbaSemMoeda:
    def window(self):
        return _Janela()


def test_pai_sem_moeda_pergunta_a_aba_de_simulacao():
    assert _simbolo_da_moeda(_AbaSemMoeda()) == "€"


def test_sem_pai_vale_a_moeda_da_edicao_e_nunca_um_simbolo_vazio():
    from triton.core.edition import get_edition_currency_symbol
    assert _simbolo_da_moeda(None) == (get_edition_currency_symbol() or "¤")
