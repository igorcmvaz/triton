"""
Testes unitários e de integração para o Banco de Dados de Tarifas Municipais (Triton).
Valida as 652 cidades, 27 UFs, integridade dos registros e o cálculo de faturas.
"""

import unittest


# Garante instância de QApplication para testes de UI

from triton.core.tariffs_database import (
    load_tariffs_db, get_available_ufs, get_cities_by_uf, get_city_data,
    search_cities, get_total_cities_count
)
from triton.core.parser import TritonConfig
from triton.core.economic import calculate_water_bill
from triton.core.tariffs_structure import CODIGOS_VALIDOS
from triton.ui.dialogs.dialog_economic import DialogTariffs


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
                if data.get('fonte_registro') and data['esgoto_pct'] == 0.0:
                    pass  # documento sem esgoto (Humaitá: a lei só tarifa a água)
                else:
                    self.assertGreater(data['esgoto_pct'], 0.0)
                self.assertGreater(len(data['faixas']), 0, f"Sem faixas em {uf_code} - {city_name}")
                
                # Valida tuplas de faixas
                for t in data['faixas']:
                    self.assertEqual(len(t), 4)
                    min_v, max_v, val, is_fix = t
                    self.assertGreaterEqual(min_v, 0.0)
                    self.assertGreaterEqual(val, 0.0)
                    # Os códigos são definidos em triton/core/tariffs_structure.py,
                    # fonte única do programa. Antes eram literais espalhados
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


    def test_tab_project_tariff_location(self):
        """Valida que o seletor de localização de tarifas na Etapa 1 (TabProject) pre-configura tarifas e energia."""
        from triton.ui.tab_project import TabProject
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


if __name__ == "__main__":
    unittest.main()
