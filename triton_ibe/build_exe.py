"""
Script de Compilação do Triton em Executável e Instalador Windows.
Suporta PyInstaller (standalone onedir / onefile) e Inno Setup 6.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def find_icon(base_dir: Path) -> Path | None:
    """Busca o ícone oficial da aplicação nos locais padrão."""
    candidates = [
        base_dir / "icons" / "triton.ico",
        base_dir / "icons" / "icon.ico",
        base_dir / "icons" / "triton.ico",
        base_dir / "icon.ico",
        base_dir / "triton.ico",
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


def build_manual(base_dir: Path, com_ingles: bool = False, so_ingles: bool = False) -> bool:
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
    if so_ingles:
        # A Internacional não tem o manual em português (manual/partes), de onde a cadeia parte: as tabelas
        # em inglês são traduzidas das portuguesas, e a montagem em português deixava lixo na pasta. O manual
        # inglês (manual/en) é regerado pelo mantenedor (gerar.py/gerar_pdf.py --idioma en) e versionado:
        # o pacote leva o PDF do commit.
        print("    Internacional: o pacote leva o manual em inglês versionado (manual/en/Triton-User-Manual.pdf).")
        return True
    if com_ingles:
        # O manual em inglês é só da Internacional (manual/en); a Brasil e a Ibérica não o têm.
        etapas += [
            ("tabelas em inglês", "manual/en/traduzir_tabelas.py"),
            ("apêndices em inglês", "manual/en/apendices_en.py"),
            ("montagem em inglês", "manual/gerar.py", "--idioma", "en"),
            ("PDF em inglês", "manual/gerar_pdf.py", "--idioma", "en"),
        ]
    geradas = 0
    for rotulo, script, *argumentos in etapas:
        caminho = base_dir / script
        if not caminho.exists():
            print(f"    {rotulo}: {script} não encontrado; pulando")
            continue
        geradas += 1
        res = subprocess.run([sys.executable, str(caminho), *argumentos], cwd=base_dir)
        if res.returncode != 0:
            print(f"[ERRO] Falha ao gerar {rotulo}.")
            return False
        print(f"    {rotulo}: ok")
    if not geradas:
        # Os geradores do manual ficam no disco do mantenedor, fora do Git (pasta manual_fonte/).
        print("    Nenhum gerador do manual nesta pasta: o pacote leva os PDFs versionados em manual/.")
    return True


def entradas_do_pacote(base_dir: Path, edicao: str) -> list:
    """Lista (origem, destino) do `--add-data` da edição, sem o que não pode ir em nenhuma.

    `data` e `tarifas` entram item a item: o PyInstaller copia o que recebe, e copiar `tarifas/fontes`
    (200 MB de documentos de terceiros), `data/simulation_outputs` (514 MB) e o `climbra.db` antigo
    (820 MB) para só apagá-los depois custava minutos e disco. As remoções do pós-processamento ficam
    como segunda barreira.
    """
    def filhos(pasta: str, destino: str, pular=lambda nome: False) -> list:
        raiz = base_dir / pasta
        if not raiz.is_dir():
            return []
        return [(f"{pasta}/{f.name}", destino if f.is_file() else f"{destino}/{f.name}")
                for f in sorted(raiz.iterdir())
                if f.name != "__pycache__" and not pular(f.name)]

    def pular_data(nome: str) -> bool:
        if nome in ("simulation_outputs", "Dados.txt", "brazilSHP", "portugal", "climbra.db"):
            return True
        if (nome.startswith("climbra_") and nome.endswith((".db", ".json"))) and edicao != "brl":
            return True
        return nome == "portugal_eobs.db" and edicao != "ibe"

    tarifas_de_terceiros = {rel.name for rel in SO_DOCUMENTOS_DE_TERCEIROS if rel.parts[0] == "tarifas"}
    entradas = filhos("data", "data", pular_data)
    if edicao == "brl":
        entradas += filhos("tarifas", "tarifas", lambda nome: nome in tarifas_de_terceiros)
    entradas += [
        ("templates", "templates"),
        ("icons", "icons"),
        ("triton/data", "triton/data"),
    ]
    entradas += filhos("additional_material", "additional_material", lambda nome: nome == "documentation")
    entradas += [
        # O manual promete os casos e os estudos de exemplo na pasta do
        # programa, e o menu Ajuda abre o PDF e o relatório de verificação:
        # nenhum dos quatro entrava no executável.
        ("manual/casos", "casos"),
        ("examples", "exemplos"),
        ("docs", "docs"),
        ("manual/Manual-Triton.pdf", "manual"),
        # Os sete volumes avulsos, para mandar só uma parte do manual.
        ("manual/mini", "manual/mini"),
        # Manual interativo offline (HTML/JS/CSS)
        ("manual/site", "manual/site"),
    ]
    if edicao == "int":
        # O manual em inglês é o que a Internacional abre; a Brasil e a Ibérica não têm manual/en.
        entradas.append(("manual/en/Triton-User-Manual.pdf", "manual/en"))
    return entradas


def build_pyinstaller(args, base_dir: Path) -> bool:
    """Executa a compilação do executável com PyInstaller."""
    print("\n=======================================================")
    from triton import __version__
    print(f"  Iniciando Compilação PyInstaller — Triton {__version__}")
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
        # Triton.spec versionado com os caminhos desta máquina, e o git pull seguinte
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

    # Inclusão de pastas de dados e templates, por edição
    data_folders = entradas_do_pacote(base_dir, getattr(args, "edicao", "brl"))

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
        "ezdxf",
        "triton.core.mcdm_methods",
        "triton.core.environmental_sync",
        "triton.core.esg_certifications",
        "triton.core.comprimento_de_serie",
        "triton.core.demanda_estocastica",
        "triton.ui.dialogs.dialog_comprimento_de_serie",
        "triton.core.excel_scenarios",
        "triton.ui.tab_economic_global_optimizer",
        "triton.core.edition",
        "triton.core.vigencia_tarifaria",
        # Planta 3D, esquema e volumetria: parte é importada só dentro de funções.
        "triton.core.component_geometry",
        "triton.core.pipe_network",
        "triton.core.plant_3d",
        "triton.core.schematic_3d",
        "triton.core.study_layout",
        "triton.core.exportar_tudo",
        "triton.core.quantitativo_do_arranjo",
        "triton.core.diagnostico",
        "triton.core.volumetry",
        "triton.core.volumetry_export",
        "triton.ui.volumetry_view",
        # Volumetria WebGL (three.js) na aba; o pacote do visualizador e o céu
        # vão em triton/data/volumetria.
        "triton.ui.volumetry_web",
        "PySide6.QtWebEngineWidgets",
        "PySide6.QtWebEngineCore",
        "triton.ui.dialogs.pipe_runs_dialog",
        "PySide6.QtSvg",
        "ezdxf.render.forms",
        "triton.cli",
        "triton.cli_estudo",
        "triton.core.estudo",
        "triton.core.modulacao_estocastica",
        "triton.ui.tab_modulacao_estocastica",
        "triton.ui.portugues_de_portugal",
        # A base E-OBS da Portugal é importada só dentro das funções da etapa 1 e do parser.
        "triton.core.base_climatica_portugal",
        "triton.core.licenca_eobs",
        "triton.ui.dialogs.dialog_licenca_eobs",
        "triton.core.dados_do_relatorio",
        "triton.ui.moeda_na_interface",
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
            shp_dir = base / "data" / "brazilSHP"
            if shp_dir.exists():
                shutil.rmtree(shp_dir, ignore_errors=True)
            site_pdf = base / "manual" / "site" / "pdf"
            if site_pdf.exists():
                shutil.rmtree(site_pdf, ignore_errors=True)


        remover_base_climatica_fora_da_brl(dist_dir, getattr(args, "edicao", "brl"))
        remover_dados_de_portugal_fora_da_ibe(dist_dir, getattr(args, "edicao", "brl"))
        remover_tarifas_fora_da_brl(dist_dir, getattr(args, "edicao", "brl"))
        podar_caminhos_excessivos_para_inno_setup(dist_dir)

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
    relatorio = Path(tempfile.gettempdir()) / "triton_diagnostico.txt"
    texto = res.stdout.strip() or (relatorio.read_text(encoding="utf-8", errors="replace") if relatorio.is_file() else "")
    try:
        print("\n[*] Diagnóstico do pacote gerado:\n" + texto)
    except Exception:
        try:
            print("\n[*] Diagnóstico do pacote gerado:\n" + texto.encode(sys.stdout.encoding or "ascii", errors="replace").decode(sys.stdout.encoding or "ascii"))
        except Exception:
            pass
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
        print("[ERRO] A compilação em dist/Triton está incompleta. Faltam:")
        for item in faltando:
            print(f"        - {item}")
        print("        Rode primeiro: python build_exe.py")
        return False

    versao = versao_do_programa(base_dir)
    print(f"[+] Versão do programa: {versao}")
    res = subprocess.run([str(iscc), f"/DMyAppVersion={versao}", f"/DEdition={edicao.upper()}", str(iss_script)],
                         cwd=base_dir)
    if res.returncode == 0:
        prefixo = {"int": "Triton_INT_Setup_", "ibe": "Triton_IBE_Setup_"}.get(edicao, "Triton_Setup_")
        nome = f"{prefixo}{versao.replace('.', '_')}.exe"
        print(f"\n[SUCESSO] Instalador gerado em: dist/{nome}")
        if edicao == "brl":
            print("          A base CLIMBra compilada (652 cidades) vai embutida.")
        return True
    else:
        print(f"\n[ERRO] Falha na compilação do instalador Inno Setup.")
        return False


def versao_do_programa(base_dir: Path) -> str:
    """Lê __version__ de triton/__init__.py, sem importar o pacote."""
    import re
    texto = (base_dir / "triton" / "__init__.py").read_text(encoding="utf-8")
    achado = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', texto)
    return achado.group(1) if achado else "0.1.0"


def verificar_pasta_para_instalador(base_dir: Path, edicao: str = "brl") -> list:
    """Arquivos que o setup_script.iss espera encontrar para a edição; devolve os ausentes."""
    nome = EDICOES.get(edicao, EDICOES["brl"])[1]
    pasta = Path("dist") / nome
    exe = f"{nome}.exe"
    esperados = [
        pasta / exe,
        pasta / "_internal/data/languages/es.json",
        pasta / "_internal/data/languages/zh.json",
        Path("LICENSE.md"),
        Path("infos_licenses/AVISOS_DE_TERCEIROS.txt"),
        Path("icons/triton.ico"),
        Path("infos_licenses/info_before.txt"),
        Path("infos_licenses/info_after.txt"),
    ]
    if edicao == "int":
        esperados.append(pasta / "_internal/manual/en/Triton-User-Manual.pdf")  # o manual que a Internacional abre
    else:
        esperados.append(pasta / "_internal/manual/Manual-Triton.pdf")
    if edicao == "brl":
        # a base CLIMBra só vai na Brasil: um banco por modelo
        esperados += [pasta / "_internal" / "data" / f"climbra_{m}.db" for m in modelos_climbra()]
    if edicao == "ibe":
        esperados.append(pasta / "_internal" / BASE_PORTUGAL)  # a base E-OBS só vai na Portugal
    return [str(p) for p in esperados if not (base_dir / p).exists()]


PYTHON_MINIMO = (3, 12)

#: A base CLIMBra compilada: um banco por modelo CMIP6, `data/climbra_<modelo>.db` (40 a 44 MB cada, para caber
#: no GitHub), mais o manifesto `data/climbra_partes.json`. Entra no executável com a pasta `data` e é lida de
#: `_internal/data` (triton/core/climate_database.py). O `data/climbra.db` único das versões anteriores ainda
#: é lido pelo programa, mas não vai no pacote quando as partes existem (seria o mesmo conteúdo em dobro).
BASE_CLIMATICA_UNICA = Path("data") / "climbra.db"
MANIFESTO_CLIMBRA = Path("data") / "climbra_partes.json"


def modelos_climbra() -> list:
    """Os 19 modelos CMIP6 da base, na ordem do programa (lidos de triton/core/climate_database.py, sem importá-lo)."""
    texto = (Path(__file__).resolve().parent / "triton" / "core" / "climate_database.py").read_text(encoding="utf-8")
    bloco = re.search(r"CLIMATE_MODELS:\s*List\[str\]\s*=\s*\[(.*?)\]", texto, re.S)
    return re.findall(r'"([^"]+)"', bloco.group(1)) if bloco else []


def partes_da_base_climatica(raiz: Path) -> list:
    """Caminhos esperados das partes `data/climbra_<modelo>.db` sob `raiz`."""
    return [raiz / "data" / f"climbra_{modelo}.db" for modelo in modelos_climbra()]


#: A base E-OBS por concelho da Edição Ibérica (triton/core/base_climatica_portugal.py), versionada em
#: data/portugal_eobs.db. As fontes brutas (E-OBS, CAOP; 3 GB) ficam em data/portugal, no disco do
#: mantenedor, e não vão em nenhum pacote.
BASE_PORTUGAL = Path("data") / "portugal_eobs.db"
FONTES_DE_PORTUGAL = Path("data") / "portugal"


#: Material de terceiros (documentos dos prestadores, o banco que os reúne e o manual do Netuno 4): fica no
#: disco do mantenedor e não vai em nenhum instalador. O programa não lê nada disso em execução.
SO_DOCUMENTOS_DE_TERCEIROS = (
    Path("tarifas") / "fontes",
    Path("tarifas") / "entrada",
    Path("tarifas") / "tarifas_fontes.db",
    Path("tarifas_portugal") / "fontes",
    Path("tarifas_portugal") / "tarifas_portugal_fontes.db",
    Path("additional_material") / "documentation",
)


def remover_tarifas_fora_da_brl(dist_dir: Path, edicao: str) -> None:
    """A pasta `tarifas` (transcrições e catálogo auditado) é da Edição Brasil; a Internacional não a leva.

    O programa lê `triton/data/brazil_cities_tariffs.json` e `tarifas/catalogo_tarifas_auditado_652.csv`.
    Os documentos de terceiros (`fontes`, o banco que os reúne, o manual do Netuno 4) e a `entrada`,
    material ainda não processado, não vão em nenhuma edição.
    """
    for base in [dist_dir, dist_dir / "_internal"]:
        alvos = [base / rel for rel in SO_DOCUMENTOS_DE_TERCEIROS]
        if edicao != "brl":
            alvos.append(base / "tarifas")
        for alvo in alvos:
            if alvo.is_dir():
                shutil.rmtree(alvo, ignore_errors=True)
                print(f"[*] Removido da edição {edicao.upper()}: {alvo}")
            elif alvo.is_file():
                alvo.unlink()
                print(f"[*] Removido da edição {edicao.upper()}: {alvo}")


def podar_caminhos_excessivos_para_inno_setup(dist_dir: Path) -> None:
    """O Inno Setup (ISCC.exe) falha ao compilar arquivos com caminho >= 260 caracteres (MAX_PATH).

    Remove arquivos em dist/ cujo caminho absoluto exceda o limite seguro (ex.: assets de páginas baixadas em tarifas/fontes).
    """
    for base in [dist_dir, dist_dir / "_internal"]:
        if not base.exists():
            continue
        for raiz, _pastas, arquivos in os.walk(base):
            for arq in arquivos:
                caminho = Path(raiz) / arq
                if len(str(caminho.resolve())) >= 250:
                    try:
                        caminho.unlink()
                        print(f"[*] Removido do pacote arquivo com caminho longo (>250 caracteres): {caminho.name}")
                    except Exception as exc:
                        print(f"[!] Aviso ao podar caminho excessivo: {exc}")


def remover_base_climatica_fora_da_brl(dist_dir: Path, edicao: str) -> None:
    """A base CLIMBra só cobre cidades brasileiras e vai só na Edição Brasil.

    O PyInstaller copia a pasta `data` inteira. Fora da Brasil saem as partes por modelo, o manifesto e o
    banco único antigo. Na Brasil, o banco único sai se as partes estiverem completas: o conteúdo é o mesmo.
    """
    for base in [dist_dir, dist_dir / "_internal"]:
        unico = base / BASE_CLIMATICA_UNICA
        pasta = base / "data"
        if edicao != "brl":
            alvos = sorted(pasta.glob("climbra_*.db")) + [pasta / "climbra_partes.json", unico]
        elif unico.exists() and all(p.is_file() for p in partes_da_base_climatica(base)):
            alvos = [unico]
        else:
            alvos = []
        for alvo in alvos:
            if alvo.exists():
                alvo.unlink()
                print(f"[*] Removido da edição {edicao.upper()}: {alvo}")


def remover_dados_de_portugal_fora_da_ibe(dist_dir: Path, edicao: str) -> None:
    """As fontes brutas saem de todas as edições; a base E-OBS fica só na Portugal."""
    for base in [dist_dir, dist_dir / "_internal"]:
        fontes = base / FONTES_DE_PORTUGAL
        if fontes.exists():
            shutil.rmtree(fontes, ignore_errors=True)
            print(f"[*] Removido do pacote: {fontes}")
        db = base / BASE_PORTUGAL
        if edicao != "ibe" and db.exists():
            db.unlink()
            print(f"[*] Removido da edição {edicao.upper()}: {db}")


def garantir_base_portugal(base_dir: Path) -> bool:
    """A Edição Ibérica sai com a base E-OBS por concelho embutida, ou não sai."""
    db = base_dir / BASE_PORTUGAL
    if db.is_file() and db.stat().st_size > 0:
        print(f"[+] Base E-OBS de Portugal embutida: {BASE_PORTUGAL} ({db.stat().st_size / 1e6:.1f} MB)")
        return True
    print(f"[ERRO] A Edição Ibérica embute a base E-OBS, e {BASE_PORTUGAL} não foi encontrado.")
    print("        Ela é versionada no repositório. Para um pacote de teste sem a base, use --sem-base-climatica.")
    return False


def garantir_base_climatica(base_dir: Path) -> bool:
    """A Edição Brasil sai com a base CLIMBra embutida, ou não sai.

    Sem este passo, uma base ausente passava calada: o PyInstaller copiava a pasta `data` sem ela e o
    instalador abria sem as 652 cidades. Vale ter os 19 bancos por modelo, versionados em `data/`.
    """
    partes = partes_da_base_climatica(base_dir)
    faltam = [p for p in partes if not (p.is_file() and p.stat().st_size > 0)]
    if partes and not faltam:
        tamanho = sum(p.stat().st_size for p in partes) / 1e6
        print(f"[+] Base climática CLIMBra embutida: {len(partes)} bancos em data/ ({tamanho:.0f} MB)")
        return True
    print("[ERRO] A Edição Brasil embute a base CLIMBra, e os bancos data/climbra_<modelo>.db não foram encontrados.")
    print(f"        Faltam {len(faltam)} de {len(partes)} (o primeiro: {faltam[0].name if faltam else '-'}).")
    print("        Obtenha-os (estão versionados no repositório). Para um pacote de teste sem a base, use")
    print("        --sem-base-climatica.")
    return False


#: Edição → (ponto de entrada, nome do executável). A Edição Brasil mantém o nome
#: "Triton": é a pasta dist/Triton que o setup_script.iss empacota.
EDICOES = {
    "brl": ("main.py", "Triton"),
    "int": ("main.py", "Triton_INT"),
    "ibe": ("main.py", "Triton_IBE"),
}


def main():
    # O executável embute o Python que o compila. O código usa sintaxe do 3.12
    # (f-strings) e, compilado num Python anterior, o instalador sairia quebrado.
    if sys.version_info < PYTHON_MINIMO:
        sys.exit(f"[ERRO] Compile o Triton com Python {PYTHON_MINIMO[0]}.{PYTHON_MINIMO[1]} ou superior "
                 f"(este é {sys.version.split()[0]}).")
    parser = argparse.ArgumentParser(
        description="Compilador oficial do Triton para Windows (PyInstaller + Inno Setup)"
    )
    parser.add_argument("--edition", choices=["brl", "int", "ibe", "prt", "por", "both", "all"], default="ibe",
                        help="Edição a compilar: 'brl' (Brasil, padrão), 'int' (Internacional), 'ibe' (Ibérica; 'prt' e 'por' são nomes antigos dela), "
                             "'both' (BRL e INT) ou 'all' (as três)")
    parser.add_argument("--name", default=None, help="Nome do executável (padrão: conforme a edição)")
    parser.add_argument("--clean", action="store_true", help="Limpa as pastas build/ e dist/ antes de compilar")
    parser.add_argument("--onefile", action="store_true", help="Gera um executável único autocontido")
    parser.add_argument("--console", action="store_true", help="Mantém o console do prompt aberto ao executar")
    parser.add_argument("--installer", action="store_true", help="Compila automaticamente o instalador Inno Setup após o build")
    parser.add_argument("--sem-manual", action="store_true", help="Não regera o manual antes de empacotar")
    parser.add_argument("--sem-base-climatica", action="store_true",
                        help="Compila a Brasil sem exigir os bancos data/climbra_<modelo>.db e a Ibérica sem data/portugal_eobs.db "
                             "(só para testes; não gera instalador)")

    parser.add_argument("--ignorar-git", action="store_true",
                        help="Compila mesmo com a pasta atrás do origin/main (não recomendado)")

    args = parser.parse_args()
    if args.edition in ("prt", "por"):   # nomes antigos da Edição Ibérica
        args.edition = "ibe"
    base_dir = Path(__file__).resolve().parent

    if not conferir_a_pasta(base_dir, args.ignorar_git):
        sys.exit(1)
    limpos_antes = arquivos_versionados_limpos(base_dir)
    try:
        gravar_revisao(base_dir)

        if args.clean:
            clean_build_dirs(base_dir)

        edicoes = {"both": ["brl", "int"], "all": ["brl", "int", "ibe"]}.get(args.edition, [args.edition])

        # O manual entra no pacote, e por isso é gerado antes dele.
        if not args.sem_manual and not build_manual(base_dir, com_ingles="int" in edicoes, so_ingles=edicoes == ["int"]):
            print("[AVISO] O manual não foi regerado; o pacote levará a versão anterior.")

        # As licenças de terceiros saem das versões instaladas aqui, as mesmas que vão no pacote. O gerador
        # é ferramenta de desenvolvimento (fica no disco do mantenedor); sem ele, vale o arquivo versionado.
        gerador_de_avisos = base_dir / "scripts" / "gerar_avisos_de_terceiros.py"
        if gerador_de_avisos.is_file():
            subprocess.run([sys.executable, str(gerador_de_avisos)], cwd=base_dir)
        else:
            print("[*] Sem scripts/gerar_avisos_de_terceiros.py: o pacote leva infos_licenses/AVISOS_DE_TERCEIROS.txt como está.")

        if "brl" in edicoes and not args.sem_base_climatica and not garantir_base_climatica(base_dir):
            sys.exit(1)
        if "ibe" in edicoes and not args.sem_base_climatica and not garantir_base_portugal(base_dir):
            sys.exit(1)

        for edicao in edicoes:
            script, nome = EDICOES[edicao]
            ed_args = argparse.Namespace(**vars(args))
            ed_args.name = args.name or nome
            ed_args.main_script = base_dir / script
            ed_args.edicao = edicao
            gravar_marcador_da_edicao(base_dir, edicao)
            print(f"\n>>> Compilando a edição {edicao.upper()} ({ed_args.name}) <<<")
            success = build_pyinstaller(ed_args, base_dir)
            if success and args.installer:
                if ed_args.name != nome or (edicao in ("brl", "ibe") and args.sem_base_climatica):
                    print(f"[AVISO] Instalador não gerado: o setup_script.iss empacota dist/{nome}"
                          + {"brl": " com a base CLIMBra", "ibe": " com a base E-OBS"}.get(edicao, "") + ".")
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
        alterados = _git(base_dir, "diff", "--name-only", "--relative", "HEAD").stdout.split()
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
        sujos = [f for f in _git(base_dir, "diff", "--name-only", "--relative", "HEAD").stdout.split() if f in limpos_antes]
    except OSError:
        return
    if sujos:
        _git(base_dir, "checkout", "--", *sujos)
        print(f"[*] Restaurados {len(sujos)} arquivo(s) versionado(s) que o build regerou (manual, site, changelog).")


def gravar_marcador_da_edicao(base_dir: Path, edicao: str) -> None:
    """Grava em triton/data/edicao_padrao.txt a edição compilada (nada na Brasil).

    É o arquivo que ``triton.core.edition`` lê quando ``TRITON_EDITION`` não está definida: o
    comando ``triton`` e ``python -m triton.cli`` rodam como a edição da pasta ou do pacote. Cada pasta
    de edição já o traz versionado; regravar aqui garante o acerto se uma pasta compilar outra edição.
    ``triton/data`` entra inteira no pacote (``--add-data``), e o marcador vai junto.
    """
    marcador = base_dir / "triton" / "data" / "edicao_padrao.txt"
    if edicao in ("int", "ibe"):
        marcador.write_text(edicao.upper() + "\n", encoding="utf-8", newline="\n")
    elif marcador.exists():
        marcador.unlink()


def gravar_revisao(base_dir: Path) -> None:
    """Grava em triton/data/revisao.json o commit compilado, que o --diagnostico mostra."""
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
    (base_dir / "triton" / "data" / "revisao.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2),
                                                                encoding="utf-8")


if __name__ == "__main__":
    main()
