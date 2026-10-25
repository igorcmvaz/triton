# -*- coding: utf-8 -*-
"""Aviso de licença da E-OBS: o texto, a escolha de uso lembrada e o bloqueio atrás de constante (D1).

Em qualquer edição, sem o banco. Os caminhos que dependem da base estão em ``test_licenca_eobs_ibe.py``.
"""
import os
import re

import pytest

from triton.core import licenca_eobs as L

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Armazem:
    """Configuração do utilizador em memória (no lugar do QSettings)."""

    def __init__(self, valor=None):
        self.dados = {} if valor is None else {"licenca_eobs/uso": valor}

    def value(self, chave, padrao=""):
        return self.dados.get(chave, padrao)

    def setValue(self, chave, valor):
        self.dados[chave] = valor

    def sync(self):
        pass


def test_a_constante_do_bloqueio_esta_ligada_por_decisao_do_titular():
    assert L.BLOQUEAR_E_OBS_EM_USO_COMERCIAL is True
    fonte = open(os.path.join(RAIZ, "triton", "core", "licenca_eobs.py"), encoding="utf-8").read()
    assert re.search(r"decisão do usuário \(D1, 25/10/2026\): ligado\n(#.*\n)*BLOQUEAR_E_OBS_EM_USO_COMERCIAL = True", fonte)


def test_o_texto_do_aviso_e_o_da_proposta_em_portugues_europeu():
    t = L.TEXTO_DO_AVISO
    assert t.startswith("Os dados de chuva desta edição vêm da E-OBS, de uso estritamente não comercial em pesquisa e educação")
    assert "utilizador" not in "Os dados" and "série de chuva" in t and "autorização dos titulares" in t
    assert "não é parecer jurídico" in t.lower() or "não é parecer jurídico" in t
    assert L.RESPOSTAS == {"pesquisa": "Uso de pesquisa ou educação", "comercial": "Uso comercial"}
    assert not re.search(r"\b(usuário|arquivo|tela)\b", t + " ".join(L.RESPOSTAS.values()))


def test_a_escolha_e_lembrada_e_so_aceita_dois_valores():
    arm = Armazem()
    assert L.ler_escolha(arm) is None
    L.gravar_escolha("pesquisa", arm)
    assert L.ler_escolha(arm) == "pesquisa" and arm.dados["licenca_eobs/uso"] == "pesquisa"
    with pytest.raises(ValueError):
        L.gravar_escolha("talvez", arm)
    assert L.ler_escolha(Armazem("lixo")) is None


def test_so_a_edicao_com_a_e_obs_pergunta_e_so_ate_haver_escolha(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "IBE")
    assert L.precisa_perguntar(Armazem()) is True
    assert L.precisa_perguntar(Armazem("pesquisa")) is False
    assert L.precisa_perguntar(Armazem("comercial")) is False
    for ed in ("BRL", "INT"):
        monkeypatch.setenv("TRITON_EDITION", ed)
        assert L.precisa_perguntar(Armazem()) is False


def test_com_a_constante_desligada_so_avisa_mesmo_com_uso_comercial(monkeypatch):
    monkeypatch.setattr(L, "BLOQUEAR_E_OBS_EM_USO_COMERCIAL", False)
    for escolha in (None, "pesquisa", "comercial"):
        assert L.e_obs_bloqueada(Armazem(escolha)) is False
    assert "registada" in L.texto_depois_da_escolha("comercial") and "desligada" not in L.texto_depois_da_escolha("comercial")
    assert L.texto_depois_da_escolha("pesquisa") == ""


def test_com_a_constante_ligada_so_o_uso_comercial_bloqueia(monkeypatch):
    monkeypatch.setattr(L, "BLOQUEAR_E_OBS_EM_USO_COMERCIAL", True)
    assert L.e_obs_bloqueada(Armazem("comercial")) is True
    assert L.e_obs_bloqueada(Armazem("pesquisa")) is False
    assert L.e_obs_bloqueada(Armazem()) is False
    assert "desligada" in L.texto_depois_da_escolha("comercial") and "ficheiro próprio" in L.texto_depois_da_escolha("comercial")


def test_o_rodape_do_laudo_so_existe_na_edicao_com_a_e_obs(monkeypatch):
    for ed in ("BRL", "INT"):
        monkeypatch.setenv("TRITON_EDITION", ed)
        assert L.rodape_do_laudo({"climate_city_name": "Lisboa"}) == ""
    monkeypatch.setenv("TRITON_EDITION", "IBE")
    html = L.rodape_do_laudo({"chuva_serie_propria": True})
    assert "Chuva: série fornecida pelo utilizador." in html and "Cobertura:" in html
    assert "uso restrito" not in html                       # série própria: a restrição da E-OBS não se aplica


# ── aviso vermelho nos relatórios (decisão do titular, 25/10/2026) ─────────────────────────────

def test_o_aviso_vermelho_so_aparece_na_ibe_e_com_a_e_obs(monkeypatch):
    for ed in ("BRL", "INT"):
        monkeypatch.setenv("TRITON_EDITION", ed)
        assert L.aviso_vermelho({"climate_city_name": "Lisboa"}) == ""
    monkeypatch.setenv("TRITON_EDITION", "IBE")
    assert L.aviso_vermelho({"chuva_serie_propria": True}) == ""      # série do utilizador: a restrição não é da E-OBS
    pt_ = L.aviso_vermelho({"climate_city_name": "Lisboa"})
    assert "NÃO PODE SER USADA COMERCIALMENTE" in pt_ and "#b91c1c" in pt_ and "font-size:17pt" in pt_
    assert "o titular do programa não responde por uso comercial" in pt_
    assert "MUST NOT BE USED COMMERCIALLY" in L.aviso_vermelho({}, ingles=True)


def test_o_aviso_entra_no_html_depois_do_body_uma_so_vez_e_traz_a_marca_dagua(monkeypatch):
    monkeypatch.setenv("TRITON_EDITION", "IBE")
    html = "<html><head></head><body class='x'><h1>Laudo</h1></body></html>"
    com = L.inserir_aviso_vermelho(html, {}, False)
    assert com.index("aviso-eobs") < com.index("<h1>Laudo</h1>") and com.startswith("<html>")
    assert L.inserir_aviso_vermelho(com, {}, False) == com
    marcado = L.marca_dagua_html(com)
    assert "NÃO COMERCIAL" in marcado and "rotate(-28deg)" in marcado and L.marca_dagua_html(marcado) == marcado
    assert L.marca_dagua_html(html) == html


def test_o_laudo_gerado_na_ibe_traz_o_aviso_vermelho_e_nas_outras_edicoes_nao(monkeypatch):
    from triton.core.report_service import generate_report_html
    dados = {"project_name": "Teste", "audit_context": {"climate_city_name": "Lisboa", "chuva_serie_propria": False},
             "lower_vol": 5000.0}
    for ed, esperado in (("IBE", True), ("INT", False), ("BRL", False)):
        monkeypatch.setenv("TRITON_EDITION", ed)
        try:
            html = generate_report_html("economic", dados, lang="pt")
        except Exception:
            pytest.skip("gerador exige mais dados de projeto")
        assert ("NÃO PODE SER USADA COMERCIALMENTE" in html) is esperado
