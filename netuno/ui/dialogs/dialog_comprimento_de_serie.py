# -*- coding: utf-8 -*-
"""A série de chuva é longa o bastante para este projeto?

Mostra o resultado da análise de `netuno/core/comprimento_de_serie.py`: o veredito
em uma frase, a frequência de resultados semelhantes por comprimento de série, e
os critérios usados, para que o número possa ser citado num trabalho.

A análise completa percorre todas as janelas possíveis e é cara; aqui ela roda
com um número declarado de janelas sorteadas por comprimento, o que responde em
segundos. O modo exaustivo fica na linha de comando (`netuno series-length`).
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QHeaderView, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QVBoxLayout,
)

from netuno.core.comprimento_de_serie import ResultadoDoComprimento

from netuno.ui.translation import tr


class DialogComprimentoDeSerie(QDialog):
    """Janela de resultado, sem entrada: quem decide os parâmetros é a aba."""

    def __init__(self, resultado: ResultadoDoComprimento, parent=None):
        super().__init__(parent)
        self.resultado = resultado
        self.setWindowTitle(tr("Comprimento representativo da série"))
        self.setMinimumWidth(560)
        self._montar()

    def _montar(self) -> None:
        r = self.resultado
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        veredito = QLabel(r.resumo())
        veredito.setWordWrap(True)
        veredito.setStyleSheet(
            "font-size: 14px; font-weight: 600; padding: 10px; border-radius: 6px; "
            + ("background-color: rgba(34,197,94,0.14);" if r.serie_e_representativa
               else "background-color: rgba(249,115,22,0.16);"))
        layout.addWidget(veredito)

        premissas = QLabel(tr(
            "Volume ideal com a série inteira: {volume} L, com {potencial}% de economia. "
            "Uma janela conta como semelhante quando elege o mesmo volume ideal e fica "
            "a até {tolerancia} pontos percentuais do potencial; o comprimento "
            "representativo é o menor que alcança {confianca}% de janelas semelhantes e "
            "se mantém nos comprimentos maiores."
        ).format(volume=f"{r.volume_ideal_l:,.0f}".replace(",", "."),
                 potencial=f"{r.potencial_no_ideal_pct:.2f}".replace(".", ","),
                 tolerancia=f"{r.tolerancia_pp:.1f}".replace(".", ","),
                 confianca=f"{r.confianca_pct:.0f}"))
        premissas.setWordWrap(True)
        premissas.setStyleSheet("font-size: 12px; color: #64748b;")
        layout.addWidget(premissas)

        tabela = QTableWidget()
        tabela.setColumnCount(3)
        tabela.setHorizontalHeaderLabels([tr("Anos de série"), tr("Janelas testadas"),
                                          tr("Resultados semelhantes")])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabela.verticalHeader().setVisible(False)
        tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        itens = sorted(r.frequencia_por_comprimento.items())
        tabela.setRowCount(len(itens))
        for linha, (anos, frequencia) in enumerate(itens):
            for coluna, texto in enumerate((
                    str(anos), str(r.janelas_por_comprimento[anos]),
                    f"{frequencia:.1f}%".replace(".", ","))):
                item = QTableWidgetItem(texto)
                item.setTextAlignment(Qt.AlignCenter)
                if anos == r.comprimento_representativo_anos:
                    fonte = item.font()
                    fonte.setBold(True)
                    item.setFont(fonte)
                tabela.setItem(linha, coluna, item)
        tabela.setMinimumHeight(240)
        layout.addWidget(tabela)

        amostra = (tr("Janelas sorteadas por comprimento: {n}, com semente {s}.")
                   .format(n=r.amostra_por_comprimento, s=r.semente)
                   if r.amostra_por_comprimento else
                   tr("Todas as janelas possíveis foram testadas."))
        rodape = QLabel(amostra + " " + tr(
            "O método é o de Geraldi e Ghisi; a resposta é deste projeto, e muda com a "
            "fração atendível e com a demanda."))
        rodape.setWordWrap(True)
        rodape.setStyleSheet("font-size: 11px; color: #94a3b8;")
        layout.addWidget(rodape)

        botoes = QHBoxLayout()
        botoes.addStretch()
        fechar = QPushButton(tr("Fechar"))
        fechar.clicked.connect(self.accept)
        botoes.addWidget(fechar)
        layout.addLayout(botoes)

    def texto_para_relatorio(self) -> str:
        """A frase que se copia para um trabalho publicado."""
        r = self.resultado
        if r.comprimento_representativo_anos is None:
            return r.resumo()
        return (f"{r.resumo()} Critério: {r.confianca_pct:.0f}% das janelas com o mesmo "
                f"volume ideal ({r.volume_ideal_l:,.0f} L) e potencial dentro de "
                f"{r.tolerancia_pp:.1f} pontos percentuais.".replace(",", "."))
