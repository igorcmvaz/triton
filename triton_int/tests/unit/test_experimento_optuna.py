# -*- coding: utf-8 -*-
"""``scripts/experimento_optuna.py`` (raiz do monorepo): ``--help``, a mensagem do extra ausente e a importação, tudo SEM optuna.

O experimento em si (grade × busca bayesiana) não roda aqui: ele precisa do extra «otimizacao», leva minutos e é só de
desenvolvimento. O optuna é simulado como ausente (``sys.modules["optuna"] = None``), de modo que o teste vale com ou sem o
pacote instalado.
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "experimento_optuna.py"
pytestmark = pytest.mark.skipif(not SCRIPT.is_file(), reason="o script fica na raiz do monorepo, fora da edição")

SEM_OPTUNA = (
    "import runpy, sys\n"
    "sys.modules['optuna'] = None\n"            # «import optuna» passa a levantar ImportError
    "sys.argv = [sys.argv[1]] + sys.argv[2:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)


def _rodar(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=120)


def _rodar_sem_optuna(*args):
    return subprocess.run([sys.executable, "-c", SEM_OPTUNA, str(SCRIPT), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=120)


def test_help_lista_as_opcoes():
    r = _rodar("--help")
    assert r.returncode == 0, r.stderr
    for opcao in ("--edicao", "--experimento", "--semente", "--n-sementes", "--tentativas-1d", "--tentativas-2d",
                  "--tentativas-nsga", "--tolerancia-pct", "--json", "--aguardar-cpu"):
        assert opcao in r.stdout
    for nome in ("1d", "1da", "2d", "nsga"):
        assert nome in r.stdout


@pytest.mark.parametrize("edicao", ["int", "brl", "ibe"])
def test_sem_o_extra_a_mensagem_diz_o_pacote_o_extra_e_o_comando(edicao):
    r = _rodar_sem_optuna("--edicao", edicao, "--experimento", "1d")
    assert r.returncode != 0
    assert "optuna" in r.stderr and "otimizacao" in r.stderr
    assert f'pip install "triton-{edicao}[otimizacao]"' in r.stderr
    assert "Traceback" not in r.stderr          # mensagem clara, não um ModuleNotFoundError solto


def test_o_modulo_importa_sem_optuna_e_nao_o_importa_no_topo():
    codigo = (
        "import importlib.util, sys\n"
        "sys.modules['optuna'] = None\n"
        f"spec = importlib.util.spec_from_file_location('experimento_optuna', {str(SCRIPT)!r})\n"
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
        "assert callable(m.main) and callable(m.montar_parser) and callable(m.exigir_optuna)\n"
        "assert sys.modules['optuna'] is None\n"
        "print('ok')\n"
    )
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=120)
    assert r.returncode == 0, r.stderr
    assert "ok" in r.stdout
    fonte = SCRIPT.read_text(encoding="utf-8")
    assert not re.search(r"^(import|from)\s+optuna\b", fonte, re.M), "o optuna só entra por triton.core._opcional"
    assert "_opcional" in fonte


def test_o_optuna_nao_esta_nos_arquivos_de_empacotamento():
    """O extra é só de desenvolvimento: nada de optuna no instalador, nos requisitos de execução ou nos hiddenimports."""
    base = SCRIPT.parents[1]
    for pasta in sorted(base.glob("triton_*")):
        for nome in ("requirements.txt", "Triton.spec", "build_exe.py"):
            arq = pasta / nome
            if arq.is_file():
                assert "optuna" not in arq.read_text(encoding="utf-8", errors="replace").lower(), f"{pasta.name}/{nome}"
