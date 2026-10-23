# -*- coding: utf-8 -*-
"""Licença da E-OBS com a base instalada: os dois caminhos da constante do bloqueio (D1).

Só vale na IBE (``tests/so_da_ibe.txt``).
"""
import pytest

from triton.core import base_climatica_portugal as pt
from triton.core import licenca_eobs as L

pytestmark = pytest.mark.skipif(not pt.caminho_da_base(), reason="data/portugal_eobs.db ausente")


class Armazem:
    def __init__(self, valor=None):
        self.dados = {} if valor is None else {"licenca_eobs/uso": valor}

    def value(self, chave, padrao=""):
        return self.dados.get(chave, padrao)

    def setValue(self, chave, valor):
        self.dados[chave] = valor

    def sync(self):
        pass


@pytest.fixture
def uso(monkeypatch):
    """Fixa a escolha de uso sem tocar na configuração real do utilizador."""
    def fixar(valor):
        arm = Armazem(valor)
        monkeypatch.setattr(L, "_armazem", lambda: arm)
    return fixar


def test_caminho_padrao_uso_comercial_nao_bloqueia_a_base(uso):
    assert L.BLOQUEAR_E_OBS_EM_USO_COMERCIAL is False
    uso("comercial")
    assert pt.disponivel() is True
    serie = pt.carregar_serie("Lisboa", "01/01/2001", "31/12/2002")[0]
    assert len(serie) == 730


def test_caminho_bloqueado_uso_comercial_desliga_a_e_obs(uso, monkeypatch):
    monkeypatch.setattr(L, "BLOQUEAR_E_OBS_EM_USO_COMERCIAL", True)
    uso("comercial")
    assert pt.disponivel() is False
    with pytest.raises(L.LicencaEObsBloqueada):
        pt.carregar_serie("Lisboa")
    from triton.core.parser import TritonConfig, serie_da_climbra
    cfg = TritonConfig()
    cfg.climate_city_name, cfg.climate_scenario = "Lisboa", pt.CENARIO_EOBS
    with pytest.raises(L.LicencaEObsBloqueada):
        serie_da_climbra(cfg)
    from triton.core import qualidade_chuva as Q
    assert not Q.tem_qualidade()          # sem a E-OBS, nenhum dado dela é mostrado (nem a cobertura)


def test_caminho_bloqueado_uso_de_pesquisa_ou_sem_escolha_segue(uso, monkeypatch):
    monkeypatch.setattr(L, "BLOQUEAR_E_OBS_EM_USO_COMERCIAL", True)
    for escolha in ("pesquisa", None):
        uso(escolha)
        assert pt.disponivel() is True
        assert len(pt.carregar_serie("Lisboa", "01/01/2001", "31/12/2001")[0]) == 365


def test_o_projeto_aberto_com_a_e_obs_bloqueada_avisa_e_nao_inventa_serie(uso, monkeypatch, tmp_path):
    """Referência sem série incorporada, base bloqueada: aviso de «base indisponível», sem chuva inventada."""
    from triton.core.parser import TritonConfig, export_triton_json, load_triton_project, serie_da_climbra
    cfg = TritonConfig()
    cfg.climate_source_mode, cfg.climate_city_uf, cfg.climate_city_name = "national_db", "Lisboa", "Lisboa"
    cfg.climate_model, cfg.climate_scenario = pt.MODELO_EOBS, pt.CENARIO_EOBS
    cfg.climate_start_date, cfg.climate_end_date, cfg.start_date = "01/01/2001", "31/12/2005", "01/01/2001"
    destino = tmp_path / "l.triton"
    export_triton_json(cfg, str(destino), precip_data=serie_da_climbra(cfg), incorporar_serie=False)
    monkeypatch.setattr(L, "BLOQUEAR_E_OBS_EM_USO_COMERCIAL", True)
    uso("comercial")
    proj = load_triton_project(str(destino))
    assert proj["precip_data"] is None and "não está disponível" in proj["aviso_chuva"]
    assert "desligada" in proj["aviso_chuva"]


def test_o_aviso_traz_a_versao_da_e_obs_do_banco():
    assert "v33.0e" in L.texto_do_aviso()
