"""O que é importado dentro de função tem de ser declarado ao empacotador.

O PyInstaller descobre dependências lendo os `import` do topo dos módulos. Um
import escrito dentro de uma função — recurso legítimo, usado aqui para não
carregar módulo pesado antes da hora — é invisível para ele: o programa roda pelo
código-fonte e quebra no executável, na hora em que o usuário clica no botão.

Este teste percorre o pacote, encontra os imports internos de módulos do próprio
programa e exige que cada um esteja declarado nas duas listas de empacotamento,
`Netuno.spec` e `build_exe.py`. Quem esquecer, descobre aqui, e não depois de
gerar o instalador.
"""
import ast
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACOTE = os.path.join(RAIZ, "netuno")

#: Importado dentro de função, mas por módulo que o empacotador já alcança pelo
#: topo de outro arquivo; declarar de novo não faria diferença.
DISPENSADOS = set()


def _modulos_importados_dentro_de_funcao(caminho):
    arvore = ast.parse(open(caminho, encoding="utf-8").read(), filename=caminho)
    achados = set()
    for no in ast.walk(arvore):
        if not isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for interno in ast.walk(no):
            if isinstance(interno, ast.ImportFrom) and (interno.module or "").startswith("netuno."):
                achados.add(interno.module)
            elif isinstance(interno, ast.Import):
                for alias in interno.names:
                    if alias.name.startswith("netuno."):
                        achados.add(alias.name)
    return achados


def _importados_em_funcao_no_pacote():
    achados = set()
    for pasta, _, arquivos in os.walk(PACOTE):
        if "__pycache__" in pasta:
            continue
        for arquivo in arquivos:
            if arquivo.endswith(".py"):
                achados |= _modulos_importados_dentro_de_funcao(os.path.join(pasta, arquivo))
    return achados


def _importados_no_topo():
    """Módulos alcançáveis pelo empacotador sem declaração, por import de topo.

    Inclui `main.py`, que é o ponto de entrada do executável, e trata pacote como
    alcançável quando um módulo dele é importado no topo de algum arquivo.
    """
    alcancaveis = set()
    arquivos_a_ler = [os.path.join(RAIZ, "main.py")]
    for pasta, _, arquivos in os.walk(PACOTE):
        if "__pycache__" in pasta:
            continue
        arquivos_a_ler += [os.path.join(pasta, a) for a in arquivos if a.endswith(".py")]
    for caminho in arquivos_a_ler:
        arvore = ast.parse(open(caminho, encoding="utf-8").read(), filename=caminho)
        for no in arvore.body:                           # só o topo do módulo
            if isinstance(no, ast.ImportFrom) and (no.module or "").startswith("netuno."):
                alcancaveis.add(no.module)
            elif isinstance(no, ast.Import):
                for alias in no.names:
                    if alias.name.startswith("netuno."):
                        alcancaveis.add(alias.name)
    # Um pacote é alcançável quando um módulo dele é importado no topo.
    pacotes = {m.rsplit(".", 1)[0] for m in alcancaveis if "." in m}
    return alcancaveis | pacotes


def _declarados(caminho):
    texto = open(caminho, encoding="utf-8").read()
    nomes = set(re.findall(r"['\"](netuno\.[\w.]+)['\"]", texto))
    # Caminhos de arquivo (netuno.ico, netuno.data) não são módulos.
    return {n for n in nomes if not re.search(r"\.(ico|png|json|csv|txt|ui)$", n)}


def test_import_dentro_de_funcao_esta_declarado_ao_empacotador():
    interno = _importados_em_funcao_no_pacote() - _importados_no_topo() - DISPENSADOS
    spec = _declarados(os.path.join(RAIZ, "Netuno.spec"))
    script = _declarados(os.path.join(RAIZ, "build_exe.py"))
    faltam_no_spec = sorted(interno - spec)
    faltam_no_script = sorted(interno - script)
    assert not faltam_no_spec, ("ausentes em Netuno.spec (hiddenimports): " + ", ".join(faltam_no_spec))
    assert not faltam_no_script, ("ausentes em build_exe.py (hidden_imports): " + ", ".join(faltam_no_script))


def test_as_duas_listas_de_empacotamento_dizem_o_mesmo():
    """Duas listas que divergem produzem dois executáveis diferentes."""
    assert _declarados(os.path.join(RAIZ, "Netuno.spec")) == _declarados(os.path.join(RAIZ, "build_exe.py"))


def _build_exe():
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_exe", os.path.join(RAIZ, "build_exe.py"))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_a_edicao_brasil_nao_sai_sem_a_base_climbra(tmp_path):
    """Sem data/climbra.db nem os CSV, a compilação da Edição Brasil é recusada.

    Antes, o PyInstaller copiava a pasta `data` sem o banco e o instalador saía
    sem as 652 cidades, sem aviso algum.
    """
    b = _build_exe()
    assert b.garantir_base_climatica(tmp_path) is False
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "climbra.db").write_bytes(b"SQLite")
    assert b.garantir_base_climatica(tmp_path) is True


def test_o_instalador_confere_a_base_climbra_no_pacote(tmp_path):
    b = _build_exe()
    faltam = b.verificar_pasta_para_instalador(tmp_path)
    assert os.path.join("dist", "Netuno", "_internal", "data", "climbra.db") in [os.path.normpath(f) for f in faltam]
    # E a pasta `data` inteira entra no executável, levando o banco junto.
    assert "('data', 'data')" in open(os.path.join(RAIZ, "Netuno.spec"), encoding="utf-8").read()
