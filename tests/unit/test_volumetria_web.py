"""O visualizador WebGL da volumetria: pacote em dia, licenças e dados da cena.

O pacote ``netuno/data/volumetria/netuno_volumetria.js`` é gerado de
``web/volumetria/src/viewer.js`` e versionado, para compilar o programa sem
Node. O risco é o de sempre com arquivo gerado: mudar o fonte e esquecer de
regerar. O cabeçalho do pacote leva o SHA-256 do fonte, e é isso que se confere.
"""

import hashlib
import re
from pathlib import Path

import pytest

from netuno.core.volumetry import build_volumetry
from netuno.core.volumetry_export import VIEWER_BUNDLE, VIEWER_DIR, VIEWER_SKY, scene_payload, viewer_html

RAIZ = Path(__file__).resolve().parents[2]
FONTE = RAIZ / "web" / "volumetria" / "src" / "viewer.js"


def _projeto():
    from netuno.core.study_layout import generate_study_layout

    return {"project_name": "Casa exemplo", **generate_study_layout({"lower_vol": 8000, "area": 150})}


def test_o_pacote_corresponde_ao_fonte():
    """Se falhar: cd web/volumetria && npm ci && npm run build."""
    cabecalho = VIEWER_BUNDLE.read_text(encoding="utf-8")[:600]
    registrado = re.search(r"fonte-sha256: ([0-9a-f]{64})", cabecalho).group(1)
    assert registrado == hashlib.sha256(FONTE.read_bytes()).hexdigest()


def test_o_pacote_leva_a_licenca_do_three_js_e_nao_fecha_o_script():
    texto = VIEWER_BUNDLE.read_text(encoding="utf-8")
    assert "three.js" in texto[:600] and "MIT License" in texto[:2000]
    assert "</script" not in texto.lower()
    assert "NetunoVolumetria" in texto


def test_os_assets_de_terceiros_tem_licenca_declarada():
    licencas = (VIEWER_DIR / "LICENCAS.md").read_text(encoding="utf-8")
    assert "CC0" in licencas and "Poly Haven" in licencas and "MIT License" in licencas
    assert VIEWER_SKY.read_bytes()[:10] == b"#?RADIANCE"


def test_a_cena_leva_o_que_o_visualizador_precisa_para_desenhar_as_pecas():
    dados = scene_payload(build_volumetry(_projeto()))
    por_chave = {s["key"]: s for s in dados["solids"]}
    assert por_chave["CI-01"]["type"] == "cisterna_inferior"
    assert por_chave["B-01"]["type"] == "motobomba"
    assert por_chave["CI-01"]["box"][0][2] < 0  # a cisterna é enterrada: o fundo fica abaixo da cota 0
    tubos = [s for s in dados["solids"] if s["kind"] == "pipe"]
    assert tubos and all(len(t["axis"]) == 7 and t["system"] and t["dn"] > 0 for t in tubos)
    # O DN real não é o raio ampliado do prisma: o visualizador precisa dos dois.
    assert all(t["dn"] / 2000.0 <= t["axis"][6] + 1e-9 for t in tubos)
    sistemas = {s["id"] for s in dados["systems"]}
    assert {t["system"] for t in tubos} <= sistemas


def test_o_html_e_uma_pagina_unica_com_textos_traduzidos():
    html = viewer_html(build_volumetry(_projeto()), {"titulo": "3D Massing", "medir": "Measure"})
    assert html.count("<script") == 1 and html.count("</script>") == 1
    assert '"medir":"Measure"' in html
    assert "<title>3D Massing — Casa exemplo</title>" in html


def test_o_nome_do_projeto_nao_e_lido_como_marcador():
    projeto = _projeto()
    projeto["project_name"] = "__SKY__ __BUNDLE__"
    html = viewer_html(build_volumetry(projeto))
    assert html.count("NetunoVolumetria.mount(") == 1
    assert "__SKY__ __BUNDLE__" in html


@pytest.mark.parametrize("valor, esperado", [("1", False), ("", True), ("0", True)])
def test_a_variavel_de_ambiente_desliga_o_visualizador_web(monkeypatch, valor, esperado):
    pytest.importorskip("PySide6")
    from netuno.ui import volumetry_web

    monkeypatch.setenv("NETUNO_VOLUMETRIA_SIMPLES", valor)
    if esperado:
        pytest.importorskip("PySide6.QtWebEngineWidgets")
    assert volumetry_web.web_disponivel() is esperado


def test_a_volumetria_abre_leve_so_com_os_rotulos():
    """Edificação, terreno, fluxo, raio-X, céu e sombras pesam: ligam-se no botão."""
    import re
    from pathlib import Path

    fonte = (Path(__file__).resolve().parents[2] / "web" / "volumetria" / "src" / "viewer.js").read_text(encoding="utf-8")
    padrao = dict(re.findall(r"(\w+): (true|false)", re.search(r"this\.show = \{([^}]*)\}", fonte).group(1)))
    assert padrao == {"building": "false", "ground": "false", "labels": "true", "flow": "false",
                      "xray": "false", "sky": "false", "shadows": "false"}
