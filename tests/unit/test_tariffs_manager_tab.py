"""
Testes unitários para o Gestor de Tarifas e Suporte Multi-Categoria (Netuno 5).
"""

import sys
import unittest
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication(sys.argv)

from netuno.core.tariffs_database import (
    get_city_data,
    get_city_tariffs_by_category,
    CATEGORIAS_TARIFARIAS,
    categorias_coletadas,
)
from netuno.ui.tab_tariffs_manager import TabTariffsManager


class TestTariffsMultiCategoryAndTab(unittest.TestCase):

    def test_all_categories_present(self):
        """Verifica que as 5 categorias principais estão cadastradas."""
        cats = list(CATEGORIAS_TARIFARIAS.keys())
        self.assertIn("residencial", cats)
        self.assertIn("comercial", cats)
        self.assertIn("industrial", cats)
        self.assertIn("publica", cats)
        self.assertIn("social", cats)

    def test_categoria_sem_tabela_coletada_nao_e_estimada(self):
        """Até a 5.0.0 a comercial era a residencial vezes 1,85, sem fonte.

        Uma categoria sem tabela oficial no registro do município não devolve nada:
        o programa não inventa a tarifa de uma categoria a partir de outra.
        """
        res = get_city_tariffs_by_category("SC", "Florianópolis", category="residencial")
        self.assertIsNotNone(res)
        self.assertEqual(res["faixas"], get_city_data("SC", "Florianópolis")["faixas"])
        for cat in ("comercial", "industrial", "publica", "social"):
            if cat not in (get_city_data("SC", "Florianópolis").get("categorias") or {}):
                self.assertIsNone(get_city_tariffs_by_category("SC", "Florianópolis", category=cat))

    def test_categoria_coletada_usa_a_tabela_dela(self):
        from unittest import mock
        import netuno.core.tariffs_database as tdb
        base = dict(get_city_data("SC", "Florianópolis"))
        base["categorias"] = {"comercial": {"faixas": [[0.0, 999999.0, 6.81, 1]],
                                            "tarifa_fixa_mensal": 46.34,
                                            "fonte_url": "resolução"}}
        with mock.patch.object(tdb, "get_city_data", return_value=base):
            com = tdb.get_city_tariffs_by_category("SC", "Florianópolis", "comercial")
            self.assertEqual(com["faixas"], [[0.0, 999999.0, 6.81, 1]])
            self.assertEqual(com["categoria_tarifaria"], "comercial")
            self.assertNotIn("categorias", com)
            self.assertEqual(tdb.categorias_coletadas(base), ["residencial", "comercial"])

    def test_tab_tariffs_manager_widget(self):
        """Valida inicialização e componentes da aba TabTariffsManager."""
        tab = TabTariffsManager()
        self.assertIsNotNone(tab)
        self.assertGreater(tab.combo_uf.count(), 0)
        self.assertGreater(tab.combo_city.count(), 0)
        self.assertEqual(tab.combo_category.count(), 5)
        # Só as categorias com tabela coletada podem ser escolhidas.
        modelo = tab.combo_category.model()
        habilitadas = [tab.combo_category.itemData(i) for i in range(5) if modelo.item(i).isEnabled()]
        self.assertEqual(habilitadas, categorias_coletadas(tab.current_city_data))

        # Testa simulação de fatura
        tab.spin_sim_vol.setValue(20.0)
        tab.update_bill_simulation()
        self.assertIn("Total: R$", tab.lbl_sim_result.text())

    def test_americana_tab_tariffs_manager_billing(self):
        """Valida que Americana carrega a tabela com Inf=6.0 na faixa 3,49 e calcula rigorosamente R$ 28,60 e R$ 174,50."""
        tab = TabTariffsManager()
        tab.load_city_tariffs("SP", "Americana", "residencial")

        # Verifica tabela de faixas
        self.assertEqual(tab.table_tiers.rowCount(), 2)
        # Faixa 0: Consumo mínimo até 6 m³
        self.assertEqual(tab.table_tiers.item(0, 0).text(), "0.0")
        self.assertEqual(tab.table_tiers.item(0, 1).text(), "6.0")
        self.assertEqual(tab.table_tiers.item(0, 2).text(), "14.3000")
        self.assertEqual(tab.table_tiers.item(0, 3).text(), "Consumo Mínimo")

        # Faixa 1: Começa em 6.0 com taxa de 3.49
        self.assertEqual(tab.table_tiers.item(1, 0).text(), "6.0")
        self.assertEqual(tab.table_tiers.item(1, 1).text(), "> 99999")
        self.assertEqual(tab.table_tiers.item(1, 2).text(), "3.4900")
        self.assertEqual(tab.table_tiers.item(1, 3).text(), "Progressiva")

        # Teste 1: Consumo de 4 m³ (<= 6 m³) -> Total = R$ 28,60
        tab.spin_sim_vol.setValue(4.0)
        tab.update_bill_simulation()
        self.assertIn("Total: R$ 28.60/mês", tab.lbl_sim_result.text())

        # Teste 2: Consumo de 6 m³ (<= 6 m³) -> Total = R$ 28,60
        tab.spin_sim_vol.setValue(6.0)
        tab.update_bill_simulation()
        self.assertIn("Total: R$ 28.60/mês", tab.lbl_sim_result.text())

        # Teste 3: Consumo de 25 m³ (> 6 m³) -> Total = R$ 174,50 (25 × 3,49 × 2)
        tab.spin_sim_vol.setValue(25.0)
        tab.update_bill_simulation()
        self.assertIn("Total: R$ 174.50/mês", tab.lbl_sim_result.text())

    def test_slider_movement_preserves_chart_dimensions(self):
        """Garante que a movimentação do botão/slider de consumo não altera as dimensões e proporções da imagem."""
        tab = TabTariffsManager()
        tab.resize(1100, 750)
        tab.show()
        app.processEvents()

        p1_orig = tab.ax1.get_position().bounds
        p2_orig = tab.ax2.get_position().bounds
        c_w_orig = tab.canvas.width()
        c_h_orig = tab.canvas.height()

        for vol_val in [0, 5, 10, 15, 20, 30, 45, 50]:
            tab.slider_sim.setValue(vol_val)
            app.processEvents()
            self.assertEqual(tab.ax1.get_position().bounds, p1_orig)
            self.assertEqual(tab.ax2.get_position().bounds, p2_orig)
            self.assertEqual(tab.canvas.width(), c_w_orig)
            self.assertEqual(tab.canvas.height(), c_h_orig)

        tab.deleteLater()


if __name__ == "__main__":
    unittest.main()
