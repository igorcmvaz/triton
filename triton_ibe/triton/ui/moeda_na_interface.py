"""A moeda do projeto nos textos fixos da interface.

Os textos-fonte do catálogo estão em reais: «CAPEX (R$)», «Tarifa Água (R$/m³)»,
«Imposto fixo (R$/mês):». Os valores calculados já saem com o símbolo da moeda do
projeto (Etapa 4), mas cabeçalhos de tabela, rótulos, itens de lista e dicas ficavam em
reais na International e na Portugal, ao lado de valores em euros.

`aplicar_moeda` percorre um widget e troca «R$» pelo símbolo escolhido. Guarda o texto
original de cada campo, de modo que trocar a moeda de novo (de euro para dólar, na
International) parte sempre do texto em reais; um texto que a própria tela reescreveu
depois da última troca é tomado como o novo original. Quem decide se a troca se aplica é
quem chama: a janela principal só a usa fora da Edição Brasil, em que a moeda é o real.

Ficam de fora o seletor de moeda (que oferece o real pelo nome) e os navegadores de texto
da documentação, que citam valores brasileiros como exemplo.
"""

from __future__ import annotations

import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractButton, QComboBox, QDoubleSpinBox, QGroupBox, QLabel,
    QLineEdit, QSpinBox, QTableWidget, QTextEdit, QWidget,
)

REAL = "R$"
#: O código «BRL» que as cadeias em inglês do catálogo trazem no lugar do «R$» («Net NPV (BRL)»).
_CODIGO_REAL = re.compile(r"(?<![A-Za-z])BRL(?![A-Za-z])")

#: Etiqueta que acompanha a moeda ainda não escolhida (código ISO «XXX»: sem moeda).
SEM_MOEDA = "¤"

#: Propriedade que exclui um widget (e o que ele contém) da troca.
MOEDA_FIXA = "moeda_fixa"

_PAPEL_ORIGINAL = int(Qt.UserRole) + 731
_PAPEL_ULTIMO = int(Qt.UserRole) + 732


def _trocar(atual: str, original, ultimo, simbolo: str, codigo: str | None = None):
    """(novo texto, original) — o original é o atual se a tela o reescreveu."""
    if not isinstance(atual, str):
        return None, original
    if atual != ultimo or not isinstance(original, str):
        original = atual
    if REAL not in original and not _CODIGO_REAL.search(original):
        return None, original
    etiqueta = codigo if codigo and codigo != "XXX" else simbolo
    return _CODIGO_REAL.sub(etiqueta, original.replace(REAL, simbolo)), original


def _no_widget(w: QWidget, campo: str, ler, escrever, simbolo: str, codigo: str | None = None) -> None:
    chave_o, chave_u = f"_moeda_{campo}_original", f"_moeda_{campo}_ultimo"
    atual = ler()
    if not atual and not w.property(chave_o):
        return
    novo, original = _trocar(atual, w.property(chave_o), w.property(chave_u), simbolo, codigo)
    if novo is None:
        return
    w.setProperty(chave_o, original)
    if novo != atual:
        escrever(novo)
    w.setProperty(chave_u, novo)


def _no_item(ler_dado, gravar_dado, atual: str, escrever, simbolo: str, codigo: str | None = None) -> None:
    novo, original = _trocar(atual, ler_dado(_PAPEL_ORIGINAL), ler_dado(_PAPEL_ULTIMO), simbolo, codigo)
    if novo is None:
        return
    gravar_dado(_PAPEL_ORIGINAL, original)
    if novo != atual:
        escrever(novo)
    gravar_dado(_PAPEL_ULTIMO, novo)


def _excluido(w: QWidget, raiz: QWidget) -> bool:
    p = w
    while p is not None:
        if p.property(MOEDA_FIXA):
            return True
        if p is raiz:
            return False
        p = p.parentWidget()
    return False


def aplicar_moeda(raiz: QWidget, simbolo: str, codigo: str | None = None) -> None:
    """Troca «R$» por `simbolo` (e o «BRL» das cadeias em inglês pelo `codigo`) nos textos fixos de `raiz`."""
    if raiz is None or not simbolo:
        return
    for w in [raiz] + raiz.findChildren(QWidget):
        if isinstance(w, QTextEdit) or _excluido(w, raiz):
            continue
        _no_widget(w, "dica", w.toolTip, w.setToolTip, simbolo, codigo)
        if isinstance(w, (QLabel, QAbstractButton)):
            _no_widget(w, "texto", w.text, w.setText, simbolo, codigo)
        elif isinstance(w, QGroupBox):
            _no_widget(w, "titulo", w.title, w.setTitle, simbolo, codigo)
        elif isinstance(w, QLineEdit) and not w.isReadOnly():
            _no_widget(w, "exemplo", w.placeholderText, w.setPlaceholderText, simbolo, codigo)
        elif isinstance(w, (QDoubleSpinBox, QSpinBox)):
            _no_widget(w, "prefixo", w.prefix, w.setPrefix, simbolo, codigo)
            _no_widget(w, "sufixo", w.suffix, w.setSuffix, simbolo, codigo)
        elif isinstance(w, QComboBox):
            for i in range(w.count()):
                _no_item(lambda papel, i=i: w.itemData(i, papel),
                         lambda papel, valor, i=i: w.setItemData(i, valor, papel),
                         w.itemText(i), lambda t, i=i: w.setItemText(i, t), simbolo, codigo)
        elif isinstance(w, QTableWidget):
            for j in range(w.columnCount()):
                item = w.horizontalHeaderItem(j)
                if item is not None:
                    _no_item(item.data, item.setData, item.text(), item.setText, simbolo, codigo)
