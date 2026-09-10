"""
Testes unitários e de integração para o Banco de Dados de Tarifas Municipais (Netuno 5).
Valida as 652 cidades, 27 UFs, integridade dos registros e o cálculo de faturas.
"""

import os
import sys
import unittest
import pytest

from PySide6.QtWidgets import QApplication

# Garante instância de QApplication para testes de UI
app = QApplication.instance() or QApplication(sys.argv)

from netuno.core.tariffs_database import (
    load_tariffs_db, get_available_ufs, get_cities_by_uf, get_city_data,
    search_cities, get_total_cities_count
)
from netuno.core.parser import NetunoConfig
from netuno.core.economic import calculate_water_bill
from netuno.core.tariffs_structure import CODIGOS_VALIDOS
from netuno.ui.dialogs.dialog_economic import DialogTariffs


class TestTariffsDatabase(unittest.TestCase):
    
    def test_database_loading(self):
        """Verifica o carregamento do banco de dados oficial e contagem de cidades/UFs."""
        db = load_tariffs_db()
        self.assertIsNotNone(db)
        self.assertEqual(get_total_cities_count(), 652)
        
        ufs = get_available_ufs()
        self.assertEqual(len(ufs), 27)
        uf_codes = [u[0] for u in ufs]
        self.assertIn("SC", uf_codes)
        self.assertIn("SP", uf_codes)
        self.assertIn("DF", uf_codes)
        self.assertIn("MG", uf_codes)
        self.assertIn("BA", uf_codes)
        self.assertIn("AM", uf_codes)
        self.assertIn("RS", uf_codes)

    def test_all_652_cities_integrity(self):
        """Verifica a integridade de todas as 652 cidades do catálogo."""
        ufs = get_available_ufs()
        total_cities_found = 0
        
        for uf_code, state_name in ufs:
            cities = get_cities_by_uf(uf_code)
            self.assertGreater(len(cities), 0, f"UF {uf_code} não possui cidades cadastradas")
            
            for city_name in cities:
                total_cities_found += 1
                data = get_city_data(uf_code, city_name)
                self.assertIsNotNone(data, f"Dados nulos para {uf_code} - {city_name}")
                self.assertEqual(data['uf'], uf_code)
                self.assertEqual(data['municipio'], city_name)
                self.assertTrue(len(data['prestador_saneamento']) > 0)
                self.assertGreater(data['esgoto_pct'], 0.0)
                self.assertGreater(len(data['faixas']), 0, f"Sem faixas em {uf_code} - {city_name}")
                
                # Valida tuplas de faixas
                for t in data['faixas']:
                    self.assertEqual(len(t), 4)
                    min_v, max_v, val, is_fix = t
                    self.assertGreaterEqual(min_v, 0.0)
                    self.assertGreaterEqual(val, 0.0)
                    # Os códigos são definidos em netuno/core/tariffs_structure.py,
                    # fonte única desde a 5.0.7. Antes disso eram literais espalhados
                    # pelo código, e este teste rejeitava a tarifa legítima da DAE
                    # Americana por desconhecer a franquia de consumo mínimo (-2).
                    self.assertIn(
                        is_fix, CODIGOS_VALIDOS,
                        f"código de faixa desconhecido {is_fix} em {uf_code}/{city_name}; "
                        f"conhecidos: {sorted(CODIGOS_VALIDOS)}"
                    )
                    
        self.assertEqual(total_cities_found, 652)

    def test_sample_reference_cities(self):
        """Valida dados e cálculos de capitais e cidades de referência."""
        # 1. Florianópolis (CASAN)
        fl = get_city_data("SC", "Florianópolis")
        self.assertIsNotNone(fl)
        self.assertEqual(fl['prestador_saneamento'], "CASAN")
        self.assertEqual(fl['esgoto_pct'], 100.0)
        self.assertTrue(fl['fonte_url'].startswith("http"))
        self.assertGreater(fl['energia_r_kwh'], 0.0)
        
        # Teste de conta d'água para 10 m³ (10.000 Litros) em Florianópolis
        # TFDI fixo R$ 46.34 + 10 m³ * R$ 3.08/m³ = R$ 77.14 água; Esgoto 100% = R$ 77.14 -> Total R$ 154.28
        bill_10m3 = calculate_water_bill(10000.0, fl['faixas'], sewage_mode=1, sewage_rate=fl['esgoto_pct'])
        self.assertAlmostEqual(bill_10m3, 154.28, delta=0.5)

        # 2. São Paulo (SABESP)
        sp = get_city_data("SP", "São Paulo")
        self.assertIsNotNone(sp)
        self.assertEqual(sp['prestador_saneamento'], "SABESP")
        self.assertEqual(sp['esgoto_pct'], 100.0)
        self.assertTrue(sp['fonte_url'].startswith("http"))

        # 3. Brasília (CAESB)
        df = get_city_data("DF", "Brasília")
        self.assertIsNotNone(df)
        self.assertEqual(df['prestador_saneamento'], "CAESB")
        self.assertEqual(df['esgoto_pct'], 100.0)

        # 4. Belo Horizonte (COPASA)
        bh = get_city_data("MG", "Belo Horizonte")
        self.assertIsNotNone(bh)
        self.assertEqual(bh['prestador_saneamento'], "COPASA")
        # COPASA cobra 74% da agua no esgoto dinamico (coleta e tratamento),
        # conforme a ARSAE-MG e as seis faixas da coleta auditada. O banco
        # guardava 80%, que era o valor de recurso.
        self.assertAlmostEqual(bh['esgoto_pct'], 74.0, delta=0.5)

    def test_dialog_tariffs_ui(self):
        """Valida inicialização e comportamento do diálogo DialogTariffs."""
        cfg = NetunoConfig()
        cfg.tariff_city_uf = "SC"
        cfg.tariff_city_name = "Florianópolis"
        
        dlg = DialogTariffs(config=cfg)
        self.assertIsNotNone(dlg)
        
        # Confirma que a UF e cidade foram selecionadas e esgoto CASAN = 100%
        self.assertEqual(dlg.combo_uf.currentData(), "SC")
        self.assertEqual(dlg.combo_city.currentText(), "Florianópolis")
        self.assertGreater(dlg.table.rowCount(), 0)
        self.assertEqual(dlg.txt_esg_val.text(), "100,0")
        
        # Testa troca de cidade para MG - Belo Horizonte
        mg_idx = dlg.combo_uf.findData("MG")
        dlg.combo_uf.setCurrentIndex(mg_idx)
        dlg.combo_city.setCurrentText("Belo Horizonte")
        self.assertIn("COPASA", dlg.lbl_prestador.text())
        # O percentual exibido vem do banco, e nao de um numero congelado no
        # teste: corrigir a fonte nao pode quebrar a verificacao da tela.
        _pct = get_city_data("MG", "Belo Horizonte")["esgoto_pct"]
        self.assertIn(f"{_pct:.0f}%", dlg.lbl_prestador.text())
        self.assertEqual(dlg.txt_esg_val.text(), f"{_pct:.1f}".replace(".", ","))
        
        # Testa sobrescrita manual pelo usuário: usuário troca para 75%
        dlg.txt_esg_val.setText("75,0")
        dlg.on_accept()
        self.assertEqual(cfg.tariff_city_uf, "MG")
        self.assertEqual(cfg.tariff_city_name, "Belo Horizonte")
        self.assertEqual(cfg.sewage_rate, 75.0)

    def test_tab_project_tariff_location(self):
        """Valida que o seletor de localização de tarifas na Etapa 1 (TabProject) pre-configura tarifas e energia."""
        from netuno.ui.tab_project import TabProject
        tab = TabProject()
        self.assertIsNotNone(tab)
        
        # Default de SC - Florianópolis
        self.assertEqual(tab.combo_tariff_uf.currentData(), "SC")
        self.assertEqual(tab.combo_tariff_city.currentText(), "Florianópolis")
        self.assertIn("CASAN", tab.lbl_t_prestador.text())
        self.assertIn("100%", tab.lbl_t_prestador.text())
        
        # Troca para SP - São Paulo
        sp_idx = tab.combo_tariff_uf.findData("SP")
        tab.combo_tariff_uf.setCurrentIndex(sp_idx)
        tab.combo_tariff_city.setCurrentText("São Paulo")
        
        cfg = tab._get_config()
        self.assertEqual(cfg.tariff_city_uf, "SP")
        self.assertEqual(cfg.tariff_city_name, "São Paulo")
        self.assertIn("SABESP", tab.lbl_t_prestador.text())
        self.assertIn("ENEL", tab.lbl_t_elec.text())

    def test_dialog_electricity_ui(self):
        """Valida inicialização e comportamento do diálogo DialogElectricity com ANEEL B1."""
        from netuno.ui.dialogs.dialog_economic import DialogElectricity
        cfg = NetunoConfig()
        cfg.elec_city_uf = "RO"
        cfg.elec_city_name = "Ariquemes"
        
        dlg = DialogElectricity(config=cfg)
        self.assertIsNotNone(dlg)
        self.assertEqual(dlg.combo_elec_uf.currentData(), "RO")
        self.assertEqual(dlg.combo_elec_city.currentText(), "Ariquemes")
        
        # Verifica se puxou automaticamente a tarifa homologada de Rondônia (0.8414)
        self.assertIn("Energisa", dlg.lbl_elec_dist.text())
        self.assertIn("Residencial B1", dlg.lbl_elec_tipo.text())
        self.assertAlmostEqual(float(dlg.txt_elec_tariff.text().replace(',', '.')), 0.8414, delta=0.001)
        
        # Testa troca para SP - São Paulo
        sp_idx = dlg.combo_elec_uf.findData("SP")
        dlg.combo_elec_uf.setCurrentIndex(sp_idx)
        dlg.combo_elec_city.setCurrentText("São Paulo")
        self.assertAlmostEqual(float(dlg.txt_elec_tariff.text().replace(',', '.')), 0.7894, delta=0.001)
        
        # Testa edição manual pelo usuário: usuário digita 0,9500
        dlg.txt_elec_tariff.setText("0,9500")
        dlg.on_accept()
        self.assertEqual(cfg.elec_city_uf, "SP")
        self.assertEqual(cfg.elec_city_name, "São Paulo")
        self.assertAlmostEqual(cfg.elec_tariff, 0.9500, delta=0.001)


if __name__ == "__main__":
    unittest.main()

