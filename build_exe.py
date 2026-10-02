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
        # O .spec gerado vai para build/: na raiz, o PyInstaller reescrevia o
        # Netuno.spec versionado com os caminhos desta máquina, e o git pull seguinte
        # parava por «alterações locais».
        f"--specpath={base_dir / 'build'}",
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
            cmd.append(f"--add-data={src_path}{sep}{dst_rel}")
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
        "netuno.core.quantitativo_do_arranjo",
        "netuno.core.diagnostico",
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

    if not args.onefile and not diagnosticar_o_pacote(dist_dir, args):
        return False

    print(f"\n[SUCESSO] Compilação concluída com sucesso em: dist/{args.name}/")
    return True


def diagnosticar_o_pacote(dist_dir: Path, args) -> bool:
    """Roda o executável gerado com ``--diagnostico`` e recusa o pacote incompleto.

    O que o PyInstaller deixa de fora só aparece quando o programa roda: um pacote
    sem o visualizador 3D, sem o QtWebEngine ou com o banco tarifário antigo saía
    com «SUCESSO». Na Edição Brasil, a base CLIMBra também é exigida, salvo com
    --sem-base-climatica.
    """
    exe = dist_dir / (args.name + (".exe" if sys.platform.startswith("win") else ""))
    if not exe.is_file():
        print(f"[AVISO] Executável não encontrado para o diagnóstico: {exe}")
        return True
    ambiente = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    try:
        res = subprocess.run([str(exe), "--diagnostico"], env=ambiente, capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=300)
    except (OSError, subprocess.TimeoutExpired) as erro:
        print(f"[ERRO] O executável gerado não rodou o diagnóstico: {erro}")
        return False
    import tempfile
    relatorio = Path(tempfile.gettempdir()) / "netuno_diagnostico.txt"
    texto = res.stdout.strip() or (relatorio.read_text(encoding="utf-8") if relatorio.is_file() else "")
    print("\n[*] Diagnóstico do pacote gerado:\n" + texto)
    falhou = res.returncode != 0
    if getattr(args, "edicao", "brl") == "brl" and not getattr(args, "sem_base_climatica", False) \
            and "[FALTA] Base climática" in texto:
        falhou = True
    if falhou:
        print("[ERRO] O pacote saiu incompleto (itens marcados FALTA acima). Nada foi aprovado.")
        if res.stderr.strip():
            print(res.stderr.strip()[-2000:])
    return not falhou


def build_inno_setup(base_dir: Path, edicao: str = "brl") -> bool:
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

    faltando = verificar_pasta_para_instalador(base_dir, edicao)
    if faltando:
        print("[ERRO] A compilação em dist/Netuno está incompleta. Faltam:")
        for item in faltando:
            print(f"        - {item}")
        print("        Rode primeiro: python build_exe.py")
        return False

    versao = versao_do_programa(base_dir)
    print(f"[+] Versão do programa: {versao}")
    res = subprocess.run([str(iscc), f"/DMyAppVersion={versao}", f"/DEdition={edicao.upper()}", str(iss_script)],
                         cwd=base_dir)
    if res.returncode == 0:
        nome = f"{'Netuno_INT_Setup_' if edicao == 'int' else 'Netuno_Setup_'}{versao.replace('.', '_')}.exe"
        print(f"\n[SUCESSO] Instalador gerado em: dist/{nome}")
        print("          A base CLIMBra compilada (652 cidades) vai embutida.")
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


def verificar_pasta_para_instalador(base_dir: Path, edicao: str = "brl") -> list:
    """Arquivos que o setup_script.iss espera encontrar para a edição; devolve os ausentes."""
    pasta = Path("dist/Netuno_INT") if edicao == "int" else Path("dist/Netuno")
    exe = "Netuno_INT.exe" if edicao == "int" else "Netuno.exe"
    esperados = [
        pasta / exe,
        pasta / "_internal/data/languages/es.json",
        pasta / "_internal/data/languages/zh.json",
        pasta / "_internal/manual/Manual-Netuno-5.pdf",
        Path("LICENSE"),
        Path("Licence.txt"),
        Path("infos_licenses/AVISOS_DE_TERCEIROS.txt"),
        Path("icons/netuno5.ico"),
        Path("infos_licenses/info_before.txt"),
        Path("infos_licenses/info_after.txt"),
    ]
    if edicao == "brl":
        esperados.append(pasta / "_internal" / BASE_CLIMATICA)  # a base CLIMBra só vai na Brasil
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

    parser.add_argument("--ignorar-git", action="store_true",
                        help="Compila mesmo com a pasta atrás do origin/main (não recomendado)")

    args = parser.parse_args()
    base_dir = Path(__file__).resolve().parent

    if not conferir_a_pasta(base_dir, args.ignorar_git):
        sys.exit(1)
    limpos_antes = arquivos_versionados_limpos(base_dir)
    try:
        gravar_revisao(base_dir)

        if args.clean:
            clean_build_dirs(base_dir)

        # O manual entra no pacote, e por isso é gerado antes dele.
        if not args.sem_manual and not build_manual(base_dir):
            print("[AVISO] O manual não foi regerado; o pacote levará a versão anterior.")

        # As licenças de terceiros saem das versões instaladas aqui, as mesmas que vão no pacote.
        subprocess.run([sys.executable, str(base_dir / "scripts" / "gerar_avisos_de_terceiros.py")], cwd=base_dir)

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
                if ed_args.name != nome or (edicao == "brl" and args.sem_base_climatica):
                    print(f"[AVISO] Instalador não gerado: o setup_script.iss empacota dist/{nome}"
                          + (" com a base CLIMBra" if edicao == "brl" else "") + ".")
                else:
                    build_inno_setup(base_dir, edicao)
    finally:
        restaurar_gerados(base_dir, limpos_antes)


# ── Git: compilar o código certo e não sujar a pasta ─────────────────────────

def _git(base_dir: Path, *argumentos: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *argumentos], cwd=base_dir, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def conferir_a_pasta(base_dir: Path, ignorar: bool = False) -> bool:
    """Recusa compilar uma pasta atrás do origin/main.

    Um ``git pull`` interrompido por alterações locais deixa a pasta na versão
    anterior sem que nada avise, e o build empacotava esse código antigo.
    """
    try:
        if _git(base_dir, "rev-parse", "--is-inside-work-tree").returncode != 0:
            return True  # cópia sem git (pacote de código-fonte): nada a conferir
    except OSError:
        return True
    revisao = _git(base_dir, "rev-parse", "--short", "HEAD").stdout.strip()
    ramo = _git(base_dir, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    print(f"[+] Código a compilar: {ramo} @ {revisao}")
    if _git(base_dir, "fetch", "--quiet", "origin", "main").returncode != 0:
        print("[AVISO] Não foi possível consultar o origin/main (sem rede?); seguindo com a pasta como está.")
        return True
    atras = _git(base_dir, "rev-list", "--count", "HEAD..origin/main").stdout.strip()
    if atras and atras != "0":
        print(f"[ERRO] A pasta está {atras} commit(s) atrás do origin/main: o pacote sairia com o código antigo.")
        print("        Rode «git stash» e «git pull» (ou resolva o que o git pull acusar) e compile de novo.")
        if ignorar:
            print("[AVISO] --ignorar-git: compilando assim mesmo.")
            return True
        return False
    return True


def arquivos_versionados_limpos(base_dir: Path) -> set:
    """Arquivos versionados sem alteração antes do build: os únicos que ele pode restaurar."""
    try:
        alterados = _git(base_dir, "diff", "--name-only", "HEAD").stdout.split()
        todos = _git(base_dir, "ls-files").stdout.split("\n")
    except OSError:
        return set()
    return {f for f in todos if f} - set(alterados)


def restaurar_gerados(base_dir: Path, limpos_antes: set) -> None:
    """Devolve ao estado do commit o que só o build alterou (manual, site, changelog).

    O manual é regerado para entrar no pacote; as diferenças são de ambiente e não
    devem ficar na pasta, onde fariam o próximo git pull parar.
    """
    if not limpos_antes:
        return
    try:
        sujos = [f for f in _git(base_dir, "diff", "--name-only", "HEAD").stdout.split() if f in limpos_antes]
    except OSError:
        return
    if sujos:
        _git(base_dir, "checkout", "--", *sujos)
        print(f"[*] Restaurados {len(sujos)} arquivo(s) versionado(s) que o build regerou (manual, site, changelog).")


def gravar_revisao(base_dir: Path) -> None:
    """Grava em netuno/data/revisao.json o commit compilado, que o --diagnostico mostra."""
    import json
    from datetime import datetime

    try:
        dados = {
            "commit": _git(base_dir, "rev-parse", "--short", "HEAD").stdout.strip(),
            "ramo": _git(base_dir, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip(),
            "alteracoes_locais": bool(_git(base_dir, "status", "--porcelain", "--untracked-files=no").stdout.strip()),
        }
    except OSError:
        dados = {"commit": "", "ramo": "", "alteracoes_locais": False}
    dados["compilado_em"] = datetime.now().isoformat(timespec="seconds")
    (base_dir / "netuno" / "data" / "revisao.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2),
                                                                encoding="utf-8")


if __name__ == "__main__":
    main()
