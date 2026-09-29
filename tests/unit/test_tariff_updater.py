"""
Testes unitários para o módulo de Atualização e Auditoria de Tarifas (Netuno 5).
Valida o parser da ANEEL, os scrapers de saneamento e o orquestrador do motor de atualização.
"""

import os
import unittest
from pathlib import Path

import pytest

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

    @pytest.mark.rede
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

    @pytest.mark.rede
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


# ---------------------------------------------------------------------------------
# Download da ANEEL sem rede: prazo total e cache nunca corrompido
# ---------------------------------------------------------------------------------

class _RespostaFalsa:
    def __init__(self, pedacos, relogio, passo_s):
        self._pedacos, self._relogio, self._passo = pedacos, relogio, passo_s

    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size):
        for pedaco in self._pedacos:
            self._relogio[0] += self._passo  # cada pedaço "leva" passo_s segundos
            if isinstance(pedaco, Exception):
                raise pedaco
            yield pedaco


def _preparar(monkeypatch, pedacos, passo_s):
    from netuno.core.tariff_updater import aneel_updater

    relogio = [0.0]
    monkeypatch.setattr(aneel_updater.time, "monotonic", lambda: relogio[0])
    monkeypatch.setattr(aneel_updater.requests, "get",
                        lambda *a, **k: _RespostaFalsa(pedacos, relogio, passo_s))
    return aneel_updater


def test_download_lento_para_no_prazo_e_preserva_o_cache(tmp_path, monkeypatch):
    """Um servidor que manda um pouco por minuto não prende o programa.

    O timeout do requests só vale entre pacotes; sem prazo total, a atualização
    de tarifas (e a integração contínua) esperariam indefinidamente.
    """
    modulo = _preparar(monkeypatch, [b"x" * 10] * 1000, passo_s=30.0)
    atualizador = modulo.AneelTariffUpdater(cache_dir=tmp_path)
    atualizador.cache_file.write_bytes(b"cache bom" * 200)

    assert atualizador.fetch_latest_csv(force_download=True) == str(atualizador.cache_file)
    assert atualizador.cache_file.read_bytes() == b"cache bom" * 200
    assert not list(tmp_path.glob("*.part"))


def test_download_interrompido_sem_cache_e_erro_claro(tmp_path, monkeypatch):
    modulo = _preparar(monkeypatch, [b"cabecalho;", ConnectionError("queda")], passo_s=1.0)
    atualizador = modulo.AneelTariffUpdater(cache_dir=tmp_path)

    with pytest.raises(RuntimeError, match="Não foi possível obter dados da ANEEL: queda"):
        atualizador.fetch_latest_csv(force_download=True)
    assert not atualizador.cache_file.exists()  # nada pela metade no lugar do cache
    assert not list(tmp_path.glob("*.part"))


def test_download_completo_substitui_o_cache(tmp_path, monkeypatch):
    modulo = _preparar(monkeypatch, [b"novo;" * 300, b"fim"], passo_s=1.0)
    atualizador = modulo.AneelTariffUpdater(cache_dir=tmp_path)
    atualizador.cache_file.write_bytes(b"antigo" * 300)

    atualizador.fetch_latest_csv(force_download=True)
    assert atualizador.cache_file.read_bytes() == b"novo;" * 300 + b"fim"
