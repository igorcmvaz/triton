"""Auditoria Arquitetural e Prontidão de Repositório (Inspirado em ArchUnitPython e 'Is your codebase ready for AI agents?').

Valida:
1. Regras de Isolamento Arquitetural: A camada de cálculo/núcleo ('triton.core')
   NUNCA deve importar a camada de interface gráfica ('triton.ui').
2. Documentação e Prontidão para IA: Todos os módulos de 'triton.core' devem
   possuir docstrings explicativas no topo de arquivo.
3. Integridade e Arquivos de Metadados: Verifica consistência do pacote,
   presença de README, LICENSE e pyproject.toml.
"""
from __future__ import annotations

import ast
import os
from pathlib import Path
import pytest

RAIZ = Path(__file__).resolve().parents[2]
PACOTE_TRITON = RAIZ / "triton"
CORE_DIR = PACOTE_TRITON / "core"
UI_DIR = PACOTE_TRITON / "ui"


def _listar_modulos_python(diretorio: Path) -> list[Path]:
    """Retorna todos os arquivos .py do diretório especificado, exceto __pycache__."""
    return [p for p in diretorio.glob("*.py") if p.is_file() and not p.name.startswith("__")]


def test_isolamento_arquitetural_core_nao_importa_ui():
    """Valida a regra fundamental de arquitetura: módulos de cálculo do core NUNCA importam triton.ui.
    
    Inspirado no paradigma ArchUnit / testes de limites arquiteturais.
    Garante que o motor de cálculo possa rodar em servidores headless, HPC e CLI
    sem dependência da biblioteca gráfica PySide6/Qt.
    
    Exceção documentada: report_generator e report_service usam dicionários de
    tradução para títulos e legendas dos relatórios impressos.
    """
    assert CORE_DIR.is_dir(), f"Diretório core não encontrado em {CORE_DIR}"
    
    violacoes = []
    modulos_isencao_relatorio = {"report_generator.py", "report_service.py"}
    
    for arq in _listar_modulos_python(CORE_DIR):
        if arq.name in modulos_isencao_relatorio:
            continue
            
        with open(arq, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()
            
        tree = ast.parse(conteudo, filename=str(arq))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "triton.ui" in alias.name or alias.name.startswith("ui"):
                        violacoes.append((arq.name, node.lineno, alias.name))
            elif isinstance(node, ast.ImportFrom):
                modulo = node.module or ""
                if "triton.ui" in modulo or modulo.startswith("ui"):
                    violacoes.append((arq.name, node.lineno, modulo))

    assert not violacoes, (
        f"Violação de isolamento arquitetural encontrada! Módulos do núcleo não devem importar triton.ui:\n"
        + "\n".join(f"  - {arq}:{linha} importou '{alvo}'" for arq, linha, alvo in violacoes)
    )


def test_prontidao_ia_docstrings_em_modulos_core():
    """Valida que módulos do núcleo possuem docstring explicativa (Is your codebase ready for AI agents?).
    
    Garante legibilidade para engenheiros, desenvolvedores e agentes autônomos de código.
    """
    modulos_sem_docstring = []
    
    for arq in _listar_modulos_python(CORE_DIR):
        with open(arq, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()
        try:
            tree = ast.parse(conteudo, filename=str(arq))
            docstring = ast.get_docstring(tree)
            if not docstring or len(docstring.strip()) < 10:
                modulos_sem_docstring.append(arq.name)
        except Exception:
            modulos_sem_docstring.append(f"{arq.name} (erro de parse)")

    assert not modulos_sem_docstring, (
        f"Módulos do núcleo sem docstring adequada:\n"
        + "\n".join(f"  - {m}" for m in modulos_sem_docstring)
    )


def test_arquivos_fundamentais_do_repositorio():
    """Valida a presença de arquivos essenciais de governança e configuração de projeto."""
    arquivos_obrigatorios = [
        RAIZ / "pyproject.toml",
        RAIZ / "README.md",
        RAIZ / "LICENSE",
        RAIZ / "CLAUDE.md",
        CORE_DIR / "simulation.py",
        CORE_DIR / "parser.py",
        CORE_DIR / "economic.py",
        CORE_DIR / "environmental.py",
    ]
    
    ausentes = [str(p.relative_to(RAIZ)) for p in arquivos_obrigatorios if not p.exists()]
    assert not ausentes, f"Arquivos essenciais ausentes no repositório: {ausentes}"
