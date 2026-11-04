"""O que é importado dentro de função tem de ser declarado ao empacotador.

O PyInstaller descobre dependências lendo os `import` do topo dos módulos. Um
import escrito dentro de uma função — recurso legítimo, usado aqui para não
carregar módulo pesado antes da hora — é invisível para ele: o programa roda pelo
código-fonte e quebra no executável, na hora em que o usuário clica no botão.

Este teste percorre o pacote, encontra os imports internos de módulos do próprio
programa e exige que cada um esteja declarado nas duas listas de empacotamento,
`Triton.spec` e `build_exe.py`. Quem esquecer, descobre aqui, e não depois de
gerar o instalador.
"""
import ast
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACOTE = os.path.join(RAIZ, "triton")

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
            if isinstance(interno, ast.ImportFrom) and (interno.module or "").startswith("triton."):
                achados.add(interno.module)
            elif isinstance(interno, ast.Import):
                for alias in interno.names:
                    if alias.name.startswith("triton."):
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
            if isinstance(no, ast.ImportFrom) and (no.module or "").startswith("triton."):
                alcancaveis.add(no.module)
            elif isinstance(no, ast.Import):
                for alias in no.names:
                    if alias.name.startswith("triton."):
                        alcancaveis.add(alias.name)
    # Um pacote é alcançável quando um módulo dele é importado no topo.
    pacotes = {m.rsplit(".", 1)[0] for m in alcancaveis if "." in m}
    return alcancaveis | pacotes


def _declarados(caminho):
    texto = open(caminho, encoding="utf-8").read()
    nomes = set(re.findall(r"['\"](triton\.[\w.]+)['\"]", texto))
    # Caminhos de arquivo (triton.ico, triton.data) não são módulos.
    return {n for n in nomes if not re.search(r"\.(ico|png|json|csv|txt|ui)$", n)}


def test_import_dentro_de_funcao_esta_declarado_ao_empacotador():
    interno = _importados_em_funcao_no_pacote() - _importados_no_topo() - DISPENSADOS
    spec = _declarados(os.path.join(RAIZ, "Triton.spec"))
    script = _declarados(os.path.join(RAIZ, "build_exe.py"))
    faltam_no_spec = sorted(interno - spec)
    faltam_no_script = sorted(interno - script)
    assert not faltam_no_spec, ("ausentes em Triton.spec (hiddenimports): " + ", ".join(faltam_no_spec))
    assert not faltam_no_script, ("ausentes em build_exe.py (hidden_imports): " + ", ".join(faltam_no_script))


def test_as_duas_listas_de_empacotamento_dizem_o_mesmo():
    """Duas listas que divergem produzem dois executáveis diferentes."""
    assert _declarados(os.path.join(RAIZ, "Triton.spec")) == _declarados(os.path.join(RAIZ, "build_exe.py"))


def _build_exe():
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_exe", os.path.join(RAIZ, "build_exe.py"))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _criar_partes(pasta, b, unico=False):
    pasta.mkdir(parents=True, exist_ok=True)
    for modelo in b.modelos_climbra():
        (pasta / f"climbra_{modelo}.db").write_bytes(b"SQLite")
    (pasta / "climbra_partes.json").write_text("{}", encoding="utf-8")
    if unico:
        (pasta / "climbra.db").write_bytes(b"SQLite")


def test_a_edicao_brasil_nao_sai_sem_a_base_climbra(tmp_path):
    """Sem os bancos data/climbra_<modelo>.db (nem o climbra.db nem os CSV), a Edição Brasil é recusada.

    Antes, o PyInstaller copiava a pasta `data` sem a base e o instalador saía sem as 652 cidades,
    sem aviso algum. Com uma parte faltando, o pacote também é recusado.
    """
    b = _build_exe()
    assert len(b.modelos_climbra()) == 19
    assert b.garantir_base_climatica(tmp_path) is False
    _criar_partes(tmp_path / "data", b)
    assert b.garantir_base_climatica(tmp_path) is True
    (tmp_path / "data" / "climbra_KACE.db").unlink()
    assert b.garantir_base_climatica(tmp_path) is False


def test_o_instalador_confere_a_base_climbra_no_pacote(tmp_path):
    b = _build_exe()
    faltam = [os.path.normpath(f) for f in b.verificar_pasta_para_instalador(tmp_path)]
    for modelo in b.modelos_climbra():
        assert os.path.join("dist", "Triton", "_internal", "data", f"climbra_{modelo}.db") in faltam
    # E a pasta `data` inteira entra no executável, levando os bancos junto.
    assert "('data', 'data')" in open(os.path.join(RAIZ, "Triton.spec"), encoding="utf-8").read()
    # Fora da Brasil, a base não é exigida.
    assert not [f for f in b.verificar_pasta_para_instalador(tmp_path, "int") if "climbra" in f]


def test_a_edicao_internacional_sai_sem_a_base_climbra(tmp_path):
    """A CLIMBra cobre só o Brasil: as partes vão na BRL e saem do pacote da INT e da IBE."""
    b = _build_exe()
    for edicao in ("brl", "int", "ibe"):
        _criar_partes(tmp_path / edicao / "_internal" / "data", b, unico=True)
        b.remover_base_climatica_fora_da_brl(tmp_path / edicao, edicao)
    brl = tmp_path / "brl" / "_internal" / "data"
    assert all(p.exists() for p in b.partes_da_base_climatica(tmp_path / "brl" / "_internal"))
    assert not (brl / "climbra.db").exists()          # as partes bastam: o banco único seria o mesmo conteúdo em dobro
    for edicao in ("int", "ibe"):
        sobra = [p.name for p in (tmp_path / edicao / "_internal" / "data").iterdir() if p.name.startswith("climbra")]
        assert sobra == [], sobra


def test_o_banco_unico_antigo_fica_se_as_partes_estao_incompletas(tmp_path):
    b = _build_exe()
    _criar_partes(tmp_path / "_internal" / "data", b, unico=True)
    (tmp_path / "_internal" / "data" / "climbra_KACE.db").unlink()
    b.remover_base_climatica_fora_da_brl(tmp_path, "brl")
    assert (tmp_path / "_internal" / "data" / "climbra.db").exists()


def test_a_pasta_de_tarifas_so_vai_na_brl_e_sem_material_de_terceiros(tmp_path):
    """A transcrição acompanha a Brasil; os documentos de terceiros e a entrada não vão em nenhuma edição."""
    b = _build_exe()
    for edicao in ("brl", "int"):
        for sub in ("fontes", "entrada", "tarifas_fontes.db", "transcricoes"):
            p = tmp_path / edicao / "_internal" / "tarifas" / sub
            if sub == "transcricoes":
                p = p / "doc.json"
            elif sub.endswith(".db"):
                pass
            else:
                p = p / "doc.pdf"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"%PDF")
        manual = tmp_path / edicao / "_internal" / "additional_material" / "documentation" / "Manual-Netuno-4.pdf"
        manual.parent.mkdir(parents=True)
        manual.write_bytes(b"%PDF")
        b.remover_tarifas_fora_da_brl(tmp_path / edicao, edicao)
    brl = tmp_path / "brl" / "_internal"
    assert (brl / "tarifas" / "transcricoes" / "doc.json").exists()
    for fora in ("fontes", "entrada", "tarifas_fontes.db"):
        assert not (brl / "tarifas" / fora).exists(), fora
    assert not (brl / "additional_material" / "documentation").exists()
    assert not (tmp_path / "int" / "_internal" / "tarifas").exists()


def test_o_pacote_nao_copia_o_que_nao_pode_ir(tmp_path):
    """`data` e `tarifas` entram item a item: nada de saídas do Netuno 4, banco antigo ou documentos de terceiros."""
    b = _build_exe()
    for rel in ("data/simulation_outputs/x.csv", "data/brazilSHP/m.shp", "data/portugal/fonte.nc", "data/languages/es.json",
                "data/climbra.db", "data/climbra_KACE.db", "data/climbra_partes.json", "data/portugal_eobs.db",
                "tarifas/fontes/doc.pdf", "tarifas/entrada/x.pdf", "tarifas/tarifas_fontes.db", "tarifas/transcricoes/a.json",
                "tarifas/catalogo_tarifas_auditado_652.csv", "additional_material/documentation/manual.pdf",
                "additional_material/cad_bim/a.dxf"):
        arquivo = tmp_path / rel
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_bytes(b"x")
    por_edicao = {e: {o for o, _d in b.entradas_do_pacote(tmp_path, e)} for e in ("brl", "int", "ibe")}
    for e, itens in por_edicao.items():
        for proibido in ("data/simulation_outputs", "data/brazilSHP", "data/portugal", "data/climbra.db",
                         "tarifas/fontes", "tarifas/entrada", "tarifas/tarifas_fontes.db", "additional_material/documentation"):
            assert proibido not in itens, (e, proibido)
        assert "data/languages" in itens and "additional_material/cad_bim" in itens
    assert {"data/climbra_KACE.db", "data/climbra_partes.json", "tarifas/transcricoes"} <= por_edicao["brl"]
    assert "data/portugal_eobs.db" not in por_edicao["brl"] and "data/portugal_eobs.db" in por_edicao["ibe"]
    for e in ("int", "ibe"):
        assert not [i for i in por_edicao[e] if i.startswith(("data/climbra", "tarifas"))], e
    assert "data/portugal_eobs.db" not in por_edicao["int"]


def test_so_a_internacional_leva_o_manual_ingles(tmp_path):
    """`manual/en` é da Internacional; a Brasil e a Portugal não o procuram nem o empacotam."""
    b = _build_exe()
    for rel in ("manual/Manual-Triton.pdf", "manual/en/Triton-User-Manual.pdf"):
        arquivo = tmp_path / rel
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_bytes(b"%PDF")
    por_edicao = {e: {o for o, _d in b.entradas_do_pacote(tmp_path, e)} for e in ("brl", "int", "ibe")}
    assert "manual/en/Triton-User-Manual.pdf" in por_edicao["int"]
    for e in ("brl", "ibe"):
        assert not [i for i in por_edicao[e] if i.startswith("manual/en")], e
        assert "manual/Manual-Triton.pdf" in por_edicao[e]
    # a conferência do instalador também só espera o manual inglês na Internacional
    esperado = {e: [f for f in b.verificar_pasta_para_instalador(tmp_path, e) if "Triton-User-Manual" in f]
                for e in ("brl", "int", "ibe")}
    assert esperado["int"] and not esperado["brl"] and not esperado["ibe"]


def test_os_modulos_dos_subpacotes_de_core_chegam_ao_executavel():
    """Os «shims» da raiz de core/ trocam a entrada em sys.modules; o PyInstaller só enxerga o import estático.

    Cada shim precisa de um `from triton.core.<subpacote>.<modulo> import ...` de topo, e as duas listas de
    empacotamento precisam coletar todo `triton.core` (que é pacote de espaço de nomes, sem __init__).
    """
    core = os.path.join(PACOTE, "core")
    sem_import_estatico = []
    for arquivo in sorted(os.listdir(core)):
        if not arquivo.endswith(".py"):
            continue
        texto = open(os.path.join(core, arquivo), encoding="utf-8").read()
        if "sys.modules[__name__]" not in texto:
            continue
        arvore = ast.parse(texto)
        alvos = [no.module for no in arvore.body
                 if isinstance(no, ast.ImportFrom) and (no.module or "").count(".") >= 3
                 and no.module.startswith("triton.core.")]
        if not alvos:
            sem_import_estatico.append(arquivo)
    assert not sem_import_estatico, ("shims sem import estático do módulo canônico: " + ", ".join(sem_import_estatico))
    assert "collect_submodules('triton.core')" in open(os.path.join(RAIZ, "Triton.spec"), encoding="utf-8").read()
    assert '"--collect-submodules", "triton.core"' in open(os.path.join(RAIZ, "build_exe.py"), encoding="utf-8").read()
