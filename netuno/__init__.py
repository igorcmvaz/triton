"""
Netuno Python Simulation Engine
High-performance replication and evolution of Netuno 4.0 rainwater harvesting simulation software.
"""

from datetime import datetime
import hashlib
import re
import unicodedata

__version__ = "5.0.7"
APP_NAME = "Netuno"
APP_VERSION_LABEL = f"Netuno {__version__}"
APP_TITLE = f"Netuno {__version__} — Dimensionamento e Aproveitamento de Água de Chuva"


def get_kebab_filename(prefix: str, ext: str) -> str:
    """
    Gera um nome de arquivo em formato Kebab-Case com data e horário atual.
    Exemplo: netuno-relatorio-2026-07-31-174542.pdf
             netuno-projeto-2026-07-31-174542.csv
             netuno-cenarios-2026-07-31-174542.xlsx
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    clean_prefix = prefix.strip().lower().replace(" ", "-").replace("_", "-")
    ext = ext.lstrip(".")
    return f"{clean_prefix}-{timestamp}.{ext}"


def get_auditable_filename(
    project_name: str,
    project_id: str,
    artifact: str,
    ext: str,
    now=None,
) -> str:
    """Nome auditável: tipo + projeto + data/hora + hash estável da referência."""
    normalized = unicodedata.normalize("NFKD", (project_name or "Projeto Netuno").strip())
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-") or "projeto-netuno"
    slug = slug[:64].rstrip("-")
    artifact_slug = re.sub(r"[^a-z0-9]+", "-", (artifact or "arquivo").lower()).strip("-") or "arquivo"
    reference = (project_id or "N5-PROJ").strip()
    project_hash = hashlib.sha256(reference.encode("utf-8")).hexdigest()[:8].upper()
    timestamp = (now or datetime.now()).strftime("%Y-%m-%d-%H%M%S")
    return f"netuno-{artifact_slug}-{slug}-{timestamp}-{project_hash}.{ext.lstrip('.')}"


def get_project_filename(project_name: str, project_id: str, ext: str = "netuno", now=None) -> str:
    """Nome do projeto com nome legível, data/hora e hash estável da referência."""
    return get_auditable_filename(project_name, project_id, "projeto", ext, now=now)
