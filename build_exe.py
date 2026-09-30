"""
Script de Compilação do Netuno 5 em Executável e Instalador Windows.
Suporta PyInstaller (standalone onedir / onefile) e Inno Setup 6.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_icon(base_dir: Path) -> Path | None:
    """Busca o ícone oficial da aplicação nos locais padrão."""
    candidates = [
        base_dir / "icons" / "netuno5.ico",
        base_dir / "icons" / "icon.ico",
        base_dir / "icons" / "netuno.ico",
        base_dir / "icon.ico",
        base_dir / "netuno.ico",
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def find_inno_compiler() -> Path | None:
    """Localiza o compilador ISCC do Inno Setup no sistema."""
    iscc_path = shutil.which("ISCC")
    if iscc_path:
        return Path(iscc_path)

    known_paths = [
        Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
        Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
        Path(r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe"),
        Path(r"C:\Program Files\Inno Setup 5\ISCC.exe"),
    ]
    for p in known_paths:
        if p.is_file():
            return p
    return None


def clean_build_dirs(base_dir: Path):
    """Remove pastas de compilações anteriores."""
    for folder in ["build", "dist"]:
        target = base_dir / folder
        if target.exists():
            print(f"[*] Limpando diretório {folder}/...")
            try:
                shutil.rmtree(target, ignore_errors=True)
            except Exception as exc:
                print(f"[!] Aviso ao limpar {folder}/: {exc}")


def build_manual(base_dir: Path) -> bool:
    """Monta o manual e compõe o PDF antes de empacotar.

    O PDF é derivado: sai do Markdown, que sai dos capítulos, das tabelas e das
    figuras geradas rodando o próprio programa. Gerá-lo aqui é o que garante que
    o manual embarcado no instalador corresponde à versão empacotada, em vez de
    ser um arquivo antigo que alguém esqueceu de atualizar.
    """
    print("\n[*] Montando o manual...")
    etapas = [
        ("tabelas", "manual/gerar_tabelas.py"),
        ("figuras", "manual/gerar_figuras.py"),
        ("figuras extras", "manual/gerar_figuras_extra.py"),
        ("figuras da chuva", "manual/gerar_figuras_chuva.py"),
        ("figuras da decisão", "manual/gerar_figuras_decisao.py"),
        ("figuras do programa", "manual/gerar_figuras_do_programa.py"),
        ("desenhos", "manual/gerar_desenhos.py"),
        ("desenho do sistema", "manual/gerar_desenho_sistema.py"),
        ("desenhos do método", "manual/gerar_desenhos_metodo.py"),
        ("esquemas", "manual/gerar_desenhos_esquemas.py"),
        ("infográficos", "manual/gerar_infograficos.py"),
        ("infográficos 2", "manual/gerar_infograficos2.py"),
        ("apêndices", "manual/gerar_apendices.py"),
        ("casos", "manual/gerar_casos.py"),
        ("montagem", "manual/gerar.py"),
        ("changelog", "manual/gerar_changelog.py"),
        ("capas", "manual/gerar_capas.py"),
        ("PDF", "manual/gerar_pdf.py"),
        ("mini manuais", "manual/gerar_mini_manuais.py"),
        ("site de documentação", "manual/gerar_site.py"),
    ]
    for rotulo, script in etapas:
        caminho = base_dir / script
        if not caminho.exists():
            print(f"    {rotulo}: {script} não encontrado; pulando")
            continue
        res = subprocess.run([sys.executable, str(caminho)], cwd=base_dir)
        if res.returncode != 0:
            print(f"[ERRO] Falha ao gerar {rotulo}.")
            return False
        print(f"    {rotulo}: ok")
    return True


def build_pyinstaller(args, base_dir: Path) -> bool:
    """Executa a compilação do executável com PyInstaller."""
    print("\n=======================================================")
    from netuno import __version__
    print(f"  Iniciando Compilação PyInstaller — Netuno {__version__}")
    print("=======================================================")

    try:
        import PyInstaller
    except ImportError:
        print("[*] PyInstaller não encontrado. Instalando automaticamente...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "-y",
        f"--name={args.name}",
    ]

    if args.onefile:
        cmd.append("--onefile")
        print("[+] Modo: Executável único (--onefile)")
    else:
        cmd.append("--onedir")
        print("[+] Modo: Diretório standalone (--onedir)")

    if args.console:
        cmd.append("--console")
        print("[+] Janela de console: ATIVADA (para depuração)")
    else:
        cmd.append("--noconsole")
        print("[+] Janela de console: DESATIVADA (modo produção)")

    # Localização do ícone
    icon_path = find_icon(base_dir)
    if icon_path:
        cmd.append(f"--icon={icon_path}")
        print(f"[+] Ícone configurado: {icon_path.relative_to(base_dir)}")
    else:
        print("[!] Nenhum ícone .ico encontrado nos diretórios padrão.")

    # Inclusão de pastas de dados e templates
    data_folders = [
        ("data", "data"),
        ("templates", "templates"),
        ("tarifas", "tarifas"),
        ("icons", "icons"),
        ("netuno/data", "netuno/data"),
        ("additional_material", "additional_material"),
        # O manual promete os casos e os estudos de exemplo na pasta do
        # programa, e o menu Ajuda abre o PDF e o relatório de verificação:
        # nenhum dos quatro entrava no executável.
        ("manual/casos", "casos"),
        ("examples", "exemplos"),
        ("docs", "docs"),
        ("manual/Manual-Netuno-5.pdf", "manual"),
        # Os sete volumes avulsos, para mandar só uma parte do manual.
        ("manual/mini", "manual/mini"),
        # Manual interativo offline (HTML/JS/CSS)
        ("manual/site", "manual/site"),
    ]

    for src_rel, dst_rel in data_folders:
        src_path = base_dir / src_rel
        if src_path.exists():
            sep = ";" if sys.platform.startswith("win") else ":"
            cmd.append(f"--add-data={src_rel}{sep}{dst_rel}")
            print(f"[+] Incluindo assets: {src_rel} -> {dst_rel}")

    # Hidden imports para garantir que submódulos dinâmicos sejam incluídos
    hidden_imports = [
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "matplotlib.backends.backend_qtagg",
        "numpy",
        "pandas",
        "openpyxl",
        "reportlab",
        "ezdxf",
        "netuno.core.mcdm_methods",
        "netuno.core.environmental_sync",
        "netuno.core.esg_certifications",
        "netuno.core.comprimento_de_serie",
        "netuno.core.demanda_estocastica",
        "netuno.ui.dialogs.dialog_comprimento_de_serie",
        "netuno.core.excel_scenarios",
        "netuno.ui.tab_economic_global_optimizer",
        "netuno.core.edition",
        # Planta 3D, esquema e volumetria: parte é importada só dentro de funções.
        "netuno.core.component_geometry",
        "netuno.core.pipe_network",
        "netuno.core.plant_3d",
        "netuno.core.schematic_3d",
        "netuno.core.study_layout",
        "netuno.core.exportar_tudo",
        "netuno.core.volumetry",
        "netuno.core.volumetry_export",
        "netuno.ui.volumetry_view",
        # Volumetria WebGL (three.js) na aba; o pacote do visualizador e o céu
        # vão em netuno/data/volumetria.
        "netuno.ui.volumetry_web",
        "PySide6.QtWebEngineWidgets",
        "PySide6.QtWebEngineCore",
        "netuno.ui.dialogs.pipe_runs_dialog",
        "PySide6.QtSvg",
        "ezdxf.render.forms",
    ]
    for hi in hidden_imports:
        cmd.append(f"--hidden-import={hi}")

    main_script = getattr(args, "main_script", None) or (base_dir / "main.py")
    cmd.append(str(main_script))

    print(f"\n[*] Executando comando de compilação...")
    res = subprocess.run(cmd, cwd=base_dir)
    if res.returncode != 0:
        print("\n[ERRO] Falha na compilação com PyInstaller.")
        return False

    # Pós-processamento de limpeza em dist/
    dist_dir = base_dir / "dist" / args.name
    if dist_dir.exists():
        # As saidas de referencia do Netuno 4 sao 514 MB de insumo de teste, e
        # nao servem a quem instala o programa. O PyInstaller as copia junto com
        # a pasta `data`, e por isso elas param em `_internal/data`: a limpeza
        # procurava so na raiz e em `_internal`, e nunca encontrava nada.
        for base in [dist_dir, dist_dir / "_internal", dist_dir / "data",
                     dist_dir / "_internal" / "data"]:
            sim_outputs = base / "simulation_outputs"
            if sim_outputs.exists():
                shutil.rmtree(sim_outputs, ignore_errors=True)
                print(f"[*] Removido do pacote: {sim_outputs.relative_to(base_dir)}")
            temp_dados = base / "data" / "Dados.txt"
            if temp_dados.exists():
                try:
                    temp_dados.unlink()
                except Exception:
                    pass

        remover_base_climatica_fora_da_brl(dist_dir, getattr(args, "edicao", "brl"))

    print(f"\n[SUCESSO] Compilação concluída com sucesso em: dist/{args.name}/")
    return True


def build_inno_setup(base_dir: Path) -> bool:
    """Compila o instalador Windows (.exe) utilizando o Inno Setup."""
    print("\n=======================================================")
    print("  Iniciando Criação do Instalador Inno Setup 6")
    print("=======================================================")

    iscc = find_inno_compiler()
    if not iscc:
        print("[AVISO] Compilador Inno Setup (ISCC.exe) não foi encontrado no sistema.")
        print("        Instale o Inno Setup 6 (https://jrsoftware.org/isdl.php) para gerar o instalador.")
        return False

    print(f"[+] Compilador Inno Setup localizado: {iscc}")

    # Cópia única na raiz. Havia uma segunda em infos_licenses/, defasada (nome do
    # grupo errado, exclusões antigas), usada só quando a da raiz faltava.
    iss_script = base_dir / "setup_script.iss"
    if not iss_script.exists():
        print(f"[ERRO] Script de instalação 'setup_script.iss' não encontrado.")
        return False

    print(f"[+] Utilizando script: {iss_script.relative_to(base_dir)}")

    faltando = verificar_pasta_para_instalador(base_dir)
    if faltando:
        print("[ERRO] A compilação em dist/Netuno está incompleta. Faltam:")
        for item in faltando:
            print(f"        - {item}")
        print("        Rode primeiro: python build_exe.py")
        return False

    versao = versao_do_programa(base_dir)
    print(f"[+] Versão do programa: {versao}")
    res = subprocess.run([str(iscc), f"/DMyAppVersion={versao}", str(iss_script)], cwd=base_dir)
    if res.returncode == 0:
        nome = f"Netuno_Setup_{versao.replace('.', '_')}.exe"
        print(f"\n[SUCESSO] Instalador gerado em: dist/{nome}")
        print("          A base CLIMBra compilada (652 cidades) vai embutida. Para instalar também")
        print("          os CSV brutos, copie a pasta 'climbra_data' para o lado do instalador.")
        return True
    else:
        print(f"\n[ERRO] Falha na compilação do instalador Inno Setup.")
        return False


def versao_do_programa(base_dir: Path) -> str:
    """Lê __version__ de netuno/__init__.py, sem importar o pacote."""
    import re
    texto = (base_dir / "netuno" / "__init__.py").read_text(encoding="utf-8")
    achado = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', texto)
    return achado.group(1) if achado else "5.0.0"


def verificar_pasta_para_instalador(base_dir: Path) -> list:
    """Arquivos que o setup_script.iss espera encontrar; devolve os ausentes."""
    esperados = [
        Path("dist/Netuno/Netuno.exe"),
        Path("dist/Netuno/_internal/data/languages/es.json"),
        Path("dist/Netuno/_internal/data/languages/zh.json"),
        Path("dist/Netuno/_internal/manual/Manual-Netuno-5.pdf"),
        Path("dist/Netuno/_internal") / BASE_CLIMATICA,
        Path("LICENSE"),
        Path("icons/netuno5.ico"),
        Path("infos_licenses/info_before.txt"),
        Path("infos_licenses/info_after.txt"),
    ]
    return [str(p) for p in esperados if not (base_dir / p).exists()]


PYTHON_MINIMO = (3, 12)

#: A base CLIMBra compilada. Entra no executável com a pasta `data` e é lida de
#: `_internal/data/climbra.db` (netuno/core/climate_database.py). Fica fora do git
#: (784 MB), por isso cada máquina de compilação a gera uma vez.
BASE_CLIMATICA = Path("data") / "climbra.db"
PASTAS_DE_CSV_CLIMBRA = ("climbra_data", "Netuno future files for 652 cities")


def remover_base_climatica_fora_da_brl(dist_dir: Path, edicao: str) -> None:
    """A base CLIMBra só cobre cidades brasileiras e vai só na Edição Brasil.

    O PyInstaller copia a pasta `data` inteira; na Internacional o banco sai
    depois, e a edição fica leve e trabalha com séries próprias.
    """
    if edicao == "brl":
        return
    for base in [dist_dir, dist_dir / "_internal"]:
        db = base / BASE_CLIMATICA
        if db.exists():
            db.unlink()
            print(f"[*] Removido da edição {edicao.upper()}: {db}")


def garantir_base_climatica(base_dir: Path) -> bool:
    """A Edição Brasil sai com a base CLIMBra embutida, ou não sai.

    Sem este passo, um `data/climbra.db` ausente passava calado: o PyInstaller
    copiava a pasta `data` sem ele e o instalador abria sem as 652 cidades.
    Se faltar o banco e houver os CSV brutos, compila-o; se não, recusa.
    """
    db = base_dir / BASE_CLIMATICA
    if db.is_file() and db.stat().st_size > 0:
        print(f"[+] Base climática CLIMBra embutida: {BASE_CLIMATICA} "
              f"({db.stat().st_size / 1e6:.0f} MB)")
        return True
    for pasta in PASTAS_DE_CSV_CLIMBRA:
        csv = base_dir / pasta
        if csv.is_dir():
            print(f"[*] {BASE_CLIMATICA} ausente: compilando a partir de '{pasta}'...")
            res = subprocess.run([sys.executable, str(base_dir / "scripts" / "compilar_base_climbra.py"),
                                  "--input", str(csv), "--output", str(db)], cwd=base_dir)
            return res.returncode == 0 and db.is_file()
    print(f"[ERRO] A Edição Brasil embute a base CLIMBra, e {BASE_CLIMATICA} não foi encontrado.")
    print("        Coloque o climbra.db em data/, ou a pasta 'climbra_data' com os CSV na raiz")
    print("        (compilada por scripts/compilar_base_climbra.py). Para um pacote de teste")
    print("        sem a base, use --sem-base-climatica.")
    return False

#: Edição → (ponto de entrada, nome do executável). A Edição Brasil mantém o nome
#: "Netuno": é a pasta dist/Netuno que o setup_script.iss empacota.
EDICOES = {
    "brl": ("main_brl.py", "Netuno"),
    "int": ("main_int.py", "Netuno_INT"),
}


def main():
    # O executável embute o Python que o compila. O código usa sintaxe do 3.12
    # (f-strings) e, compilado num Python anterior, o instalador sairia quebrado.
    if sys.version_info < PYTHON_MINIMO:
        sys.exit(f"[ERRO] Compile o Netuno com Python {PYTHON_MINIMO[0]}.{PYTHON_MINIMO[1]} ou superior "
                 f"(este é {sys.version.split()[0]}).")
    parser = argparse.ArgumentParser(
        description="Compilador oficial do Netuno 5 para Windows (PyInstaller + Inno Setup)"
    )
    parser.add_argument("--edition", choices=["brl", "int", "both"], default="brl",
                        help="Edição a compilar: 'brl' (Brasil, padrão), 'int' (Internacional) ou 'both'")
    parser.add_argument("--name", default=None, help="Nome do executável (padrão: conforme a edição)")
    parser.add_argument("--clean", action="store_true", help="Limpa as pastas build/ e dist/ antes de compilar")
    parser.add_argument("--onefile", action="store_true", help="Gera um executável único autocontido")
    parser.add_argument("--console", action="store_true", help="Mantém o console do prompt aberto ao executar")
    parser.add_argument("--installer", action="store_true", help="Compila automaticamente o instalador Inno Setup após o build")
    parser.add_argument("--sem-manual", action="store_true", help="Não regera o manual antes de empacotar")
    parser.add_argument("--sem-base-climatica", action="store_true",
                        help="Compila a edição Brasil sem exigir data/climbra.db (só para testes; não gera instalador)")

    args = parser.parse_args()
    base_dir = Path(__file__).resolve().parent

    if args.clean:
        clean_build_dirs(base_dir)

    # O manual entra no pacote, e por isso é gerado antes dele.
    if not args.sem_manual and not build_manual(base_dir):
        print("[AVISO] O manual não foi regerado; o pacote levará a versão anterior.")

    edicoes = ["brl", "int"] if args.edition == "both" else [args.edition]
    if "brl" in edicoes and not args.sem_base_climatica and not garantir_base_climatica(base_dir):
        sys.exit(1)

    for edicao in edicoes:
        script, nome = EDICOES[edicao]
        ed_args = argparse.Namespace(**vars(args))
        ed_args.name = args.name or nome
        ed_args.main_script = base_dir / script
        ed_args.edicao = edicao
        print(f"\n>>> Compilando a edição {edicao.upper()} ({ed_args.name}) <<<")
        success = build_pyinstaller(ed_args, base_dir)
        if success and args.installer:
            if edicao == "brl" and ed_args.name == "Netuno" and not args.sem_base_climatica:
                build_inno_setup(base_dir)
            else:
                print("[AVISO] O instalador (setup_script.iss) empacota a pasta dist/Netuno, da edição Brasil "
                      f"com a base CLIMBra. A compilação {edicao.upper()} fica em dist/{ed_args.name}.")


if __name__ == "__main__":
    main()
