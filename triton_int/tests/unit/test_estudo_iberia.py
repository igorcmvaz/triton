# -*- coding: utf-8 -*-
"""``triton estudo``: ``clima.iberia`` (município da base ibérica por código ou nome). IBE roda; BRL e INT recusam."""
import json
from pathlib import Path

import pytest

from triton.core import base_climatica_iberica as ib
from triton.core import estudo as E
from triton.core.edition import get_current_edition

RAIZ = Path(__file__).resolve().parents[2]
IBE = get_current_edition() == "IBE"
SUBS = {"area_captacao_m2": 200, "usuarios": 10, "demanda_per_capita_l_dia": 100, "fracao_pluvial_pct": 40,
        "volume_maximo_l": 5000, "passo_volume_l": 500}


def _doc(local, **clima):
    return {"esquema": {"nome": "triton-estudo", "versao": 1},
            "estudo": {"id": "teste-iberia", "titulo": "Teste", "tipologia": "escolar"},
            "projeto_base": {"modelo": "edicao"},
            "padroes": {"substituicoes": dict(SUBS)},
            "casos": [{"id": "a", "clima": {"iberia": {"local": local, **clima}}}],
            "analise": {"tipo": "economic"}}


def _validar(doc):
    return E.validar_documento(doc, RAIZ, verificar_arquivos=False)


@pytest.mark.skipif(IBE, reason="vale para BRL e INT")
def test_fora_da_ibe_a_base_iberica_e_recusada():
    _, erros, _ = _validar(_doc("ES-28079"))
    assert any("iberia" in e and "Edição Ibérica" in e for e in erros)


@pytest.mark.skipif(not (IBE and ib.disponivel()), reason="base ibérica só na IBE")
class TestIbe:
    def test_o_esquema_aceita_iberia(self):
        assert "iberia" in E.esquema_json()["properties"]["padroes"]["properties"]["clima"]["properties"]

    def test_codigo_nome_unico_e_rotulo_validam(self):
        for local in ("ES-28079", "Sevilla", "Madrid [ES-28079]", "PT-1106"):
            _, erros, _ = _validar(_doc(local))
            assert not erros, (local, erros)

    def test_nome_repetido_pede_o_codigo(self):
        repetido = next(u["nome"] for u in ib.unidades() if len(ib.candidatos(u["nome"])) > 1)
        _, erros, _ = _validar(_doc(repetido))
        assert any("ambíguo" in e and "ES-" in e for e in erros)

    def test_local_inexistente_e_sem_serie_sao_recusados(self):
        _, erros, _ = _validar(_doc("Atlantida"))
        assert any("não existe" in e for e in erros)
        _, erros, _ = _validar(_doc("ES-51001"))
        assert any("não tem série" in e for e in erros)

    def test_um_caso_de_espanha_roda_com_a_base_e_a_tarifa_da_camada_3(self, tmp_path):
        arq = tmp_path / "estudo.json"
        arq.write_text(json.dumps(_doc("ES-41091")), encoding="utf-8")
        plano, _ = E.carregar_plano(arq)
        r = E.executar_caso(plano, plano["casos"][0])
        assert r["status"] == "ok", r.get("erro")
        assert r["fonte_da_chuva"]["serie"]["dias"] == 10957
        assert any(a["papel"] == "base-iberia01" and len(a["sha256"]) == 64 for a in r["arquivos"])
        assert any("indicativa" in a or "média regional" in a for a in r["alertas"])
        assert any("Iberia01" in l for l in r["fonte_da_chuva"]["credit_and_licence"])
        assert not any("E-OBS" in l for l in r["fonte_da_chuva"]["credit_and_licence"])
        r2 = E.executar_caso(plano, plano["casos"][0])
        assert r["metricas"] == r2["metricas"]

    def test_ilha_roda_com_alerta_de_nivel_c(self, tmp_path):
        arq = tmp_path / "estudo.json"
        arq.write_text(json.dumps(_doc("PT-3103")), encoding="utf-8")
        plano, _ = E.carregar_plano(arq)
        r = E.executar_caso(plano, plano["casos"][0])
        assert r["status"] == "ok" and any("nível C" in a for a in r["alertas"])


@pytest.mark.skipif(not (IBE and ib.disponivel()), reason="base ibérica só na IBE")
class TestCli:
    def _cli(self, *args, tmp=None):
        import os
        import subprocess
        import sys
        env = {**os.environ, "TRITON_EDITION": "IBE", "PYTHONIOENCODING": "utf-8"}
        return subprocess.run([sys.executable, "-m", "triton.cli", *args], cwd=RAIZ, env=env, capture_output=True,
                              text=True, encoding="utf-8", timeout=600)

    def test_locais_procura_por_nome_e_por_codigo(self):
        r = self._cli("locais", "sevilla", "--limite", "3")
        assert r.returncode == 0 and "ES-41091\tSevilla" in r.stdout
        assert "Espanha 8131 locais" in r.stderr
        j = self._cli("locais", "PT-1106", "--format", "json")
        assert '"codigo": "PT-1106"' in j.stdout

    def test_run_com_local_usa_a_chuva_do_municipio(self, tmp_path):
        saida = tmp_path / "r.json"
        r = self._cli("run", "examples/portugal/lisboa.triton", "--local", "ES-41091", "--format", "json", "--output", str(saida))
        assert r.returncode == 0, r.stderr
        texto = saida.read_text(encoding="utf-8")
        assert "Iberia01" in texto and "Sevilla" in texto

    def test_local_com_nome_ambiguo_falha_com_as_alternativas(self):
        repetido = next(u["nome"] for u in ib.unidades() if len(ib.candidatos(u["nome"])) > 1)
        r = self._cli("run", "examples/portugal/lisboa.triton", "--local", repetido)
        assert r.returncode == 2 and "ambíguo" in r.stderr
