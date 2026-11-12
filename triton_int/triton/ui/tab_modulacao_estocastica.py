# -*- coding: utf-8 -*-
"""Ferramenta 13 — Modulação Probabilística.

Refaz o estudo pronto com as variáveis que o usuário escolhe no catálogo sorteadas
(núcleo em `triton/core/modulacao_estocastica.py`, o mesmo do comando
`triton probabilistic-study`). O estudo determinístico não muda: esta tela só mostra a
robustez dele.

A tela tem quatro blocos — variáveis, distribuições, execução e resultados — e a
apresentação dos resultados segue a de um artigo: a Tabela 1 diz o que de fato foi
sorteado; a Tabela 2 resume o volume escolhido pelo estudo (estudo determinístico, média,
desvio-padrão, coeficiente de variação e percentis), com a probabilidade de o investimento
se pagar e o seu intervalo de 95% (Wilson); as figuras, numeradas e legendadas fora do
gráfico, trazem os valores escritos; a Tabela 3 dá os percentis de todos os volumes. O
layout se reorganiza com a largura, sem rolagem lateral.
"""

from __future__ import annotations

import copy
import csv
import json
import re
import time
from typing import Any, Dict, List, Optional

import numpy as np
from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QMessageBox, QProgressBar, QPushButton, QScrollArea, QSizePolicy, QSpinBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from triton.core import modulacao_estocastica as M
from triton.core.parser import format_ptbr
from triton.ui.charts import TritonBaseChart
from triton.ui.translation import get_current_lang, tr

TIPOS_NA_TELA = (("normal", "Normal"), ("lognormal", "Lognormal"), ("triangular", "Triangular"), ("uniforme", "Uniforme"))
COR = {"faixa": "#a7f3d0", "mediana": "#047857", "base": "#b91c1c", "eixo": "#334155", "grade": "#cbd5e1",
       "tecnico": "#1d4ed8", "economico": "#b45309", "topsis": "#0f766e", "co2": "#6d28d9"}
#: Larguras (px) a partir das quais os cartões ficam em 3 e 2 colunas, e as figuras em 2.
COLUNAS_3, COLUNAS_2, FIGURAS_2 = 1050, 700, 900
#: Os grupos de variáveis em quatro colunas só quando os rótulos cabem inteiros.
GRUPOS_4 = 1400
#: Abaixo disto, o viés do η² por decis ((classes − 1)/N ≈ 0,03 com 300) passa a pesar na leitura.
REALIZACOES_PARA_LER_O_ETA2 = 300
#: Colunas da lista de modelos climáticos conforme a largura.
MODELOS_5, MODELOS_3 = 1100, 700


#: Símbolo da moeda do projeto (Etapa 4), atualizado pela ferramenta a cada desenho.
MOEDA = "R$"


def _m(texto: str) -> str:
    """O texto com a moeda do projeto no lugar de «R$» (os textos-fonte estão em reais)."""
    return texto.replace("R$", MOEDA) if MOEDA != "R$" else texto


#: Descrições do catálogo que falam em reais, na versão para outra moeda.
_DESCRICAO_EM_OUTRA_MOEDA = {
    "fator_tarifa": "Multiplica todos os valores monetários da estrutura de água (faixas, parcela fixa, "
                    "conta mínima) e o esgoto cobrado em valor; o esgoto em % da água acompanha a água.",
}


def _descricao(var) -> str:
    """A descrição da variável, na moeda do projeto."""
    if MOEDA != "R$" and var.chave in _DESCRICAO_EM_OUTRA_MOEDA:
        return tr(_DESCRICAO_EM_OUTRA_MOEDA[var.chave])
    return _m(tr(var.descricao))


def _br(x, casas=0):
    if x is None:
        return "—"
    if get_current_lang() in ("pt", "es"):
        return format_ptbr(float(x), casas)
    return f"{float(x):,.{casas}f}"


def _m3(volume_l: float) -> str:
    return _br(volume_l / 1000.0, 1 if volume_l % 1000 else 0)


def _formatar_eixo(eixo, casas: int = 0):
    """Números do eixo com o separador decimal da língua da interface."""
    from matplotlib.ticker import FuncFormatter
    eixo.set_major_formatter(FuncFormatter(lambda x, _p: _br(x, casas)))


def _estilo(ax):
    ax.set_facecolor("#ffffff")
    ax.tick_params(colors=COR["eixo"], labelsize=7.5)
    ax.grid(True, linestyle=":", alpha=0.7, color=COR["grade"])
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#94a3b8")


def _rotulo_eixo(ax, x: str = None, y: str = None):
    if x:
        ax.set_xlabel(x, fontsize=8, color=COR["eixo"])
    if y:
        ax.set_ylabel(y, fontsize=8, color=COR["eixo"])


def _rotulo_variavel(chave: str) -> str:
    v = M.CATALOGO[chave]
    return f"{tr(v.rotulo)} ({_m(tr(v.unidade))})"


class _Trabalhador(QObject):
    progresso = Signal(int, int)
    concluido = Signal(object)
    falhou = Signal(str)

    def __init__(self, cfg, precip, parametros, amostras, semente, pesos, ambiental, partes=None):
        super().__init__()
        self.args = (cfg, precip, parametros)
        self.kw = dict(amostras=amostras, semente=semente, pesos=pesos, ambiental=ambiental, partes=partes)
        self._cancelar = False

    def cancelar(self):
        self._cancelar = True

    def rodar(self):
        try:
            dados = M.simular(*self.args, ao_progredir=lambda a, b: self.progresso.emit(a, b),
                              cancelar=lambda: self._cancelar, **self.kw)
            self.concluido.emit(dados)
        except Exception as e:  # a mensagem vai para a tela; a análise não derruba o programa
            self.falhou.emit(str(e))


# ============================================================================ figuras
class _Grafico(TritonBaseChart):
    """Base das figuras da ferramenta: sem título interno (a legenda fica fora, numerada)."""

    def __init__(self, nome, parent=None, aspect=(16, 10)):
        super().__init__(nome, parent, aspect_ratio=aspect)
        self.set_canvas_height_range(240, 380)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.dados: Any = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.dados is not None:  # refaz o layout do gráfico no tamanho novo
            self.desenhar(self.dados)

    def desenhar(self, dados):
        self.dados = dados
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        _estilo(ax)
        if self._plotar(ax, dados) is False:
            self.dados = None
            return
        self.figure.tight_layout(pad=0.8)
        self.safe_draw()

    def _plotar(self, ax, dados):  # pragma: no cover - sobrescrito
        raise NotImplementedError


class _GraficoCurva(_Grafico):
    """A densidade da distribuição escolhida, por sorteio (miniatura do cartão)."""

    def __init__(self, parent=None):
        super().__init__("densidade", parent, aspect=(16, 6))
        self.set_canvas_height_range(80, 130)

    def _plotar(self, ax, dados):
        dist, unidade, casas = dados
        try:
            dist.validar()
            valores = dist.sortear(np.random.default_rng(0), 4000)
            ax.hist(valores, bins=30, density=True, color=COR["faixa"], edgecolor=COR["mediana"], linewidth=0.3)
            ax.axvline(float(np.mean(valores)), color=COR["mediana"], linewidth=1.1)
            p5, p95 = np.percentile(valores, [5, 95])
            ax.text(0.99, 0.95, f"P5 {_br(p5, casas)} · P95 {_br(p95, casas)}", transform=ax.transAxes,
                    ha="right", va="top", fontsize=6.5, color=COR["eixo"])
        except ValueError as e:
            ax.text(0.5, 0.5, str(e), ha="center", va="center", fontsize=7, color="#b91c1c", wrap=True,
                    transform=ax.transAxes)
        ax.set_yticks([])
        ax.grid(False)
        _formatar_eixo(ax.xaxis, casas)
        _rotulo_eixo(ax, x=unidade)


class _GraficoLeque(_Grafico):
    """Faixa P5–P95, mediana e estudo determinístico ao longo dos volumes; valores no volume escolhido."""

    def __init__(self, nome, chave, rotulo_y, casas_y=0, parent=None):
        super().__init__(nome, parent)
        self.chave, self.rotulo_y, self.casas_y = chave, rotulo_y, casas_y

    def _plotar(self, ax, dados):
        linhas = [v for v in dados["por_volume"] if v[self.chave]["p50"] is not None]
        if not linhas:
            self.plot_empty(tr("Sem dados"))
            return False
        x = [v["volume_l"] / 1000.0 for v in linhas]
        ax.fill_between(x, [v[self.chave]["p5"] for v in linhas], [v[self.chave]["p95"] for v in linhas],
                        color=COR["faixa"], alpha=0.85, linewidth=0, label=tr("P5–P95"))
        ax.plot(x, [v[self.chave]["p50"] for v in linhas], color=COR["mediana"], linewidth=1.8,
                label=tr("Mediana (P50)"))
        ax.plot(x, [v["base"][self.chave] for v in linhas], color=COR["base"], linewidth=1.1, linestyle="--",
                label=tr("Estudo determinístico"))
        ref = dados.get("volume_de_referencia_l")
        linha_ref = next((v for v in linhas if v["volume_l"] == ref), None)
        if linha_ref is not None:
            xr = ref / 1000.0
            ax.axvline(xr, color="#64748b", linewidth=0.8, linestyle=":")
            for p, va in (("p95", "bottom"), ("p50", "center"), ("p5", "top")):
                y = linha_ref[self.chave][p]
                ax.plot([xr], [y], marker="o", markersize=3, color=COR["mediana"])
                ax.annotate(f"{p.upper()} {_br(y, self.casas_y)}", (xr, y), xytext=(6, 0),
                            textcoords="offset points", fontsize=7, va=va, color=COR["eixo"],
                            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85))
        if self.chave == "vpl_brl":
            ax.axhline(0, color=COR["eixo"], linewidth=0.7)
        ax.set_xlim(0, max(x))
        from matplotlib.ticker import MaxNLocator
        # Marcas redondas (1, 2, 5 ou 10 m³), nunca 2,5 arredondado para 2.
        ax.xaxis.set_major_locator(MaxNLocator(nbins=10, steps=[1, 2, 5, 10]))
        _formatar_eixo(ax.xaxis, 0 if max(x) >= 5 else 1)
        _formatar_eixo(ax.yaxis, self.casas_y)
        _rotulo_eixo(ax, tr("Volume do reservatório inferior (m³)"), _m(self.rotulo_y))
        ax.legend(fontsize=7, loc="lower right", frameon=False)


class _GraficoHistograma(_Grafico):
    """A distribuição do VPL no volume escolhido, com o estudo determinístico, a mediana e P(VPL > 0)."""

    def _plotar(self, ax, dados):
        valores = [a["vpl_ref_brl"] for a in dados.get("amostras", []) if a.get("vpl_ref_brl") is not None]
        if len(valores) < 3:
            self.plot_empty(tr("São precisas ao menos 3 realizações"))
            return False
        ax.hist(valores, bins=min(30, max(8, len(valores) // 6)), color=COR["faixa"], edgecolor=COR["mediana"],
                linewidth=0.4)
        ax.axvline(0, color=COR["eixo"], linewidth=0.8)
        ref = dados.get("referencia") or {}
        base = ref.get("base", {}).get("vpl_brl")
        if base is not None:
            ax.axvline(base, color=COR["base"], linestyle="--", linewidth=1.1,
                       label=f"{tr('Estudo determinístico')}: {_br(base)}")
        mediana = float(np.median(valores))
        ax.axvline(mediana, color=COR["mediana"], linewidth=1.6, label=f"{tr('Mediana (P50)')}: {_br(mediana)}")
        prob = (ref.get("prob_vpl_positivo") or {}).get("pct")
        if prob is not None:
            ax.text(0.98, 0.97, f"P(VPL > 0) = {_br(prob, 1)}%", transform=ax.transAxes, ha="right", va="top",
                    fontsize=8, fontweight="bold", color=COR["eixo"])
        _formatar_eixo(ax.xaxis, 0)
        _rotulo_eixo(ax, _m(tr("VPL (R$)")), tr("Realizações"))
        ax.legend(fontsize=7, frameon=False, loc="upper left")


class _GraficoFrequencia(_Grafico):
    """Com que frequência cada volume é o ideal técnico, o ótimo econômico e o vencedor TOPSIS."""

    def _plotar(self, ax, dados):
        freq = dados["frequencia_pct"]
        chaves = (("ideal_tecnico", tr("Ideal técnico"), COR["tecnico"]),
                  ("otimo_economico", tr("Ótimo econômico (payback)"), COR["economico"]),
                  ("vencedor_topsis", tr("Vencedor TOPSIS"), COR["topsis"]))
        rotulos = sorted({k for c, _, _ in chaves for k in freq[c]},
                         key=lambda k: (k == "nenhum", float(k) if k != "nenhum" else 0.0))
        if not rotulos:
            self.plot_empty(tr("Sem dados"))
            return False
        pos = np.arange(len(rotulos))
        largura = 0.27
        for i, (c, nome, cor) in enumerate(chaves):
            alturas = [freq[c].get(r, 0.0) for r in rotulos]
            barras = ax.bar(pos + (i - 1) * largura, alturas, largura, color=cor, label=nome)
            for b, h in zip(barras, alturas):
                if h >= 1:
                    ax.text(b.get_x() + b.get_width() / 2, h + 1, _br(h), ha="center", va="bottom", fontsize=6,
                            color=COR["eixo"])
        ax.set_xticks(pos)
        ax.set_xticklabels([tr("nenhum") if r == "nenhum" else _m3(float(r)) for r in rotulos], fontsize=7)
        ax.set_ylim(0, 110)
        ax.grid(True, axis="y", linestyle=":", alpha=0.7, color=COR["grade"])
        ax.grid(False, axis="x")
        _formatar_eixo(ax.yaxis, 0)
        _rotulo_eixo(ax, tr("Volume do reservatório inferior (m³)"), tr("Frequência (%)"))
        ax.legend(fontsize=7, frameon=False, loc="upper right")


class _GraficoSensibilidade(_Grafico):
    """ρ de Spearman de cada variável sorteada com a economia e com o VPL, ordenado pelo |ρ| do VPL."""

    def __init__(self, nome, parent=None):
        super().__init__(nome, parent)

    def _plotar(self, ax, dados):
        sens = dados.get("sensibilidade_spearman") or {}
        if not sens:
            self.plot_empty(tr("São precisas ao menos 3 realizações"))
            return False
        nomes = sorted(sens, key=lambda n: abs(sens[n]["vpl_brl"] or sens[n]["potencial_pct"] or 0.0))
        pos = np.arange(len(nomes))
        series = ((0.2, "potencial_pct", tr("Economia de água potável"), COR["mediana"]),
                  (-0.2, "vpl_brl", tr("VPL"), COR["economico"]))
        for desloc, chave, rotulo, cor in series:
            valores = [sens[n][chave] for n in nomes]
            ax.barh(pos + desloc, [v or 0.0 for v in valores], 0.38, color=cor, label=rotulo)
            for y, v in zip(pos + desloc, valores):
                if v is not None:
                    ax.text(v + (0.03 if v >= 0 else -0.03), y, _br(v, 2), va="center",
                            ha="left" if v >= 0 else "right", fontsize=6.5, color=COR["eixo"])
        ax.set_yticks(pos)
        ax.set_yticklabels([tr(M.CATALOGO[n].rotulo) for n in nomes], fontsize=7.5)
        ax.axvline(0, color=COR["eixo"], linewidth=0.8)
        ax.set_xlim(-1.25, 1.25)
        ax.grid(True, axis="x", linestyle=":", alpha=0.7, color=COR["grade"])
        ax.grid(False, axis="y")
        _formatar_eixo(ax.xaxis, 1)
        _rotulo_eixo(ax, tr("ρ de Spearman"))
        ax.legend(fontsize=7, frameon=False, loc="lower right")
        # Altura acompanha o número de variáveis
        self.set_canvas_height_range(240, max(380, 60 + 34 * len(nomes)))


class _GraficoConvergencia(_Grafico):
    """Média acumulada do VPL no volume escolhido e o seu intervalo de 95% (Monte Carlo)."""

    def _plotar(self, ax, dados):
        conv = dados.get("convergencia") or []
        if len(conv) < 2:
            self.plot_empty(tr("São precisas ao menos 10 realizações"))
            return False
        k = [c["realizacoes"] for c in conv]
        ax.fill_between(k, [c["ic95_inf"] for c in conv], [c["ic95_sup"] for c in conv], color=COR["faixa"],
                        alpha=0.85, linewidth=0, label=tr("IC 95% da média"))
        ax.plot(k, [c["vpl_media"] for c in conv], color=COR["mediana"], linewidth=1.6, label=tr("Média acumulada"))
        ultimo = conv[-1]
        meia = (ultimo["ic95_sup"] - ultimo["ic95_inf"]) / 2.0
        ax.annotate(f"{_br(ultimo['vpl_media'])} ± {_br(meia)}", (k[-1], ultimo["vpl_media"]), xytext=(-5, 8),
                    textcoords="offset points", ha="right", fontsize=7, color=COR["eixo"])
        from matplotlib.ticker import MaxNLocator
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        _formatar_eixo(ax.yaxis, 0)
        _rotulo_eixo(ax, tr("Realizações"), _m(tr("VPL (R$)")))
        ax.legend(fontsize=7, frameon=False)


# ============================================================================ entrada
class _CartaoParametro(QGroupBox):
    """A distribuição, os parâmetros e a curva de uma variável escolhida."""

    def __init__(self, chave: str, parent=None):
        self.var = M.CATALOGO[chave]
        super().__init__(_rotulo_variavel(chave), parent)
        self.chave = chave
        self.casas = self.var.casas
        self.setToolTip(_descricao(self.var))
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        lay = QVBoxLayout(self)
        self.lbl_projeto = QLabel()
        self.lbl_projeto.setStyleSheet("color: #475569; font-size: 11px;")
        lay.addWidget(self.lbl_projeto)
        self.combo_tipo = QComboBox()
        self.combo_tipo.setMinimumContentsLength(8)
        self.combo_tipo.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        for k, rotulo in TIPOS_NA_TELA:
            self.combo_tipo.addItem(tr(rotulo), k)
        lay.addWidget(self.combo_tipo)
        grade = QGridLayout()
        self.campos: Dict[str, QDoubleSpinBox] = {}
        for i, (k, rotulo) in enumerate((("media", "Média"), ("desvio", "Desvio-padrão"), ("minimo", "Mínimo"),
                                         ("moda", "Moda"), ("maximo", "Máximo"),
                                         ("limite_inferior", "Limite inferior"),
                                         ("limite_superior", "Limite superior"))):
            spin = QDoubleSpinBox()
            spin.setRange(-1e6, 1e7)
            spin.setDecimals(max(self.casas, 2) if self.var.unidade in ("×", "—", "% ao mês") else self.casas)
            spin.setMinimumWidth(60)
            spin.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
            if k in ("limite_inferior", "limite_superior"):
                spin.setRange(-1e6 - 1, 1e7)
                spin.setSpecialValueText(tr("sem limite"))
            spin.valueChanged.connect(self.atualizar)
            lbl = QLabel(tr(rotulo))
            grade.addWidget(lbl, i, 0)
            grade.addWidget(spin, i, 1)
            self.campos[k] = spin
            spin._rotulo = lbl
        grade.setColumnStretch(1, 1)
        lay.addLayout(grade)
        self.curva = _GraficoCurva(self)
        lay.addWidget(self.curva)
        self.combo_tipo.currentIndexChanged.connect(self.atualizar)

    def definir(self, dist: M.Distribuicao, valor_projeto: Optional[float] = None):
        for spin in self.campos.values():
            spin.blockSignals(True)
        self.combo_tipo.setCurrentIndex(max(0, self.combo_tipo.findData(dist.tipo)))
        for k, spin in self.campos.items():
            valor = getattr(dist, k)
            spin.setValue(spin.minimum() if valor is None else float(valor))
        for spin in self.campos.values():
            spin.blockSignals(False)
        if valor_projeto is not None:
            self.lbl_projeto.setText(tr("No estudo: {0}").format(_br(valor_projeto, max(self.casas, 2)
                                                                       if self.var.unidade in ("×", "—") else self.casas)))
        self.atualizar()

    def distribuicao(self, variar: bool = True) -> M.Distribuicao:
        v = {k: s.value() for k, s in self.campos.items()}
        lim = lambda k: None if self.campos[k].value() == self.campos[k].minimum() else v[k]  # noqa: E731
        return M.Distribuicao(tipo=self.combo_tipo.currentData(), media=v["media"], desvio=v["desvio"],
                              minimo=v["minimo"], moda=v["moda"], maximo=v["maximo"],
                              limite_inferior=lim("limite_inferior"), limite_superior=lim("limite_superior"),
                              variar=variar)

    def atualizar(self, *_):
        tipo = self.combo_tipo.currentData()
        usados = {"normal": {"media", "desvio"}, "lognormal": {"media", "desvio"},
                  "triangular": {"minimo", "moda", "maximo"}, "uniforme": {"minimo", "maximo"}}[tipo]
        usados |= {"limite_inferior", "limite_superior"}
        for k, spin in self.campos.items():
            spin.setVisible(k in usados)
            spin._rotulo.setVisible(k in usados)
        self.curva.desenhar((self.distribuicao(), tr(self.var.unidade), self.casas))


def _legenda(texto: str) -> QLabel:
    """Legenda numerada acima da figura ou da tabela (padrão ABNT: título fora do gráfico)."""
    lbl = QLabel(texto)
    lbl.setWordWrap(True)
    lbl.setStyleSheet("font-size: 11px; color: #334155; padding-top: 8px;")
    return lbl


def _titulo(texto: str) -> QLabel:
    lbl = QLabel(f"<h3 style='margin:8px 0 2px 0'>{texto}</h3>")
    return lbl


def _tabela(colunas: List[str], minimo: int) -> QTableWidget:
    t = QTableWidget(0, len(colunas))
    t.setHorizontalHeaderLabels(colunas)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.horizontalHeader().setMinimumSectionSize(36)
    t.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    t.verticalHeader().setVisible(False)
    t.setEditTriggers(QTableWidget.NoEditTriggers)
    t.setWordWrap(True)
    t.setMinimumHeight(minimo)
    t.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
    return t


def _preencher(tabela: QTableWidget, linhas: List[List[str]], negrito: Optional[set] = None):
    tabela.setRowCount(len(linhas))
    for i, linha in enumerate(linhas):
        for j, texto in enumerate(linha):
            item = QTableWidgetItem(texto)
            if j:
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if negrito and i in negrito:
                fonte = item.font()
                fonte.setBold(True)
                item.setFont(fonte)
            tabela.setItem(i, j, item)
    tabela.resizeRowsToContents()
    altura = tabela.horizontalHeader().height() + sum(tabela.rowHeight(i) for i in range(len(linhas))) + 6
    tabela.setFixedHeight(min(max(altura, 80), 520))


# ============================================================================ a ferramenta
class TabModulacaoEstocastica(QWidget):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent or main_window)
        self.main_window = main_window
        self.resultado: Optional[Dict[str, Any]] = None
        self._thread: Optional[QThread] = None
        self._trabalhador: Optional[_Trabalhador] = None
        self._inicio = 0.0
        self._largura = 1200
        #: A triagem a que cada cartão corresponde: o cartão que o usuário não editou acompanha
        #: o estudo quando ele muda (outro projeto aberto, outro per capita na Etapa 2).
        self._triagens: Dict[str, M.Distribuicao] = {}
        self._um_volume = False
        self._montar()

    # ---------------------------------------------------------------- montagem
    def _montar(self):
        externo = QVBoxLayout(self)
        externo.setContentsMargins(0, 0, 0, 0)
        self.rolagem = QScrollArea()
        self.rolagem.setWidgetResizable(True)
        self.rolagem.setFrameShape(QFrame.NoFrame)
        self.rolagem.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        corpo = QWidget()
        corpo.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        lay = QVBoxLayout(corpo)
        lay.setContentsMargins(14, 10, 14, 14)
        self.rolagem.setWidget(corpo)
        externo.addWidget(self.rolagem)

        lay.addWidget(QLabel(f"<h2>🎲 {tr('Modulação Probabilística')}</h2>"))
        intro = QLabel(tr(
            "Refaz o estudo pronto muitas vezes, cada uma com as variáveis escolhidas sorteadas das suas "
            "distribuições, e mostra a robustez do resultado. O estudo determinístico não muda: as demais etapas, "
            "os relatórios e a linha de comando continuam com ele. As distribuições iniciais são de triagem, "
            "centradas no projeto; ajuste-as ao que se sabe da edificação."))
        intro.setWordWrap(True)
        lay.addWidget(intro)
        self.lbl_referencia = QLabel()
        self.lbl_referencia.setWordWrap(True)
        self.lbl_referencia.setStyleSheet("padding: 6px; border: 1px solid #cbd5e1; border-radius: 6px;")
        lay.addWidget(self.lbl_referencia)

        # 1. Variáveis
        lay.addWidget(_titulo(tr("1. O que variar")))
        dica = QLabel(tr("Marque as premissas incertas do projeto. As demais ficam com o valor do estudo."))
        dica.setWordWrap(True)
        lay.addWidget(dica)
        self.checks: Dict[str, QCheckBox] = {}
        self.caixas_grupo: List[QGroupBox] = []
        for grupo in M.GRUPOS:
            caixa = QGroupBox(tr(grupo))
            caixa.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
            vb = QVBoxLayout(caixa)
            for v in M.CATALOGO.values():
                if v.grupo != grupo:
                    continue
                chk = QCheckBox(_rotulo_variavel(v.chave))
                chk.setToolTip(_descricao(v))
                chk.toggled.connect(self._ao_marcar)
                vb.addWidget(chk)
                self.checks[v.chave] = chk
            vb.addStretch()
            self.caixas_grupo.append(caixa)
        self.grade_grupos = QGridLayout()
        lay.addLayout(self.grade_grupos)

        # Modelos climáticos: cada realização sorteia a série de um dos marcados.
        from triton.core.climate_database import CLIMATE_MODELS
        self.caixa_modelos = QGroupBox(tr("Modelos climáticos (CLIMBra)"))
        self.caixa_modelos.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        vb_modelos = QVBoxLayout(self.caixa_modelos)
        self.lbl_modelos = QLabel()
        self.lbl_modelos.setWordWrap(True)
        vb_modelos.addWidget(self.lbl_modelos)
        self.checks_modelos: Dict[str, QCheckBox] = {}
        for m in CLIMATE_MODELS:
            chk = QCheckBox(m)
            chk.toggled.connect(self._ao_marcar_modelo)
            self.checks_modelos[m] = chk
        self.grade_modelos = QGridLayout()
        vb_modelos.addLayout(self.grade_modelos)
        linha_modelos = QHBoxLayout()
        self.btn_todos_modelos = QPushButton(tr("Marcar todos"))
        self.btn_todos_modelos.clicked.connect(lambda: self._marcar_modelos(True))
        self.btn_nenhum_modelo = QPushButton(tr("Desmarcar todos"))
        self.btn_nenhum_modelo.clicked.connect(lambda: self._marcar_modelos(False))
        linha_modelos.addWidget(self.btn_todos_modelos)
        linha_modelos.addWidget(self.btn_nenhum_modelo)
        linha_modelos.addStretch()
        vb_modelos.addLayout(linha_modelos)
        from triton.core.edition import usa_dados_do_brasil
        self.caixa_modelos.setVisible(usa_dados_do_brasil())
        lay.addWidget(self.caixa_modelos)

        # 2. Distribuições
        lay.addWidget(_titulo(tr("2. Distribuições")))
        self.cartoes = {k: _CartaoParametro(k) for k in M.CATALOGO}
        self.grade_cartoes = QGridLayout()
        lay.addLayout(self.grade_cartoes)
        self.lbl_nenhuma = QLabel(tr("Nenhuma variável marcada: o resultado seria o próprio estudo."))
        lay.addWidget(self.lbl_nenhuma)

        # 3. Execução
        lay.addWidget(_titulo(tr("3. Execução")))
        controles = QGridLayout()
        self.spin_cv = QDoubleSpinBox()
        self.spin_cv.setRange(0.0, 200.0)
        self.spin_cv.setToolTip(tr("Ruído de um dia para o outro em torno do nível sorteado; numa série longa ele "
                                   "quase não move o resultado. 0 = sem variação diária."))
        self.spin_n = QSpinBox()
        self.spin_n.setRange(1, 20000)
        self.spin_n.setSingleStep(100)
        self.spin_n.setValue(1000)
        self.spin_semente = QSpinBox()
        self.spin_semente.setRange(0, 2 ** 31 - 1)
        self.spin_semente.setValue(42)
        for i, (rotulo, w) in enumerate(((tr("Variação diária (CV, %):"), self.spin_cv),
                                         (tr("Realizações:"), self.spin_n), (tr("Semente:"), self.spin_semente))):
            w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
            controles.addWidget(QLabel(rotulo), 0, 2 * i)
            controles.addWidget(w, 0, 2 * i + 1)
            controles.setColumnStretch(2 * i + 1, 1)
        self.btn_padroes = QPushButton(tr("Valores de triagem"))
        self.btn_padroes.clicked.connect(self.restaurar_padroes)
        controles.addWidget(self.btn_padroes, 0, 6)
        lay.addLayout(controles)
        botoes = QHBoxLayout()
        self.btn_simular = QPushButton(tr("▶ Simular"))
        self.btn_simular.clicked.connect(self.simular)
        self.btn_cancelar = QPushButton(tr("Cancelar"))
        self.btn_cancelar.setEnabled(False)
        self.btn_cancelar.clicked.connect(self.cancelar)
        self.btn_exportar = QPushButton(tr("Exportar (CSV + JSON)"))
        self.btn_exportar.setEnabled(False)
        self.btn_exportar.clicked.connect(self.exportar)
        self.barra = QProgressBar()
        self.barra.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        for w in (self.btn_simular, self.btn_cancelar, self.btn_exportar):
            botoes.addWidget(w)
        botoes.addWidget(self.barra, 1)
        lay.addLayout(botoes)
        self.lbl_estado = QLabel()
        self.lbl_estado.setWordWrap(True)
        lay.addWidget(self.lbl_estado)

        # 4. Resultados
        lay.addWidget(_titulo(tr("4. Resultados")))
        self.lbl_metodo = QLabel(tr("Rode a modulação para ver os resultados."))
        self.lbl_metodo.setWordWrap(True)
        self.lbl_metodo.setStyleSheet("color: #475569; font-size: 11px;")
        lay.addWidget(self.lbl_metodo)
        self.lbl_destaque = QLabel()
        self.lbl_destaque.setWordWrap(True)
        self.lbl_destaque.setStyleSheet("padding: 8px; background: #ecfdf5; border-radius: 6px;")
        self.lbl_destaque.hide()
        lay.addWidget(self.lbl_destaque)

        lay.addWidget(_legenda(tr("Tabela 1 — Variáveis sorteadas: distribuição declarada e estatísticas da amostra.")))
        self.tabela_entradas = _tabela([tr("Variável"), tr("No estudo"), tr("Distribuição"), tr("Média"),
                                        tr("Desvio-padrão"), "P5", "P95"], 80)
        lay.addWidget(self.tabela_entradas)
        self.leg_tab2 = _legenda(tr("Tabela 2 — Resultados no volume escolhido pelo estudo."))
        lay.addWidget(self.leg_tab2)
        self.tabela_ref = _tabela([tr("Grandeza"), tr("Estudo determinístico"), tr("Média"), tr("Desvio-padrão"),
                                   tr("CV (%)"), "P5", "P50", "P95"], 80)
        lay.addWidget(self.tabela_ref)
        self.lbl_probabilidades = QLabel()
        self.lbl_probabilidades.setWordWrap(True)
        lay.addWidget(self.lbl_probabilidades)

        self.graf_potencial = _GraficoLeque("modulacao-economia", "potencial_pct", tr("Economia de água potável (%)"), 1)
        self.graf_vpl = _GraficoLeque("modulacao-vpl", "vpl_brl", tr("VPL (R$)"), 0)
        self.graf_histograma = _GraficoHistograma("modulacao-histograma-vpl")
        self.graf_frequencia = _GraficoFrequencia("modulacao-frequencia")
        self.graf_sensibilidade = _GraficoSensibilidade("modulacao-sensibilidade")
        self.graf_convergencia = _GraficoConvergencia("modulacao-convergencia")
        self.figuras = (self.graf_potencial, self.graf_vpl, self.graf_histograma, self.graf_frequencia,
                        self.graf_sensibilidade, self.graf_convergencia)
        legendas = (
            tr("Figura 1 — Economia de água potável por volume: faixa entre os percentis 5 e 95, mediana e estudo "
               "determinístico; os valores marcados são os do volume escolhido pelo estudo (linha pontilhada)."),
            tr("Figura 2 — Valor presente líquido por volume: faixa entre os percentis 5 e 95, mediana e estudo "
               "determinístico; valores no volume escolhido."),
            tr("Figura 3 — Distribuição do valor presente líquido no volume escolhido pelo estudo."),
            tr("Figura 4 — Frequência (%) com que cada volume é o ideal técnico, o ótimo econômico (menor payback "
               "descontado) e o vencedor do TOPSIS."),
            tr("Figura 5 — Sensibilidade no volume escolhido: correlação de postos de Spearman (ρ) de cada variável "
               "sorteada com a economia e com o VPL, da maior para a menor influência no VPL."),
            tr("Figura 6 — Convergência: média acumulada do VPL no volume escolhido e intervalo de 95% (erro-padrão "
               "de Monte Carlo). A faixa que estreita indica que o número de realizações basta."),
        )
        self.blocos_figuras = []
        self.legendas_figuras: List[QLabel] = []
        for g, texto in zip(self.figuras, legendas):
            g.plot_empty(tr("Rode a modulação para gerar o gráfico"))
            bloco = QWidget()
            bloco.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
            vb = QVBoxLayout(bloco)
            vb.setContentsMargins(0, 0, 0, 0)
            rotulo = _legenda(texto)
            self.legendas_figuras.append(rotulo)
            vb.addWidget(rotulo)
            vb.addWidget(g)
            self.blocos_figuras.append(bloco)
        self.grade_figuras = QGridLayout()
        lay.addLayout(self.grade_figuras)

        self.lbl_um_volume = QLabel(tr(
            "O estudo tem um volume só (volume fixo na Etapa 4): as figuras e a tabela por volume ficam de fora, "
            "porque não há volumes a comparar. Para vê-las, use a varredura de volumes na Etapa 4."))
        self.lbl_um_volume.setWordWrap(True)
        self.lbl_um_volume.setStyleSheet("padding: 6px; border: 1px dashed #94a3b8; border-radius: 6px;")
        self.lbl_um_volume.hide()
        lay.addWidget(self.lbl_um_volume)
        self.leg_tab3 = _legenda(tr("Tabela 3 — Percentis da economia e do VPL e probabilidade de VPL positivo em "
                                    "cada volume; em negrito, o volume escolhido pelo estudo."))
        lay.addWidget(self.leg_tab3)
        self.tabela = _tabela([tr("Volume (m³)"), tr("Economia P5 (%)"), tr("Economia P50 (%)"),
                               tr("Economia P95 (%)"), tr("VPL P5 (R$)"), tr("VPL P50 (R$)"), tr("VPL P95 (R$)"),
                               tr("P(VPL > 0) (%)")], 120)
        lay.addWidget(self.tabela)
        self.leg_variancia = _legenda(tr(
            "Tabela 4 — Parte da variância do resultado no volume escolhido explicada por cada fonte de incerteza "
            "(η², razão de correlação; as variáveis contínuas agrupadas em decis). Com fontes independentes e efeitos "
            "aditivos, a soma fica perto de 1."))
        lay.addWidget(self.leg_variancia)
        self.tabela_variancia = _tabela([tr("Fonte de incerteza"), tr("η² da economia"), tr("η² do VPL"),
                                         tr("η² do saldo de CO₂")], 80)
        lay.addWidget(self.tabela_variancia)
        self.leg_tab4 = _legenda(tr("Tabela 5 — Resultados no volume escolhido, por modelo climático sorteado."))
        self.tabela_modelos = _tabela([tr("Modelo"), tr("Realizações"), tr("Economia média (%)"),
                                       tr("VPL médio (R$)"), tr("P(VPL > 0) (%)"), tr("IC 95% (%)")], 80)
        self.leg_tab4.hide()
        self.tabela_modelos.hide()
        lay.addWidget(self.leg_tab4)
        lay.addWidget(self.tabela_modelos)
        lay.addStretch()
        self.restaurar_padroes()
        self._reorganizar(self._largura, forcar=True)

    def _colunas(self, largura: int):
        return (3 if largura >= COLUNAS_3 else (2 if largura >= COLUNAS_2 else 1),
                2 if largura >= FIGURAS_2 else 1, 4 if largura >= GRUPOS_4 else (2 if largura >= 560 else 1))

    def _reorganizar(self, largura: int, forcar: bool = False):
        """Colunas conforme a largura (cartões 3/2/1, figuras 2/1, grupos 4/2): nunca rolagem lateral."""
        self._largura = largura
        c_cartoes, c_figuras, c_grupos = self._colunas(largura)
        if not forcar and getattr(self, "_atual", None) == (c_cartoes, c_figuras, c_grupos):
            return
        self._atual = (c_cartoes, c_figuras, c_grupos)
        c_modelos = 5 if largura >= MODELOS_5 else (3 if largura >= MODELOS_3 else 2)
        for i, chk in enumerate(self.checks_modelos.values()):
            self.grade_modelos.removeWidget(chk)
            self.grade_modelos.addWidget(chk, i // c_modelos, i % c_modelos)
        marcados = [self.cartoes[k] for k in M.CATALOGO if self.checks[k].isChecked()]
        # Com um volume só, as figuras por volume (leques e frequência) não têm o que mostrar.
        figuras = [b for i, b in enumerate(self.blocos_figuras) if not (self._um_volume and i in (0, 1, 3))]
        for grade, itens, todos, n in ((self.grade_cartoes, marcados, list(self.cartoes.values()), c_cartoes),
                                       (self.grade_figuras, figuras, self.blocos_figuras, c_figuras),
                                       (self.grade_grupos, self.caixas_grupo, self.caixas_grupo, c_grupos)):
            for w in todos:
                grade.removeWidget(w)
                if w not in itens:
                    w.hide()
            for c in range(4):
                grade.setColumnStretch(c, 1 if c < n else 0)
            for i, w in enumerate(itens):
                grade.addWidget(w, i // n, i % n)
                w.show()
        self.lbl_nenhuma.setVisible(not marcados)

    def _ao_marcar(self, *_):
        self._reorganizar(self._largura, forcar=True)

    def _ao_marcar_modelo(self, *_):
        self._descrever_modelos()

    def _marcar_modelos(self, marcar: bool):
        for chk in self.checks_modelos.values():
            chk.blockSignals(True)
            chk.setChecked(marcar and chk.isEnabled())
            chk.blockSignals(False)
        self._descrever_modelos()

    def modelos_marcados(self) -> List[str]:
        return [m for m, chk in self.checks_modelos.items() if chk.isChecked() and chk.isEnabled()]

    def _descrever_modelos(self):
        """Diz de onde vêm as séries, ou por que o sorteio de modelos não se aplica a este projeto."""
        cfg = self._cfg()
        pode = M.pode_sortear_modelos(cfg)
        for chk in self.checks_modelos.values():
            chk.setEnabled(pode)
        self.btn_todos_modelos.setEnabled(pode)
        self.btn_nenhum_modelo.setEnabled(pode)
        if not pode:
            from triton.core.edition import usa_dados_de_portugal
            if usa_dados_de_portugal():
                self.lbl_modelos.setText(tr(
                    "A chuva deste projeto vem da base E-OBS, com uma só série por concelho. O sorteio entre "
                    "modelos pede a base CLIMBra, que só a Edição Brasil traz."))
                return
            self.lbl_modelos.setText(tr(
                "A chuva deste projeto vem de um arquivo próprio. O sorteio entre modelos pede a base CLIMBra "
                "(Etapa 1), que tem as 19 séries para a mesma cidade."))
            return
        n = len(self.modelos_marcados())
        texto = tr("Cada realização sorteia, com igual probabilidade, a série de um dos modelos marcados: {0}, "
                   "cenário {1}, de {2} a {3}. O fator da chuva, se marcado, multiplica a série sorteada. "
                   "Nenhum marcado: todas as realizações usam a série do projeto ({4}).").format(
            cfg.climate_city_name, cfg.climate_scenario, cfg.climate_start_date, cfg.climate_end_date,
            cfg.climate_model)
        if n:
            texto += " " + tr("Marcados: {0}.").format(n)
        self.lbl_modelos.setText(texto)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reorganizar(self.rolagem.viewport().width())

    # ---------------------------------------------------------------- estudo
    def _estudo(self):
        """(cfg, chuva, pesos, ambiental) do estudo da tela, ou mensagem do que falta."""
        mw = self.main_window
        if mw is None:
            return None, tr("Abra a ferramenta pela janela principal.")
        precip = getattr(getattr(mw, "tab_project", None), "precip_data", None)
        if precip is None or len(precip) == 0:
            return None, tr("Carregue a série de chuva na Etapa 1 e rode o estudo antes de modulá-lo.")
        cfg = mw.config_do_estudo() if hasattr(mw, "config_do_estudo") else copy.deepcopy(mw.config)
        from triton.cli import _analysis_from_ui_state
        estado = mw._collect_project_ui_state() if hasattr(mw, "_collect_project_ui_state") else {}
        analise = _analysis_from_ui_state(estado)
        return (copy.deepcopy(cfg), np.asarray(precip, dtype=float), analise.get("topsis_weights"),
                analise.get("environmental"), analise.get("topsis_criterion_shares")), None

    def _cfg(self):
        estudo, _ = self._estudo()
        cfg = estudo[0] if estudo else getattr(self.main_window, "config", None)
        if cfg is None:
            from triton.core.parser import TritonConfig
            cfg = TritonConfig()
        return cfg

    def restaurar_padroes(self):
        cfg = self._cfg()
        self.aplicar_parametros(M.padroes_do_projeto(cfg))
        self._triagens = {k: M.distribuicao_de_triagem(cfg, k) for k in M.CATALOGO}
        self.atualizar_referencia()

    @staticmethod
    def _equivalentes(a: M.Distribuicao, b: M.Distribuicao) -> bool:
        """A mesma distribuição, a menos do arredondamento das caixas da tela."""
        if a.tipo != b.tipo:
            return False
        campos = {"normal": ("media", "desvio"), "lognormal": ("media", "desvio"),
                  "triangular": ("minimo", "moda", "maximo"), "uniforme": ("minimo", "maximo")}[a.tipo]
        for c in campos + ("limite_inferior", "limite_superior"):
            x, y = getattr(a, c), getattr(b, c)
            if (x is None) != (y is None):
                return False
            if x is not None and not np.isclose(float(x), float(y), rtol=0.01, atol=0.01):
                return False
        return True

    def recentrar(self):
        """Leva ao estudo atual os cartões que o usuário não editou; os editados ficam como estão."""
        cfg = self._cfg()
        for k, cartao in self.cartoes.items():
            nova = M.distribuicao_de_triagem(cfg, k)
            antiga = self._triagens.get(k)
            atual = cartao.distribuicao(variar=True)
            if antiga is None or self._equivalentes(atual, antiga):
                cartao.definir(nova, M.valor_do_projeto(cfg, k))
            else:
                cartao.definir(atual, M.valor_do_projeto(cfg, k))
            self._triagens[k] = nova

    def aplicar_parametros(self, parametros: M.ParametrosIncertos):
        cfg = self._cfg()
        for k, cartao in self.cartoes.items():
            dist = parametros.variaveis.get(k) or M.distribuicao_de_triagem(cfg, k)
            cartao.definir(dist, M.valor_do_projeto(cfg, k))
            self.checks[k].blockSignals(True)
            self.checks[k].setChecked(bool(dist.variar))
            self.checks[k].blockSignals(False)
        self.spin_cv.setValue(parametros.cv_diario_pct)
        for m, chk in self.checks_modelos.items():
            chk.blockSignals(True)
            chk.setChecked(m in parametros.modelos_climaticos)
            chk.blockSignals(False)
        self._descrever_modelos()
        self._reorganizar(self._largura, forcar=True)

    def parametros(self) -> M.ParametrosIncertos:
        return M.ParametrosIncertos(
            variaveis={k: c.distribuicao(variar=self.checks[k].isChecked()) for k, c in self.cartoes.items()},
            cv_diario_pct=self.spin_cv.value(), modelos_climaticos=self.modelos_marcados())

    def atualizar_referencia(self):
        estudo, falta = self._estudo()
        if falta:
            self.lbl_referencia.setText(f"⚠️ {falta}")
            return
        cfg = estudo[0]
        self.lbl_referencia.setText(tr(
            "Estudo de referência: {0} L/hab.dia, {1} pessoas, {2}% de usos não potáveis internos, "
            "{3} dias de chuva.").format(_br(cfg.demand_value, 1), int(cfg.residents_count),
                                          _br(100.0 * cfg.non_potable_indoor_share, 1), len(estudo[1])))

    def atualizar_moeda(self):
        """A moeda do projeto (Etapa 4) em rótulos, cartões e cabeçalhos: euro na International."""
        global MOEDA
        mw = self.main_window
        ts = getattr(mw, "tab_tanks_simulation", None)
        if ts is not None and hasattr(ts, "get_currency_symbol"):
            simbolo = ts.get_currency_symbol()
        else:
            from triton.core.edition import get_edition_currency_symbol
            simbolo = get_edition_currency_symbol()
        if simbolo == MOEDA and getattr(self, "_moeda_aplicada", None) == simbolo:
            return
        MOEDA = simbolo
        self._moeda_aplicada = simbolo
        for k, chk in self.checks.items():
            chk.setText(_rotulo_variavel(k))
            chk.setToolTip(_descricao(M.CATALOGO[k]))
        for k, cartao in self.cartoes.items():
            cartao.setTitle(_rotulo_variavel(k))
            cartao.setToolTip(_descricao(M.CATALOGO[k]))
        for tabela in (self.tabela, self.tabela_modelos):
            for j in range(tabela.columnCount()):
                item = tabela.horizontalHeaderItem(j)
                if item is not None:
                    item.setText(re.sub(r"\((?:R\$|\$|\u20ac|\u00a3|\u00a5|\u00a4|\u20b9|A\$|C\$|CHF|R)\)", f"({simbolo})", item.text()))

    def showEvent(self, event):
        super().showEvent(event)
        self.atualizar_moeda()
        self.recentrar()
        self.atualizar_referencia()
        self._descrever_modelos()
        self._reorganizar(self.rolagem.viewport().width())

    # ---------------------------------------------------------------- estado do projeto
    def get_project_state(self) -> Dict[str, Any]:
        return {"parametros": self.parametros().para_dict(), "amostras": self.spin_n.value(),
                "semente": self.spin_semente.value()}

    def apply_project_state(self, estado: Optional[Dict[str, Any]]):
        if not estado:
            return
        if estado.get("parametros"):
            self.aplicar_parametros(M.ParametrosIncertos.de_dict(estado["parametros"]))
            # As distribuições gravadas valem; só as que ainda são a triagem acompanham o estudo.
            cfg = self._cfg()
            self._triagens = {k: M.distribuicao_de_triagem(cfg, k) for k in M.CATALOGO}
        self.spin_n.setValue(int(estado.get("amostras", self.spin_n.value())))
        self.spin_semente.setValue(int(estado.get("semente", self.spin_semente.value())))

    # ---------------------------------------------------------------- execução
    def simular(self, *_args, bloquear: bool = False):
        estudo, falta = self._estudo()
        if falta:
            QMessageBox.warning(self, tr("Modulação Probabilística"), falta)
            return
        try:
            parametros = self.parametros()
            parametros.validar()
        except ValueError as e:
            QMessageBox.warning(self, tr("Modulação Probabilística"), str(e))
            return
        if not parametros.ativas() and parametros.cv_diario_pct <= 0 and not parametros.modelos_climaticos:
            QMessageBox.information(self, tr("Modulação Probabilística"),
                                    tr("Nenhuma variável marcada: o resultado seria o próprio estudo."))
            return
        cfg, precip, pesos, ambiental, partes = estudo
        self._trabalhador = _Trabalhador(cfg, precip, parametros, self.spin_n.value(), self.spin_semente.value(),
                                         pesos, ambiental, partes)
        self._trabalhador.progresso.connect(self._ao_progredir)
        self._trabalhador.concluido.connect(self._ao_concluir)
        self._trabalhador.falhou.connect(self._ao_falhar)
        self.barra.setRange(0, self.spin_n.value())
        self.barra.setValue(0)
        self.btn_simular.setEnabled(False)
        self.btn_cancelar.setEnabled(True)
        self._inicio = time.monotonic()
        self.lbl_estado.setText(tr("Rodando o caso-base…"))
        if bloquear:  # testes: no mesmo fio
            self._trabalhador.rodar()
            return
        self._thread = QThread(self)
        self._trabalhador.moveToThread(self._thread)
        self._thread.started.connect(self._trabalhador.rodar)
        self._trabalhador.concluido.connect(self._thread.quit)
        self._trabalhador.falhou.connect(self._thread.quit)
        self._thread.start()

    def cancelar(self):
        if self._trabalhador is not None:
            self._trabalhador.cancelar()
            self.lbl_estado.setText(tr("Cancelando…"))

    def _ao_progredir(self, feitas: int, total: int):
        self.barra.setValue(feitas)
        gasto = time.monotonic() - self._inicio
        resta = gasto / max(1, feitas) * (total - feitas)
        self.lbl_estado.setText(tr("{0}/{1} — faltam ~{2} s").format(feitas, total, int(resta)))

    def _ao_falhar(self, mensagem: str):
        self.btn_simular.setEnabled(True)
        self.btn_cancelar.setEnabled(False)
        self.lbl_estado.setText("")
        QMessageBox.critical(self, tr("Modulação Probabilística"), mensagem)

    def _ao_concluir(self, dados: Dict[str, Any]):
        self.resultado = dados
        self.btn_simular.setEnabled(True)
        self.btn_cancelar.setEnabled(False)
        self.btn_exportar.setEnabled(bool(dados.get("realizacoes_feitas")))
        self.lbl_estado.setText(tr("{0} realizações em {1} s").format(
            dados["realizacoes_feitas"], int(time.monotonic() - self._inicio))
            + (f" — {tr('cancelado')}" if dados.get("cancelado") else ""))
        if dados.get("realizacoes_feitas"):
            self.mostrar(dados)
            self._renumerar()

    # ---------------------------------------------------------------- apresentação
    @staticmethod
    def _descrever_distribuicao(d: Dict[str, Any], casas: int) -> str:
        tipo = tr(dict(TIPOS_NA_TELA)[d["tipo"]])
        if d["tipo"] in ("normal", "lognormal"):
            return f"{tipo} ({_br(d['media'], casas)}; {_br(d['desvio'], casas)})"
        if d["tipo"] == "triangular":
            return f"{tipo} ({_br(d['minimo'], casas)}; {_br(d['moda'], casas)}; {_br(d['maximo'], casas)})"
        return f"{tipo} ({_br(d['minimo'], casas)}; {_br(d['maximo'], casas)})"

    def mostrar(self, dados: Dict[str, Any]):
        self.atualizar_moeda()
        cfg = self._cfg()
        ativas = dados.get("variaveis_ativas", [])
        self.lbl_metodo.setText(tr(
            "{0} realizações de Monte Carlo, semente {1}. As {2} variáveis marcadas são sorteadas de forma "
            "independente, uma vez por realização, e aplicadas a todos os volumes (comparação pareada); as demais "
            "ficam com o valor do estudo. Variação diária do consumo: CV de {3}%. Percentis empíricos; intervalos de "
            "95% de Wilson para as probabilidades e do erro-padrão de Monte Carlo para a média.").format(
            dados["realizacoes_feitas"], dados["semente"], len(ativas),
            _br(dados["parametros"].get("cv_diario_pct", 0.0), 0)))

        # Tabela 1 — entradas
        linhas = []
        for k in ativas:
            casas = M.CATALOGO[k].casas if M.CATALOGO[k].unidade not in ("×", "—") else 2
            e = dados["entradas"][k]
            d = dados["parametros"]["variaveis"][k]
            linhas.append([_rotulo_variavel(k), _br(M.valor_do_projeto(cfg, k), casas),
                           self._descrever_distribuicao(d, casas), _br(e["media"], casas), _br(e["desvio"], casas),
                           _br(e["p5"], casas), _br(e["p95"], casas)])
        _preencher(self.tabela_entradas, linhas)

        ref = dados.get("referencia") or {}
        if ref:
            self.leg_tab2.setText(tr("Tabela 2 — Resultados no volume escolhido pelo estudo ({0} m³).").format(
                _m3(ref["volume_l"])))
            itens = (("potencial_pct", tr("Economia de água potável (%)"), 1),
                     ("vpl_brl", _m(tr("VPL (R$)")), 0),
                     ("payback_anos", tr("Payback descontado (anos)"), 1),
                     ("co2_kg", tr("Saldo de CO₂ no ciclo de vida (kg)"), 0))
            _preencher(self.tabela_ref, [[rotulo, _br(ref["base"].get(c), casas), _br(ref[c]["media"], casas),
                                          _br(ref[c]["desvio"], casas), _br(ref[c]["cv_pct"], 1),
                                          _br(ref[c]["p5"], casas), _br(ref[c]["p50"], casas),
                                          _br(ref[c]["p95"], casas)] for c, rotulo, casas in itens])
            pv, pc = ref.get("prob_vpl_positivo"), ref.get("prob_co2_positivo")
            textos = []
            if pv and pv["pct"] is not None:
                textos.append(tr("P(VPL > 0) = {0}% (IC 95% de Wilson: {1}% a {2}%)").format(
                    _br(pv["pct"], 1), _br(pv["ic95_inf"], 1), _br(pv["ic95_sup"], 1)))
            if pc and pc["pct"] is not None:
                textos.append(tr("P(saldo de CO₂ > 0) = {0}% (IC 95%: {1}% a {2}%)").format(
                    _br(pc["pct"], 1), _br(pc["ic95_inf"], 1), _br(pc["ic95_sup"], 1)))
            textos.append(tr("o payback descontado é calculado nas {0} realizações em que o investimento se paga")
                          .format(ref.get("realizacoes_que_se_pagam", 0)))
            self.lbl_probabilidades.setText("; ".join(textos) + ".")

            p, v = ref["potencial_pct"], ref["vpl_brl"]
            freq = dados["frequencia_pct"]["vencedor_topsis"]
            mantido = freq.get(f"{ref['volume_l']:.0f}", 0.0)
            sens = dados.get("sensibilidade_spearman") or {}
            dominante = max(sens, key=lambda n: abs(sens[n]["vpl_brl"] or 0.0)) if sens else None
            destaque = _m(tr(
                "<b>No volume escolhido ({0} m³)</b>: economia de {1}% no estudo e de {2}% a {3}% em 90% das "
                "realizações; VPL mediano de R$ {4} (P5 R$ {5}, P95 R$ {6}); o investimento se paga em {7}% das "
                "realizações; o volume continua o vencedor do TOPSIS em {8}% delas.")).format(
                _m3(ref["volume_l"]), _br(ref["base"]["potencial_pct"], 1), _br(p["p5"], 1), _br(p["p95"], 1),
                _br(v["p50"]), _br(v["p5"]), _br(v["p95"]), _br((pv or {}).get("pct"), 0), _br(mantido, 0))
            if dominante:
                destaque += " " + tr("A variável que mais pesa no VPL é {0} (ρ = {1}).").format(
                    tr(M.CATALOGO[dominante].rotulo).lower(), _br(sens[dominante]["vpl_brl"], 2))
            eta = (dados.get("sensibilidade_modelo_eta2") or {}).get("vpl_brl")
            if eta is not None:
                destaque += " " + tr("O modelo climático explica {0}% da variância do VPL (η²).").format(_br(100 * eta, 0))
            self.lbl_destaque.setText(destaque)
            self.lbl_destaque.show()

        self._um_volume = len(dados.get("por_volume") or []) <= 1
        self.lbl_um_volume.setVisible(self._um_volume)
        self.leg_tab3.setVisible(not self._um_volume)
        self.tabela.setVisible(not self._um_volume)
        self._reorganizar(self._largura, forcar=True)
        for i, g in enumerate(self.figuras):
            if not (self._um_volume and i in (0, 1, 3)):
                g.desenhar(dados)

        linhas = []
        negrito = set()
        for i, v in enumerate(dados["por_volume"]):
            if v["volume_l"] == dados.get("volume_de_referencia_l"):
                negrito.add(i)
            linhas.append([_m3(v["volume_l"]), _br(v["potencial_pct"]["p5"], 1), _br(v["potencial_pct"]["p50"], 1),
                           _br(v["potencial_pct"]["p95"], 1), _br(v["vpl_brl"]["p5"]), _br(v["vpl_brl"]["p50"]),
                           _br(v["vpl_brl"]["p95"]), _br(v["prob_vpl_positivo_pct"], 0)])
        _preencher(self.tabela, linhas, negrito)

        legenda_ve = tr(
            "Tabela 4 — Parte da variância do resultado no volume escolhido explicada por cada fonte de incerteza "
            "(η², razão de correlação; as variáveis contínuas agrupadas em decis). Com fontes independentes e efeitos "
            "aditivos, a soma fica perto de 1.")
        n_feitas = int(dados.get("realizacoes_feitas") or 0)
        if 0 < n_feitas < REALIZACOES_PARA_LER_O_ETA2:
            # O η² por classes superestima cada parcela em cerca de (classes − 1)/N.
            legenda_ve += " " + tr(
                "Com {0} realizações, cada η² está superestimado em cerca de {1} (viés de (classes − 1)/N): "
                "valores dessa ordem não distinguem uma fonte sem efeito, e a soma pode passar de 1. "
                "Aumente as realizações para ler as parcelas pequenas.").format(n_feitas, _br(9.0 / n_feitas, 2))
        self.leg_variancia.setText(legenda_ve)
        ve = dados.get("variancia_explicada_eta2") or {}
        ordem = sorted(ve, key=lambda k: -(ve[k]["vpl_brl"] or 0.0))
        _preencher(self.tabela_variancia, [
            [tr("Modelo climático") if k == "modelo_climatico" else _rotulo_variavel(k),
             _br(ve[k]["potencial_pct"], 2), _br(ve[k]["vpl_brl"], 2), _br(ve[k]["co2_kg"], 2)] for k in ordem]
            + ([[tr("Soma"), *(_br(sum(ve[k][c] or 0.0 for k in ordem), 2)
                               for c in ("potencial_pct", "vpl_brl", "co2_kg"))]] if ordem else []))

        por_modelo = dados.get("por_modelo") or []
        self.leg_tab4.setVisible(bool(por_modelo))
        self.tabela_modelos.setVisible(bool(por_modelo))
        if por_modelo:
            eta = dados.get("sensibilidade_modelo_eta2") or {}
            self.leg_tab4.setText(tr(
                "Tabela 5 — Resultados no volume escolhido, por modelo climático sorteado. O modelo explica "
                "{0}% da variância da economia e {1}% da do VPL (η², razão de correlação).").format(
                _br(100 * eta["potencial_pct"], 0) if eta.get("potencial_pct") is not None else "—",
                _br(100 * eta["vpl_brl"], 0) if eta.get("vpl_brl") is not None else "—"))
            linhas = []
            for m in por_modelo:
                pv = m.get("prob_vpl_positivo") or {}
                linhas.append([m["modelo"], str(m["realizacoes"]), _br(m["potencial_pct"]["media"], 1),
                               _br(m["vpl_brl"]["media"]), _br(pv.get("pct"), 0),
                               f"{_br(pv.get('ic95_inf'), 0)}–{_br(pv.get('ic95_sup'), 0)}"
                               if pv.get("pct") is not None else "—"])
            _preencher(self.tabela_modelos, linhas)

    def _renumerar(self):
        """Figuras e tabelas visíveis numeradas em sequência, sem saltos quando alguma fica de fora."""
        figuras = [r for i, r in enumerate(self.legendas_figuras) if not (self._um_volume and i in (0, 1, 3))]
        tabelas = [self.leg_tab2, self.leg_tab3, self.leg_variancia, self.leg_tab4]
        tabelas = [r for r in tabelas if r is self.leg_tab2 or not r.isHidden()]
        for primeiro, rotulos in ((1, figuras), (2, tabelas)):
            for n, rotulo in enumerate(rotulos, start=primeiro):
                rotulo.setText(re.sub(r"\d+", str(n), rotulo.text(), count=1))

    def exportar(self, caminho: Optional[str] = None):
        if not self.resultado:
            return
        if not caminho:
            caminho, _ = QFileDialog.getSaveFileName(self, tr("Exportar"), "triton-modulacao-estocastica.json",
                                                     "JSON (*.json)")
        if not caminho:
            return
        base = caminho[:-5] if caminho.lower().endswith(".json") else caminho
        with open(base + ".json", "w", encoding="utf-8") as f:
            json.dump(self.resultado, f, ensure_ascii=False, indent=2)
        amostras = self.resultado.get("amostras") or []
        with open(base + ".csv", "w", newline="", encoding="utf-8-sig") as f:
            if amostras:
                w = csv.DictWriter(f, fieldnames=list(amostras[0].keys()), delimiter=";")
                w.writeheader()
                w.writerows(amostras)
        return base + ".json", base + ".csv"
