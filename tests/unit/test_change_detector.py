"""
Testes unitários para o módulo de Detecção de Mudanças e Geração de Dashboard (Netuno 5).
"""

import os
import unittest
from pathlib import Path

from netuno.core.tariff_updater import (
    TariffChangeDetector,
    generate_interactive_dashboard,
)


class TestChangeDetector(unittest.TestCase):

    def setUp(self):
        self.detector = TariffChangeDetector()

    def test_compute_sha256(self):
        """Valida cálculo de hash criptográfico SHA-256."""
        h1 = self.detector.compute_sha256(b"teste 123")
        h2 = self.detector.compute_sha256(b"teste 123")
        h3 = self.detector.compute_sha256(b"outro conteudo")
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)

    def test_dashboard_generation(self):
        """Valida geração do arquivo HTML autônomo do dashboard."""
        sample_cities = {
            "SP - São Paulo": {
                "uf": "SP",
                "municipio": "São Paulo",
                "regiao": "Sudeste",
                "prestador_saneamento": "SABESP",
                "agencia_reguladora": "ARSESP",
                "tarifa_fixa_mensal": 40.42,
                "esgoto_pct": 100.0,
                "faixas": [[0.0, 10.0, 4.042, 1]],
                "distribuidora_energia": "ENEL Distribuição São Paulo",
                "energia_r_kwh": 0.78938,
                "fonte_url": "https://www.sabesp.com.br/tarifas",
                "status_global": "AUTO_OR_VERIFIED"
            }
        }
        sample_registry = {
            "monitored_urls": {
                "https://www.sabesp.com.br/tarifas": {
                    "content_sha256": "abcdef123456",
                    "status": "UNCHANGED",
                    "requires_manual_action": False
                }
            }
        }
        out_file = Path(__file__).resolve().parents[2] / "outputs" / "test_dashboard.html"
        html = generate_interactive_dashboard(sample_cities, sample_registry, output_path=out_file)

        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("São Paulo", html)
        self.assertIn("SABESP", html)
        self.assertTrue(out_file.exists())

        # Limpa arquivo de teste
        if out_file.exists():
            os.remove(out_file)


if __name__ == "__main__":
    unittest.main()
