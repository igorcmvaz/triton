"""O botão que responde, na tela, se a série de chuva basta para o projeto."""
import os
import sys

import numpy as np
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QTableWidget  # noqa: E402

from netuno.core.comprimento_de_serie import DIAS_NO_ANO, analisar  # noqa: E402
from netuno.ui.dialogs.dialog_comprimento_de_serie import DialogComprimentoDeSerie  # noqa: E402
from netuno.ui.tab_tanks_simulation import TabTanksSimulation  # noqa: E402

PROJETO = dict(area=100.0, runoff_coeff=0.80, discard_mm=2.0, discard_mode=1,
               total_demand_per_day=600.0, rainwater_share=0.30)


@pytest.fixture(scope="session")
def app():
    return QApplication.instance() or QApplication(sys.argv)


@pytest.fixture
def resultado():
    return analisar(np.full(5 * DIAS_NO_ANO, 6.0), PROJETO,
                    volume_maximo_l=5000.0, passo_l=1000.0)


def test_a_janela_mostra_o_veredito_e_uma_linha_por_comprimento(app, resultado):
    dialogo = DialogComprimentoDeSerie(resultado)
    tabela = dialogo.findChild(QTableWidget)
    assert tabela is not None
    assert tabela.rowCount() == len(resultado.frequencia_por_comprimento)
    assert resultado.resumo() in dialogo.texto_para_relatorio()
    dialogo.deleteLater()


def test_a_aba_avisa_quando_a_serie_e_curta_demais(app, monkeypatch):
    aba = TabTanksSimulation()
    aba.precip_data = np.full(200, 5.0)      # menos de dois anos
    avisos = []
    monkeypatch.setattr("netuno.ui.tab_tanks_simulation.QMessageBox.warning",
                        lambda *args, **kwargs: avisos.append(args[1:3]))
    aba.on_analisar_comprimento_da_serie()
    assert avisos, "a aba tinha de avisar que a série não dá para analisar"
    aba.deleteLater()


def test_a_aba_abre_a_janela_com_o_resultado(app, monkeypatch):
    aba = TabTanksSimulation()
    aba.precip_data = np.random.default_rng(4).gamma(0.6, 8.0, 6 * DIAS_NO_ANO)
    aba.txt_sweep_max.setText("6000")
    aba.txt_sweep_step.setText("1000")
    aba.txt_delta_ideal.setText("1,0")
    abertas = []
    monkeypatch.setattr(
        "netuno.ui.dialogs.dialog_comprimento_de_serie.DialogComprimentoDeSerie.exec",
        lambda self: abertas.append(self.resultado) or 0)
    aba.on_analisar_comprimento_da_serie()
    assert len(abertas) == 1
    assert abertas[0].anos_da_serie == 6
    assert abertas[0].limiar_ganho_pct_m3 == pytest.approx(1.0)
    # O cursor de espera não pode ficar preso depois da análise.
    assert QApplication.overrideCursor() is None
    aba.deleteLater()
