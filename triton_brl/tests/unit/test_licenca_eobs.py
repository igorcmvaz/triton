# -*- coding: utf-8 -*-
"""Aviso de licença da E-OBS: o texto, a escolha de uso lembrada e o bloqueio atrás de constante (D1).

Em qualquer edição, sem o banco. Os caminhos que dependem da base estão em ``test_licenca_eobs_prt.py``.
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


def test_a_constante_do_bloqueio_esta_desligada_e_comentada_como_decisao_pendente():
    assert L.BLOQUEAR_E_OBS_EM_USO_COMERCIAL is False
    fonte = open(os.path.join(RAIZ, "triton", "core", "licenca_eobs.py"), encoding="utf-8").read()
    assert re.search(r"decisão do usuário pendente \(D1\)\n(#.*\n)*BLOQUEAR_E_OBS_EM_USO_COMERCIAL = False", fonte)


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
    monkeypatch.setenv("TRITON_EDITION", "PRT")
    assert L.precisa_perguntar(Armazem()) is True
    assert L.precisa_perguntar(Armazem("pesquisa")) is False
    assert L.precisa_perguntar(Armazem("comercial")) is False
    for ed in ("BRL", "INT"):
        monkeypatch.setenv("TRITON_EDITION", ed)
        assert L.precisa_perguntar(Armazem()) is False


def test_por_defeito_nada_e_bloqueado_nem_com_uso_comercial(monkeypatch):
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
    monkeypatch.setenv("TRITON_EDITION", "PRT")
    html = L.rodape_do_laudo({"chuva_serie_propria": True})
    assert "Chuva: série fornecida pelo utilizador." in html and "Cobertura:" in html
    assert "uso restrito" not in html                       # série própria: a restrição da E-OBS não se aplica
