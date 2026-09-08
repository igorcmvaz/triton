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


def build_pyinstaller(args, base_dir: Path) -> bool:
    """Executa a compilação do executável com PyInstaller."""
    print("\n=======================================================")
    print("  Iniciando Compilação PyInstaller — Netuno 5.0.7")
    print("=======================================================")

    try:
        import PyInstaller
    except ImportError:
        print("[*] PyInstaller não encontrado. Instalando automaticamente...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
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
        "netuno.core.mcdm_methods",
        "netuno.core.environmental_sync",
        "netuno.core.esg_certifications",
    ]
    for hi in hidden_imports:
        cmd.append(f"--hidden-import={hi}")

    main_script = base_dir / "main.py"
    cmd.append(str(main_script))

    print(f"\n[*] Executando comando de compilação...")
    res = subprocess.run(cmd, cwd=base_dir)
    if res.returncode != 0:
        print("\n[ERRO] Falha na compilação com PyInstaller.")
        return False

    # Pós-processamento de limpeza em dist/
    dist_dir = base_dir / "dist" / args.name
    if dist_dir.exists():
        for base in [dist_dir, dist_dir / "_internal"]:
            sim_outputs = base / "simulation_outputs"
            if sim_outputs.exists():
                shutil.rmtree(sim_outputs, ignore_errors=True)
            temp_dados = base / "data" / "Dados.txt"
            if temp_dados.exists():
                try:
                    temp_dados.unlink()
                except Exception:
                    pass

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

    iss_script = base_dir / "setup_script.iss"
    if not iss_script.exists():
        iss_script = base_dir / "infos_licenses" / "setup_script.iss"

    if not iss_script.exists():
        print(f"[ERRO] Script de instalação 'setup_script.iss' não encontrado.")
        return False

    print(f"[+] Utilizando script: {iss_script.relative_to(base_dir)}")
    res = subprocess.run([str(iscc), str(iss_script)], cwd=base_dir)
    if res.returncode == 0:
        print(f"\n[SUCESSO] Instalador oficial gerado em: dist/Netuno_Setup_5_0_7.exe")
        return True
    else:
        print(f"\n[ERRO] Falha na compilação do instalador Inno Setup.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Compilador oficial do Netuno 5 para Windows (PyInstaller + Inno Setup)"
    )
    parser.add_argument("--name", default="Netuno", help="Nome do executável gerado (padrão: Netuno)")
    parser.add_argument("--clean", action="store_true", help="Limpa as pastas build/ e dist/ antes de compilar")
    parser.add_argument("--onefile", action="store_true", help="Gera um executável único autocontido")
    parser.add_argument("--console", action="store_true", help="Mantém o console do prompt aberto ao executar")
    parser.add_argument("--installer", action="store_true", help="Compila automaticamente o instalador Inno Setup após o build")

    args = parser.parse_args()
    base_dir = Path(__file__).resolve().parent

    if args.clean:
        clean_build_dirs(base_dir)

    success = build_pyinstaller(args, base_dir)
    if success and args.installer:
        build_inno_setup(base_dir)


if __name__ == "__main__":
    main()
