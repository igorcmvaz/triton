"""O projeto novo da interface parte do arranjo 3D, e o arranjo mora na configuração."""

from netuno.core.study_layout import generate_study_layout


def test_a_janela_nova_parte_do_arranjo(qapp):
    from netuno.ui.main_window import MainWindow

    janela = MainWindow()
    assert janela.config.capex_do_arranjo is True
    assert janela.config.mao_de_obra_automatica is True
    janela.bim_layout = generate_study_layout({"lower_vol": 6000, "area": 120})
    assert janela.config.bim_layout is janela.bim_layout or janela.config.bim_layout == janela.bim_layout
    janela.close()
