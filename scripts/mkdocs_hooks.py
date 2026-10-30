# -*- coding: utf-8 -*-
"""Gancho do mkdocs: acrescenta ao site os documentos técnicos que ficam fora de ``docs/`` (ferramenta só de desenvolvimento).

O ``mkdocs.yml`` da raiz do monorepo lê ``docs/``; os documentos técnicos de ``triton_int/`` ficam nas pastas das edições,
porque são os que o instalador leva. Em vez de copiá-los, o gancho os declara ao mkdocs como arquivos gerados que apontam
para o original, sob os caminhos de ``extra.docs_externos`` (destino no site -> origem, relativa à pasta do ``mkdocs.yml``).
O pacote ``mkdocs`` só é importado na hora de montar o site; ``mapa_de_externos`` não precisa dele (é o que o teste usa).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping


def mapa_de_externos(raiz: Path, extra: Mapping[str, Any]) -> Dict[str, Path]:
    """``{destino no site: caminho absoluto do original}`` a partir de ``extra.docs_externos``."""
    declarados = (extra or {}).get("docs_externos") or {}
    return {str(destino): (Path(raiz) / str(origem)).resolve() for destino, origem in declarados.items()}


def on_files(files: Any, config: Any) -> Any:
    """Ponto de extensão do mkdocs: inclui cada documento externo que existe; avisa dos que faltam."""
    import logging
    from mkdocs.structure.files import File
    registro = logging.getLogger("mkdocs.hooks.triton")
    raiz = Path(config.config_file_path).resolve().parent
    for destino, origem in mapa_de_externos(raiz, config.get("extra") or {}).items():
        if not origem.is_file():
            registro.warning("documento externo ausente: %s", origem)
            continue
        files.append(File.generated(config, destino, abs_src_path=str(origem)))
    return files
