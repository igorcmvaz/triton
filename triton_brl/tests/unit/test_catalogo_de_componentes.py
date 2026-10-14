"""Todo tipo do catálogo BIM existe em todas as saídas.

Um tipo novo passa por cinco lugares: o bloco DXF, a família do Revit, o rótulo
do esquema 3D, o nome e a ficha da volumetria e o modelo do visualizador WebGL.
Esquecer um deles não quebra nada na hora — a peça só sai sem símbolo, sem
família ou como caixa genérica. Este teste cobra os cinco de uma vez.
"""

import json
from pathlib import Path

import ezdxf
import pytest

from triton.core.bim_exporter import COMPONENT_TYPES
from triton.core.cad_block_library import register_plan_blocks
from triton.core.schematic_3d import _TYPE_LABELS
from triton.core.volumetry import _ACCESSORY_INFO, _COLORS, _TYPE_NAMES

RAIZ = Path(__file__).resolve().parents[2]
TIPOS = [item["type_id"] for item in COMPONENT_TYPES]
#: Tipos com ficha própria em volumetry._component_solid_body (não usam a genérica).
COM_FICHA_PROPRIA = {"cisterna_inferior", "reservatorio_superior", "filtro_pluvial", "first_flush", "motobomba"}


def test_todo_tipo_tem_bloco_dxf():
    doc = ezdxf.new()
    register_plan_blocks(doc)
    faltam = [item["cad_block"] for item in COMPONENT_TYPES if item["cad_block"] not in doc.blocks]
    assert not faltam


def test_todo_tipo_tem_familia_no_revit():
    mapa = json.loads((RAIZ / "integrations" / "revit" / "family_mapping.json").read_text(encoding="utf-8"))
    assert not [t for t in TIPOS if t not in mapa]


@pytest.mark.parametrize("tabela, nome", [(_TYPE_LABELS, "esquema 3D"), (_TYPE_NAMES, "volumetria"), (_COLORS, "cores")])
def test_todo_tipo_tem_nome_e_cor(tabela, nome):
    assert not [t for t in TIPOS if t not in tabela], nome


def test_todo_acessorio_tem_ficha_descritiva():
    assert not [t for t in TIPOS if t not in COM_FICHA_PROPRIA and t not in _ACCESSORY_INFO]


def test_todo_tipo_tem_modelo_no_visualizador():
    """Sem modelo, a peça vira uma caixa arredondada genérica no WebGL."""
    fonte = (RAIZ / "web" / "volumetria" / "src" / "viewer.js").read_text(encoding="utf-8")
    faltam = [t for t in TIPOS if f'"{t}"' not in fonte and f"{t}:" not in fonte and not t.startswith("registro")]
    assert not faltam
