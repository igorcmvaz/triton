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

    def test_florianopolis_multi_category_scaling(self):
        """Valida multiplicadores de tarifas para Florianópolis em diferentes categorias."""
        res = get_city_tariffs_by_category("SC", "Florianópolis", category="residencial")
        com = get_city_tariffs_by_category("SC", "Florianópolis", category="comercial")
        ind = get_city_tariffs_by_category("SC", "Florianópolis", category="industrial")
        soc = get_city_tariffs_by_category("SC", "Florianópolis", category="social")

        self.assertIsNotNone(res)
        self.assertIsNotNone(com)
        self.assertIsNotNone(ind)
        self.assertIsNotNone(soc)

        # Comercial deve ter tarifa fixa e unitária maior que residencial
        self.assertGreater(com["tarifa_fixa_mensal"], res["tarifa_fixa_mensal"])
        self.assertGreater(com["faixas"][0][2], res["faixas"][0][2])

        # Industrial deve ter tarifa maior que comercial
        self.assertGreater(ind["tarifa_fixa_mensal"], com["tarifa_fixa_mensal"])

        # Social deve ter desconto (tarifa menor que residencial)
        self.assertLess(soc["tarifa_fixa_mensal"], res["tarifa_fixa_mensal"])
        self.assertLess(soc["faixas"][0][2], res["faixas"][0][2])

    def test_tab_tariffs_manager_widget(self):
        """Valida inicialização e componentes da aba TabTariffsManager."""
        tab = TabTariffsManager()
        self.assertIsNotNone(tab)
        self.assertGreater(tab.combo_uf.count(), 0)
        self.assertGreater(tab.combo_city.count(), 0)
        self.assertEqual(tab.combo_category.count(), 5)

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


if __name__ == "__main__":
    unittest.main()
