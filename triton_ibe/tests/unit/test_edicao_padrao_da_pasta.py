"""Sem ``TRITON_EDITION``, a CLI e o comando ``triton`` rodam como a edição da pasta (INT em INT, IBE em IBE).

Antes, ``get_current_edition`` caía em BRL, e ``python -m triton.cli`` numa pasta da INT ou da IBE
partia dos padrões do Brasil. O marcador ``triton/data/edicao_padrao.txt`` (um por edição; a BRL não
tem, e vale BRL) resolve; a variável de ambiente continua mandando.
"""
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PASTA = {"triton_brl": "BRL", "triton_int": "INT", "triton_ibe": "IBE"}.get(RAIZ.name.lower(), "BRL")


def _rodar(codigo: str, ambiente: dict | None = None) -> str:
    env = {k: v for k, v in os.environ.items() if k != "TRITON_EDITION"}
    env.update(ambiente or {})
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, "-c", codigo], cwd=str(RAIZ), env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=120)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def test_sem_variavel_vale_a_edicao_da_pasta():
    assert _rodar("from triton.core.edition import get_current_edition as g; print(g())") == PASTA


def test_a_variavel_de_ambiente_continua_mandando():
    saida = _rodar("from triton.core.edition import get_current_edition as g; print(g())", {"TRITON_EDITION": "BRL"})
    assert saida == "BRL"


def test_a_cli_sem_variavel_parte_dos_padroes_da_edicao():
    codigo = ("from triton.core.edition import configuracao_da_edicao as c; k=c(); "
              "print(k.tariff_city_name, k.elec_tariff, k.climate_city_name)")
    saida = _rodar(codigo)
    if PASTA == "BRL":
        assert saida.startswith("Florian")
    else:
        assert saida.startswith("CUSTOM 0.0")
        assert "Florian" not in saida


def test_o_marcador_existe_nas_edicoes_que_nao_sao_a_brasil():
    marcador = RAIZ / "triton" / "data" / "edicao_padrao.txt"
    if PASTA == "BRL":
        assert not marcador.exists()
    else:
        assert marcador.read_text(encoding="utf-8").strip() == PASTA


def test_o_instalador_leva_o_marcador_e_o_build_o_regrava(tmp_path):
    """``triton/data`` entra inteira no pacote (e o marcador com ela); o build regrava o da edição compilada."""
    import importlib.util

    import pytest
    if not (RAIZ / "build_exe.py").is_file():
        pytest.skip("build_exe.py não faz parte do repositório (só o necessário para a linha de comando)")
    spec = importlib.util.spec_from_file_location("build_exe_da_pasta", RAIZ / "build_exe.py")
    build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build)
    for edicao in ("brl", "int", "ibe"):
        assert ("triton/data", "triton/data") in build.entradas_do_pacote(RAIZ, edicao)
    (tmp_path / "triton" / "data").mkdir(parents=True)
    build.gravar_marcador_da_edicao(tmp_path, "ibe")
    assert (tmp_path / "triton" / "data" / "edicao_padrao.txt").read_text(encoding="utf-8").strip() == "IBE"
    build.gravar_marcador_da_edicao(tmp_path, "brl")
    assert not (tmp_path / "triton" / "data" / "edicao_padrao.txt").exists()
