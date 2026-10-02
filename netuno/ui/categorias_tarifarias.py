"""O seletor de categoria tarifária, igual no Gestor de Tarifas e no diálogo econômico.

Oferece as cinco categorias, mas só deixa escolher as que têm tabela oficial coletada
para o município. As demais aparecem desabilitadas, com o motivo: o programa não
estima uma categoria a partir de outra, e quem precisa dela lança a tabela no modo
Personalizado.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from netuno.core.tariffs_database import CATEGORIAS_TARIFARIAS, categorias_coletadas
from netuno.ui.translation import tr


def preencher_categorias(combo, dados: Optional[Dict[str, Any]], selecionada: str = "residencial") -> str:
    """Repovoa o combo para o município de `dados` e devolve a categoria que ficou escolhida."""
    disponiveis = categorias_coletadas(dados) or ["residencial"]
    if selecionada not in disponiveis:
        selecionada = "residencial"
    bloqueado = combo.blockSignals(True)
    combo.clear()
    for cid, info in CATEGORIAS_TARIFARIAS.items():
        rotulo = f"{info['icone']} {tr(info['nome'])}"
        if cid not in disponiveis:
            rotulo += tr(" — tabela não coletada")
        combo.addItem(rotulo, cid)
        if cid not in disponiveis:
            item = combo.model().item(combo.count() - 1)
            item.setEnabled(False)
            item.setToolTip(tr("A tabela oficial desta categoria ainda não foi coletada para o "
                               "município. Lance a estrutura da concessionária no modo Personalizado."))
    combo.setCurrentIndex(max(0, combo.findData(selecionada)))
    combo.blockSignals(bloqueado)
    return selecionada
