"""O que o instalador oferece e mostra.

A base CLIMBra vai compilada dentro do programa (data/climbra.db). Os CSV de origem,
cerca de 6,5 GB, só servem para recompilar o banco: o instalador não deve oferecê-los.
"""

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ISS = (RAIZ / "setup_script.iss").read_text(encoding="utf-8")


def test_o_instalador_nao_oferece_os_csv_da_base_climatica():
    assert "climbra_data" not in ISS
    assert "Triton future files" not in ISS
    assert "{src}" not in ISS  # nada copiado de fora do instalador
    assert 'Name: "clima"' not in ISS


def test_a_base_compilada_e_exigida_antes_de_gerar_o_instalador():
    import build_exe

    faltando = build_exe.verificar_pasta_para_instalador(Path("/inexistente"))
    assert any("climbra.db" in item for item in faltando)


def test_a_licenca_mostrada_e_o_texto_integral_da_gpl_v3():
    assert "LicenseFile=LICENSE" in ISS
    texto = (RAIZ / "LICENSE").read_text(encoding="utf-8")
    assert "GNU GENERAL PUBLIC LICENSE" in texto and "Version 3, 29 June 2007" in texto
    assert "END OF TERMS AND CONDITIONS" in texto


def test_os_avisos_de_terceiros_vao_com_o_programa_e_cobrem_as_dependencias():
    import subprocess
    import sys

    assert 'Source: "infos_licenses\\AVISOS_DE_TERCEIROS.txt"; DestDir: "{app}"' in ISS
    avisos = (RAIZ / "infos_licenses" / "AVISOS_DE_TERCEIROS.txt").read_text(encoding="utf-8")
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in avisos  # Qt
    assert "PYTHON SOFTWARE FOUNDATION LICENSE" in avisos.upper()
    for componente in ("PySide6", "numpy", "matplotlib", "three.js", "CLIMBra"):
        assert componente in avisos
    res = subprocess.run([sys.executable, str(RAIZ / "scripts" / "gerar_avisos_de_terceiros.py"), "--conferir"],
                         capture_output=True, text=True)
    assert res.returncode == 0, res.stdout


def test_a_licenca_e_instalada_com_o_programa():
    assert 'Source: "Licence.txt"; DestDir: "{app}"; DestName: "LICENSE.txt"' in ISS
    aviso = (RAIZ / "Licence.txt").read_text(encoding="utf-8")
    assert "SPDX-License-Identifier: GPL-3.0-or-later" in aviso
    assert "END OF TERMS AND CONDITIONS" in aviso
