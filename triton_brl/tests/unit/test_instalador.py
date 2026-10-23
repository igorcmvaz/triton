"""O que o instalador oferece e mostra.

A base CLIMBra vai compilada dentro do programa (data/climbra_<modelo>.db). Os CSV de origem,
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
    assert any("climbra_" in item for item in faltando)


def test_a_licenca_mostrada_e_o_texto_do_codigo_fonte_academico():
    assert "LicenseFile=LICENSE.md" in ISS
    texto = (RAIZ / "LICENSE.md").read_text(encoding="utf-8")
    assert "CÓDIGO FONTE DISPONÍVEL PARA FINS ACADÊMICOS" in texto
    assert "ACADEMIC SOURCE-AVAILABLE" in texto
    assert "GNU GENERAL PUBLIC LICENSE" not in texto
    assert "Triton 5" not in texto and "TRITON 5" not in texto


def test_os_avisos_de_terceiros_vao_com_o_programa_e_cobrem_as_dependencias():
    assert 'Source: "infos_licenses\\AVISOS_DE_TERCEIROS.txt"; DestDir: "{app}"' in ISS
    avisos = (RAIZ / "infos_licenses" / "AVISOS_DE_TERCEIROS.txt").read_text(encoding="utf-8")
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in avisos  # Qt
    assert "PYTHON SOFTWARE FOUNDATION LICENSE" in avisos.upper()
    for componente in ("PySide6", "numpy", "matplotlib", "three.js"):
        assert componente in avisos
    # A atribuição de dados vale só para a edição que leva o dado.
    edicao = RAIZ.name.rsplit("_", 1)[-1].upper()
    assert ("CLIMBra" in avisos) == (edicao == "BRL")
    assert ("E-OBS" in avisos) == (edicao == "IBE")


def test_a_licenca_e_instalada_com_o_programa():
    assert 'Source: "LICENSE.md"; DestDir: "{app}"' in ISS
    assert (RAIZ / "LICENSE.md").is_file()
    assert not (RAIZ / "LICENSE").exists() and not (RAIZ / "Licence.txt").exists()


def test_o_instalador_nao_exclui_todos_os_bancos_sqlite():
    """`*.db` nas exclusões tiraria do instalador a base CLIMBra e a E-OBS; só os bancos de terceiros saem."""
    assert "*.db" not in ISS.replace("climbra_*.db", "")
    assert "*.sqlite" not in ISS
    assert "tarifas_fontes.db" in ISS and "tarifas_portugal_fontes.db" in ISS
    # a base climática é excluída das edições a que não pertence, e só delas
    linhas = {l.split()[2]: l for l in ISS.splitlines() if "#define ExcluirBases" in l}
    assert len(linhas) == 3
    brl = [l for l in ISS.splitlines() if "#define ExcluirBases" in l][2]
    assert "climbra_*.db" not in brl and "portugal_eobs.db" in brl


def test_os_nomes_do_instalador_batem_com_o_build():
    import build_exe

    for edicao, (_script, nome) in build_exe.EDICOES.items():
        assert f'"{nome}.exe"' in ISS, f"{nome}.exe não está no setup_script.iss ({edicao})"
        assert f'"dist\\{nome}"' in ISS, f"dist\\{nome} não está no setup_script.iss ({edicao})"
        prefixo = {"int": "Triton_INT_Setup_", "ibe": "Triton_IBE_Setup_"}.get(edicao, "Triton_Setup_")
        assert f'"{prefixo}"' in ISS


def test_os_textos_do_instalador_acompanham_o_estado_de_lancamento():
    """O pyproject é a fonte do estado: o instalador não pode falar em «beta» se ele declara Production/Stable."""
    beta = "Development Status :: 4 - Beta" in (RAIZ / "pyproject.toml").read_text(encoding="utf-8")
    for nome in ("info_before.txt", "info_after.txt"):
        texto = (RAIZ / "infos_licenses" / nome).read_text(encoding="utf-8-sig").lower()
        assert ("beta" in texto) == beta, nome
