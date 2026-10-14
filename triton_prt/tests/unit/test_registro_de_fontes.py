"""Nada entra em tarifas/fontes sem passar pelo registro, e o registro não mente.

O usuário manda PDFs ao longo das sessões; o registro é o que impede reenviar e
retranscrever o mesmo material. Estes testes garantem que todo arquivo guardado está
registrado, que a impressão digital confere e que nenhum arquivo aparece duas vezes.
"""

from __future__ import annotations

import hashlib
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTES = os.path.join(RAIZ, "tarifas", "fontes")
REGISTRO = json.load(open(os.path.join(FONTES, "registro.json"), encoding="utf-8"))["itens"]
NAO_SAO_FONTES = {"registro.json", "REGISTRO.md", "LEIAME.md"}


def _sha(caminho):
    return hashlib.sha256(open(caminho, "rb").read()).hexdigest()


def test_nenhum_arquivo_registrado_duas_vezes():
    shas = [i["sha256"] for i in REGISTRO]
    assert len(shas) == len(set(shas))
    assert [i["id"] for i in REGISTRO] == list(range(1, len(REGISTRO) + 1))


def test_todo_arquivo_guardado_esta_no_registro():
    guardados = {i["guardado_em"] for i in REGISTRO if i["guardado_em"]}
    for pasta, _dirs, nomes in os.walk(FONTES):
        for nome in nomes:
            if nome in NAO_SAO_FONTES:
                continue
            rel = os.path.relpath(os.path.join(pasta, nome), RAIZ).replace(os.sep, "/")
            # Os recursos de uma página salva («Página completa») vivem em <página>_files/
            # e entram com ela: basta a página estar registrada.
            anexa = next((p for p in rel.split("/") if p.endswith("_files")), None)
            if anexa:
                pagina = rel[:rel.index(anexa)] + anexa[:-len("_files")]
                assert any(g.startswith(pagina + ".htm") for g in guardados), f"{rel}: página sem registro"
                continue
            assert rel in guardados, f"{rel} está em tarifas/fontes sem registro"


def test_a_impressao_digital_confere():
    for i in REGISTRO:
        if i["guardado_em"]:
            assert _sha(os.path.join(RAIZ, i["guardado_em"])) == i["sha256"], i["arquivo"]
        else:
            assert i["nao_guardado_motivo"], i["arquivo"]
