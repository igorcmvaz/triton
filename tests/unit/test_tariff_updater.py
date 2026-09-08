"""
Testes unitários para o módulo de Atualização e Auditoria de Tarifas (Netuno 5).
Valida o parser da ANEEL, os scrapers de saneamento e o orquestrador do motor de atualização.
"""

import os
import unittest
from pathlib import Path

from netuno.core.tariff_updater import (
    AneelTariffUpdater,
    SanitationScraperRegistry,
    TariffUpdateEngine,
    generate_update_report,
)
from netuno.core.tariffs_database import load_tariffs_db, get_city_data


class TestTariffUpdater(unittest.TestCase):

    def setUp(self):
        self.engine = TariffUpdateEngine()

    def test_aneel_distributor_matching(self):
        """Valida que distribuidoras conhecidas são mapeadas corretamente."""
        updater = AneelTariffUpdater()
        updater.load_and_parse(force_download=False)

        # Testa distribuidora de São Paulo
        sp_res = updater.get_tariff_for_distributor("ENEL Distribuição São Paulo")
        self.assertIsNotNone(sp_res)
        self.assertEqual(sp_res["distribuidora"], "ELETROPAULO")
        self.assertGreater(sp_res["energia_r_kwh"], 0.5)

        # Testa COPEL (Paraná)
        pr_res = updater.get_tariff_for_distributor("COPEL Distribuição")
        self.assertIsNotNone(pr_res)
        self.assertEqual(pr_res["distribuidora"], "COPEL-DIS")
        self.assertGreater(pr_res["energia_r_kwh"], 0.5)

        # Testa CELESC (Santa Catarina)
        sc_res = updater.get_tariff_for_distributor("CELESC Distribuição")
        self.assertIsNotNone(sc_res)
        self.assertEqual(sc_res["distribuidora"], "CELESC")

    def test_sanitation_registry_matching(self):
        """Valida identificação de concessionárias estaduais no registro."""
        registry = SanitationScraperRegistry()

        sample_city = {
            "prestador_saneamento": "SABESP",
            "agencia_reguladora": "ARSESP",
            "tarifa_fixa_mensal": 40.42,
            "esgoto_pct": 100.0,
            "confianca_grau": "A — alta"
        }
        res = registry.update_city_sanitation("São Paulo", "SP", sample_city)
        self.assertIn(res["update_status_sanitation"], ["AUTO_SCRAPED", "VERIFIED_AUDIT"])
        self.assertEqual(res["agencia_reguladora"], "ARSESP")

    def test_dry_run_execution(self):
        """Valida execução em modo dry-run para um estado específico (SC)."""
        res = self.engine.run_update(mode="all", target_uf="SC", dry_run=True)
        self.assertTrue(res["dry_run"])
        stats = res["stats"]
        self.assertGreater(stats["processed"], 0)
        self.assertGreater(stats["overall_auto_or_verified"], 0)

        # Valida geração de relatório em Markdown
        report = generate_update_report(res)
        self.assertIn("Relatório Executivo de Atualização Tarifária", report)
        self.assertIn("Dry Run", report)


if __name__ == "__main__":
    unittest.main()
