# -*- coding: utf-8 -*-
"""``--progresso {auto,rich,simples}`` em ``estudo run`` e ``estudo lote``: saída de erro, queda para ``simples`` e bytes iguais."""
import argparse
import io
import os
import re
import sys
from pathlib import Path

import pytest

from triton import cli_estudo
from triton import cli_progresso as PR
from triton.core import _opcional
from triton.core import estudo as E
from triton.core.edition import get_current_edition

RAIZ = Path(__file__).resolve().parents[2]
ED = get_current_edition()
EXEMPLO = RAIZ / "examples" / "estudos" / {"BRL": "tres-tipologias-exemplo", "INT": "residencial-unifamiliar-exemplo",
                                          "IBE": "residencial-unifamiliar-exemplo"}[ED] / "estudo.json"
TEM_EXEMPLO = pytest.mark.skipif(not EXEMPLO.is_file(), reason="estudo-exemplo ausente nesta edição")
TEM_RICH = _opcional.disponivel("rich")


@pytest.fixture(autouse=True)
def _data_fixa(monkeypatch):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")


def _parser():
    p = argparse.ArgumentParser()
    cli_estudo.registrar(p.add_subparsers(dest="command"))
    return p


def _rodar(argv, capsys):
    args = _parser().parse_args(["estudo", *argv])
    codigo = cli_estudo.executar(args)
    cap = capsys.readouterr()
    return codigo, cap.out, cap.err


def _lido(pasta):
    return {p.relative_to(pasta).as_posix(): p.read_bytes() for p in sorted(Path(pasta).rglob("*")) if p.is_file()}


# ── escolha do modo (sem rodar nada) ──────────────────────────────────────────────────────────

def test_modo_simples_nunca_avisa_e_auto_depende_de_pacote_e_terminal():
    assert PR.escolher_modo("simples", True, True) == ("simples", None)
    assert PR.escolher_modo("auto", True, True) == ("rich", None)
    assert PR.escolher_modo("auto", True, False) == ("simples", None)       # saída de erro redirecionada
    assert PR.escolher_modo("auto", False, True) == ("simples", None)       # sem o pacote: cai sem barulho
    assert PR.escolher_modo("rich", True, False) == ("rich", None)          # pedido explícito vale mesmo sem terminal


def test_rich_pedido_sem_o_pacote_cai_em_simples_com_aviso_que_diz_o_extra():
    modo, aviso = PR.escolher_modo("rich", False, True)
    assert modo == "simples" and aviso and "rich" in aviso and "[cli]" in aviso
    with pytest.raises(ValueError):
        PR.escolher_modo("xyz")


def test_sem_stderr_o_rich_explicito_cai_em_simples(monkeypatch):
    monkeypatch.setattr(sys, "stderr", None)
    assert PR.escolher_modo("rich", True, True) == ("simples", None)
    assert PR.escolher_modo("auto") == ("simples", None)


def test_quiet_desliga_tudo_sem_avaliar_o_modo(monkeypatch, capsys):
    monkeypatch.setattr(_opcional, "disponivel", lambda nome: False)
    log, progresso, fechar = PR.criar("rich", True)
    assert log is None and progresso is None
    fechar()
    assert capsys.readouterr().err == ""


def test_aviso_de_rich_ausente_sai_uma_vez_na_saida_de_erro(monkeypatch, capsys):
    monkeypatch.setattr(_opcional, "disponivel", lambda nome: False)
    log, progresso, fechar = PR.criar("rich", False)
    fechar()
    err = capsys.readouterr().err
    assert log is not None and progresso is None
    assert err.count("rich") >= 1 and len([l for l in err.splitlines() if l.strip()]) == 1


# ── execução: saída de erro, bytes idênticos ──────────────────────────────────────────────────

@TEM_EXEMPLO
def test_simples_escreve_as_linhas_de_caso_na_saida_de_erro_e_o_resumo_na_padrao(tmp_path, capsys):
    codigo, out, err = _rodar(["run", str(EXEMPLO), "--saida", str(tmp_path / "s"), "--progresso", "simples"], capsys)
    assert codigo == 0
    assert len(re.findall(r"^\[\d/3\] ", err, re.M)) == 3 and "[1/3]" not in out
    assert "resultados.csv" in out


@TEM_EXEMPLO
def test_os_arquivos_de_resultado_sao_identicos_em_qualquer_modo(tmp_path, capsys, monkeypatch):
    saidas = {}
    for modo in ("simples", "auto", "rich"):
        if modo == "rich" and not TEM_RICH:
            monkeypatch.setattr(_opcional, "disponivel", lambda nome: False)      # cai em simples, com aviso
        codigo, out, err = _rodar(["run", str(EXEMPLO), "--saida", str(tmp_path / modo), "--progresso", modo], capsys)
        assert codigo == 0, err
        saidas[modo] = _lido(tmp_path / modo)
    quiet = tmp_path / "quiet"
    assert _rodar(["run", str(EXEMPLO), "--saida", str(quiet), "--quiet"], capsys)[0] == 0
    saidas["quiet"] = _lido(quiet)
    base = saidas["simples"]
    assert "resultados.csv" in base and len(base) > 6
    for modo, arquivos in saidas.items():
        assert arquivos == base, modo


@TEM_EXEMPLO
@pytest.mark.skipif(not TEM_RICH, reason="extra «cli» (rich) não instalado")
def test_rich_desenha_na_saida_de_erro_e_nao_na_padrao(tmp_path, capsys):
    codigo, out, err = _rodar(["run", str(EXEMPLO), "--saida", str(tmp_path / "r"), "--progresso", "rich"], capsys)
    assert codigo == 0
    assert "3/3" in err or "3" in err                      # a barra vai para stderr
    assert "[1/3]" not in err and "[1/3]" not in out        # sem as linhas do modo simples
    assert "resultados.csv" in out                          # o resumo final segue na saída padrão


def test_lote_aceita_progresso_e_da_os_mesmos_bytes(tmp_path, capsys):
    import shutil
    from tests.unit.test_estudo_execucao import _estudo, _gravar, _pasta_com_base
    pasta = _pasta_com_base(tmp_path)
    lote = pasta / "lote"
    lote.mkdir()
    shutil.copyfile(pasta / "base.triton", lote / "base.triton")
    _gravar(lote, "estudo_a.json", _estudo("escolas", "escolar"))
    _gravar(lote, "estudo_b.json", _estudo("hospitais", "hospitalar", [
        {"id": "h1", "nome": "H1", "substituicoes": {"area_captacao_m2": 300}}]))
    a = _rodar(["lote", str(lote), "--saida", str(tmp_path / "a"), "--progresso", "simples"], capsys)
    b = _rodar(["lote", str(lote), "--saida", str(tmp_path / "b"), "--progresso", "auto", "--quiet"], capsys)
    assert a[0] == 0 and b[0] == 0, a[2]
    assert _lido(tmp_path / "a") == _lido(tmp_path / "b")
    assert a[2].count("/") >= 3 and b[2] == ""                 # simples escreve as linhas; --quiet não escreve nada


def test_callback_de_progresso_recebe_inicio_e_um_evento_por_caso(tmp_path):
    if not EXEMPLO.is_file():
        pytest.skip("estudo-exemplo ausente nesta edição")
    eventos = []
    ex = E.rodar_estudo(EXEMPLO, tmp_path / "s", progresso=lambda *a: eventos.append(a))
    assert ex.codigo == 0
    assert eventos[0][:3] == ("inicio", 0, 3) and [e[0] for e in eventos[1:]] == ["caso"] * 3
    assert [e[1] for e in eventos[1:]] == [1, 2, 3] and all(e[4] is None for e in eventos[1:])


def test_ajuda_lista_a_opcao_nos_dois_subcomandos():
    ajuda = {}
    for acao in ("run", "lote"):
        buf = io.StringIO()
        sub = [a for a in _parser()._subparsers._group_actions[0].choices["estudo"]._subparsers._group_actions[0].choices.items()
               if a[0] == acao][0][1]
        sub.print_help(buf)
        ajuda[acao] = buf.getvalue()
    for texto in ajuda.values():
        assert "--progresso" in texto and "auto,rich,simples" in texto.replace(" ", "").replace("{", "").replace("}", "") or "{auto,rich,simples}" in texto
