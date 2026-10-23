# -*- coding: utf-8 -*-
"""Interface da edição IBE/PRT: nível de qualidade da chuva, linha de cobertura e aviso de licença.

Só vale na PRT (``tests/so_da_prt.txt``) e precisa de Qt.
"""
import re
import sys

import numpy as np
import pytest

pytest.importorskip("PySide6")
from PySide6.QtWidgets import QApplication, QMessageBox  # noqa: E402

from triton.core import base_climatica_portugal as pt  # noqa: E402
from triton.core import licenca_eobs as L  # noqa: E402
from triton.core import qualidade_chuva as Q  # noqa: E402

pytestmark = pytest.mark.skipif(not pt.disponivel(), reason="data/portugal_eobs.db ausente")


class Armazem:
    def __init__(self):
        self.dados = {}

    def value(self, chave, padrao=""):
        return self.dados.get(chave, padrao)

    def setValue(self, chave, valor):
        self.dados[chave] = valor

    def sync(self):
        pass


def _sem_caixas(monkeypatch):
    for nome in ("information", "warning", "critical"):
        monkeypatch.setattr(QMessageBox, nome, staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok))


@pytest.fixture
def janela(monkeypatch):
    _sem_caixas(monkeypatch)
    app = QApplication.instance() or QApplication(sys.argv)
    from triton.ui.main_window import MainWindow
    w = MainWindow()
    yield w
    w.close()
    app.processEvents()


def test_a_tela_inicial_e_o_titulo_trazem_a_linha_de_cobertura_do_banco(janela):
    linha = Q.linha_de_cobertura()
    assert janela.lbl_cobertura.text() == linha
    assert linha.endswith("Espanha: 0 locais") and "A 45, B 159, C 74" in linha
    assert linha in janela.windowTitle()


def test_a_aba_do_projeto_mostra_nivel_e_motivo_do_concelho(janela):
    tp = janela.tab_project
    assert tp._base_portugal
    for distrito, concelho in (("Lisboa", "Lisboa"), ("Faro", "Albufeira"), ("Aveiro", "Águeda")):
        tp.combo_climate_uf.setCurrentIndex(tp.combo_climate_uf.findData(distrito))
        tp.combo_climate_city.setCurrentIndex(tp.combo_climate_city.findData(concelho))
        QApplication.processEvents()
        q = Q.qualidade_do_concelho(concelho)
        assert tp.lbl_qualidade_chuva.isVisibleTo(tp)
        texto = tp.lbl_qualidade_chuva.text()
        assert f"nível {q['nivel']}" in texto and concelho in texto
        assert q["motivo"].split(": ", 1)[1][:30] in texto
        assert "10 %" in tp.lbl_qualidade_chuva.toolTip() and "Iberia01" in tp.lbl_qualidade_chuva.toolTip()
        assert "viés" not in texto.lower()


def test_o_texto_da_interface_esta_em_portugues_europeu(janela):
    tp = janela.tab_project
    tp.combo_climate_city.setCurrentIndex(tp.combo_climate_city.findData("Lisboa"))
    QApplication.processEvents()
    texto = tp.lbl_qualidade_chuva.text() + tp.lbl_qualidade_chuva.toolTip() + janela.lbl_cobertura.text()
    assert not re.search(r"\b(usuário|arquivo|tela|esgoto)\b", texto)


def test_a_caixa_do_aviso_tem_as_duas_respostas(janela):
    from triton.ui.dialogs.dialog_licenca_eobs import montar_aviso
    caixa, b_pesquisa, b_comercial = montar_aviso(janela)
    assert caixa.text().startswith("Os dados de chuva desta edição vêm da E-OBS, de uso estritamente não comercial")
    assert b_pesquisa.text() == "Uso de pesquisa ou educação" and b_comercial.text() == "Uso comercial"
    assert len(caixa.buttons()) == 2


@pytest.mark.parametrize("resposta", ["pesquisa", "comercial"])
def test_o_aviso_pergunta_uma_vez_e_lembra_a_escolha(janela, monkeypatch, resposta):
    from triton.ui.dialogs import dialog_licenca_eobs as D
    arm = Armazem()
    chamadas = []

    def exec_falso(self):
        chamadas.append(1)
        self._clicado = {b.text(): b for b in self.buttons()}[L.RESPOSTAS[resposta]]
        return 0
    monkeypatch.setattr(QMessageBox, "exec", exec_falso)
    monkeypatch.setattr(QMessageBox, "clickedButton", lambda self: self._clicado)
    assert D.perguntar_uso_se_necessario(janela, arm) == resposta
    assert arm.dados["licenca_eobs/uso"] == resposta
    assert D.perguntar_uso_se_necessario(janela, arm) is None         # segunda vez: não pergunta
    assert len(chamadas) == 1


def test_fechar_o_aviso_sem_escolher_nao_grava_nada(janela, monkeypatch):
    from triton.ui.dialogs import dialog_licenca_eobs as D
    arm = Armazem()
    monkeypatch.setattr(QMessageBox, "exec", lambda self: 0)
    monkeypatch.setattr(QMessageBox, "clickedButton", lambda self: None)
    assert D.perguntar_uso_se_necessario(janela, arm) is None
    assert arm.dados == {}


def test_com_o_bloqueio_ligado_a_aba_do_projeto_oculta_a_base_e_pede_serie_propria(monkeypatch):
    """O caminho bloqueado na interface: sem a base E-OBS, a Etapa 1 oferece só o arquivo próprio."""
    monkeypatch.setattr(L, "BLOQUEAR_E_OBS_EM_USO_COMERCIAL", True)
    arm = Armazem()
    arm.dados["licenca_eobs/uso"] = "comercial"
    monkeypatch.setattr(L, "_armazem", lambda: arm)
    _sem_caixas(monkeypatch)
    app = QApplication.instance() or QApplication(sys.argv)
    from triton.ui.main_window import MainWindow
    w = MainWindow()
    try:
        tp = w.tab_project
        assert not tp._base_portugal and not tp.rb_source_national.isVisibleTo(tp)
        assert tp.rb_source_custom.isChecked()
        assert w.lbl_cobertura is None
    finally:
        w.close()
        app.processEvents()


def test_projeto_aberto_pela_interface_com_pacote_antigo_mantem_a_serie_incorporada(janela, monkeypatch, tmp_path):
    """Reabrir um projeto cuja série é de outro pacote: a série do estudo não é trocada em silêncio."""
    from triton.core import parser as P
    cfg = P.TritonConfig()
    cfg.climate_source_mode, cfg.climate_city_uf, cfg.climate_city_name = "national_db", "Faro", "Faro"
    cfg.climate_model, cfg.climate_scenario = pt.MODELO_EOBS, pt.CENARIO_EOBS
    cfg.climate_start_date, cfg.climate_end_date, cfg.start_date = "01/01/2001", "31/12/2005", "01/01/2001"
    serie = P.serie_da_climbra(cfg)
    destino = tmp_path / "f.triton"
    P.export_triton_json(cfg, str(destino), precip_data=serie)
    mensagens = []
    monkeypatch.setattr(QMessageBox, "warning",
                        staticmethod(lambda *a, **k: mensagens.append(a[2]) or QMessageBox.StandardButton.Ok))
    antigo = dict(pt.pacote())
    monkeypatch.setattr(P, "_pacote_atual_da_eobs",
                        lambda: {**antigo, "pacote_id": "PT-EOBS-v34.0-deadbeef", "sha256_pacote": "d" * 64})
    janela.on_load_simulation(str(destino))
    QApplication.processEvents()
    assert np.array_equal(np.asarray(janela.tab_project.precip_data, dtype=float), serie)
    assert any("PT-EOBS-v34.0-deadbeef" in m for m in mensagens)
    assert janela.config.chuva_procedencia["mudou"] is True
