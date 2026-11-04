"""Diagnóstico de uma instalação: o que este executável traz e o que consegue fazer.

``Triton.exe --diagnostico`` grava o relatório em ``triton_diagnostico.txt`` (na pasta
temporária) e o mostra. O ``build_exe.py`` o roda logo depois de compilar e recusa o
pacote sem volumetria 3D: assim uma versão sem o visualizador, sem a base climática
ou com o banco tarifário antigo deixa de passar calada.

Cada verificação devolve ``(item, ok, detalhe)``. ``ok`` é ``None`` quando o item
não se aplica à edição (a base CLIMBra na Internacional, por exemplo).
"""

from __future__ import annotations

import os
import sys
from typing import List, Optional, Tuple

Verificacao = Tuple[str, Optional[bool], str]

#: Itens sem os quais o pacote não sai (build_exe.py).
OBRIGATORIOS = ("Volumetria 3D (WebGL)", "Arranjo 3D e volumetria", "Banco tarifário")


def _volumetria_web() -> Verificacao:
    from triton.core.volumetry_export import VIEWER_BUNDLE

    if os.environ.get("TRITON_VOLUMETRIA_SIMPLES", "").strip() not in ("", "0"):
        return ("Volumetria 3D (WebGL)", False, "desligada por TRITON_VOLUMETRIA_SIMPLES")
    if not VIEWER_BUNDLE.is_file():
        return ("Volumetria 3D (WebGL)", False, f"visualizador ausente: {VIEWER_BUNDLE}")
    try:
        import PySide6.QtWebEngineWidgets  # noqa: F401
        from PySide6.QtCore import QLibraryInfo
    except Exception as erro:  # pragma: no cover - depende do pacote
        return ("Volumetria 3D (WebGL)", False, f"QtWebEngine não importa: {erro}")
    pasta = QLibraryInfo.path(QLibraryInfo.LibraryPath.LibraryExecutablesPath)
    processo = [n for n in ("QtWebEngineProcess.exe", "QtWebEngineProcess")
                if os.path.isfile(os.path.join(pasta, n))]
    if getattr(sys, "frozen", False) and not processo:
        return ("Volumetria 3D (WebGL)", False, f"QtWebEngineProcess ausente em {pasta}")
    tamanho = VIEWER_BUNDLE.stat().st_size / 1e3
    return ("Volumetria 3D (WebGL)", True, f"visualizador {tamanho:.0f} kB; QtWebEngine em {pasta}")


def _arranjo_3d() -> Verificacao:
    try:
        from triton.core.quantitativo_do_arranjo import conferir_cobertura, levantar
        from triton.core.study_layout import generate_study_layout
        from triton.core.volumetry import build_volumetry

        layout = generate_study_layout({"lower_vol": 5000, "area": 150, "pump_count": 2})
        cena = build_volumetry(dict(layout, project_name="diagnóstico"))
        faltam = conferir_cobertura(levantar(layout))
    except Exception as erro:
        return ("Arranjo 3D e volumetria", False, f"{type(erro).__name__}: {erro}")
    if faltam:
        return ("Arranjo 3D e volumetria", False, "; ".join(faltam))
    return ("Arranjo 3D e volumetria", True,
            f"{len(layout['bim_components'])} peças, {len(layout['pipe_runs'])} trechos, "
            f"{len(cena.solids)} sólidos; quantitativo completo")


def _base_climatica() -> Verificacao:
    from triton.core.climate_database import get_available_climate_cities, get_climate_db_path
    from triton.core.edition import rotulo_da_edicao, usa_dados_do_brasil

    banco = get_climate_db_path()
    cidades = len(get_available_climate_cities())
    if not usa_dados_do_brasil():
        return ("Base climática CLIMBra", None, f"não se aplica à {rotulo_da_edicao()}")
    if not banco or cidades == 0:
        return ("Base climática CLIMBra", False, "banco climbra.db não encontrado")
    return ("Base climática CLIMBra", True, f"{cidades} cidades em {banco}")


def _tarifas() -> Verificacao:
    from triton.core.edition import rotulo_da_edicao, usa_dados_do_brasil
    if not usa_dados_do_brasil():
        return ("Banco tarifário", None, f"não se aplica à {rotulo_da_edicao()}")
    try:
        from triton.core.tariff_regimes import EXPONENCIAL
        from triton.core.tariffs_database import _find_database_file, load_tariffs_db

        caminho = _find_database_file()
        cidades = load_tariffs_db().get("cities", {})
    except Exception as erro:
        return ("Banco tarifário", False, f"{type(erro).__name__}: {erro}")

    corsan = [d for d in cidades.values() if "CORSAN" in str(d.get("prestador_saneamento", "")).upper()]
    exponencial = sum(1 for d in corsan if d.get("regime_tarifario") == EXPONENCIAL)
    ok = bool(cidades) and exponencial == len(corsan)
    return ("Banco tarifário", ok,
            f"{len(cidades)} municípios; CORSAN na fórmula exponencial: {exponencial} de {len(corsan)}; {caminho}")


def _dados_de_portugal() -> Verificacao:
    """Base E-OBS por concelho e tarifários transcritos: só na Edição Ibérica."""
    from triton.core.edition import rotulo_da_edicao, usa_dados_de_portugal

    nome = "Dados de Portugal (E-OBS e tarifários)"
    if not usa_dados_de_portugal():
        return (nome, None, f"não se aplica à {rotulo_da_edicao()}")
    from triton.core import base_climatica_portugal as pt
    from triton.core import tarifarios_portugal as tarifas

    if not pt.disponivel():
        return (nome, False, "data/portugal_eobs.db não encontrado")
    return (nome, True, f"{len(pt.concelhos())} concelhos com série em {pt.caminho_da_base()}; "
                        f"tarifários: {', '.join(tarifas.concelhos())}")


def _dados_iberia() -> Verificacao:
    """Chuva do Iberia01 por município (Portugal, Espanha, Baleares) e ilhas por ERA5: só na Edição Ibérica."""
    from triton.core.edition import rotulo_da_edicao, usa_dados_de_portugal

    nome = "Dados ibéricos (Iberia01 e ilhas)"
    if not usa_dados_de_portugal():
        return (nome, None, f"não se aplica à {rotulo_da_edicao()}")
    from triton.core import base_climatica_iberica as ib

    if not ib.disponivel():
        return (nome, False, "ficheiros do Iberia01 (data/chuva_iberia01_p*.db, ibe_unidades.db) não encontrados")
    c = ib.contagens()
    partes = len(ib.partes_instaladas())
    return (nome, True, f"{c['PT']} unidades de Portugal e {c['ES']} de Espanha; {c['iberia01']} com Iberia01, "
                        f"{c['era5']} com ERA5 (nível C), {c['nenhuma']} sem chuva; {partes} partes em {ib.pasta_dos_dados()}")


def _manual() -> Verificacao:
    raiz = getattr(sys, "_MEIPASS", None)
    if not raiz:
        # No código-fonte, a raiz da edição é a pasta que tem `manual/` (o módulo mora em triton/core/system).
        atual = os.path.dirname(os.path.abspath(__file__))
        while atual and not os.path.isdir(os.path.join(atual, "manual")) and os.path.dirname(atual) != atual:
            atual = os.path.dirname(atual)
        raiz = atual
    from triton.core.edition import is_int_edition

    # A Internacional abre o manual em inglês (manual/en); as outras, o português.
    pdf = os.path.join(raiz, "manual", "en", "Triton-User-Manual.pdf") if is_int_edition() \
        else os.path.join(raiz, "manual", "Manual-Triton.pdf")
    return ("Manual em PDF", os.path.isfile(pdf), pdf)


def verificacoes() -> List[Verificacao]:
    itens: List[Verificacao] = []
    for funcao in (_volumetria_web, _arranjo_3d, _base_climatica, _tarifas, _dados_de_portugal, _dados_iberia, _manual):
        try:
            itens.append(funcao())
        except Exception as erro:  # um item quebrado não esconde os outros
            itens.append((funcao.__name__.strip("_"), False, f"{type(erro).__name__}: {erro}"))
    return itens


def revisao_compilada() -> str:
    """O commit de onde o pacote saiu, gravado pelo build_exe.py em triton/data/revisao.json."""
    import json
    from pathlib import Path

    _r1 = Path(__file__).resolve().parent.parent / "data" / "revisao.json"
    _r2 = Path(__file__).resolve().parent.parent.parent / "data" / "revisao.json"
    arquivo = _r1 if _r1.exists() else _r2
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "Revisão: não registrada (pacote gerado sem o build_exe.py, ou código-fonte)"
    texto = f"Revisão: {dados.get('commit') or '?'} ({dados.get('ramo') or '?'}), compilado em {dados.get('compilado_em', '?')}"
    if dados.get("alteracoes_locais"):
        texto += " — ATENÇÃO: havia alterações locais não commitadas"
    return texto


def relatorio(itens: Optional[List[Verificacao]] = None) -> str:
    from triton import __version__
    from triton.core.edition import rotulo_da_edicao

    itens = verificacoes() if itens is None else itens
    linhas = [
        f"Triton {__version__} — {rotulo_da_edicao()}",
        f"Executável: {sys.executable}" + (" (empacotado)" if getattr(sys, "frozen", False) else " (código-fonte)"),
        revisao_compilada(),
        "",
    ]
    for nome, ok, detalhe in itens:
        marca = "—" if ok is None else ("OK" if ok else "FALTA")
        linhas.append(f"[{marca:5}] {nome}: {detalhe}")
    return "\n".join(linhas) + "\n"


def faltam_obrigatorios(itens: List[Verificacao]) -> List[str]:
    return [nome for nome, ok, _ in itens if nome in OBRIGATORIOS and ok is False]
