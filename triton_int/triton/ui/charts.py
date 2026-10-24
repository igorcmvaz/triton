"""
Componentes de Gráficos Dinâmicos em PySide6 no estilo Clássico do Netuno 4.
Gráficos 2x2 com Identidade Visual UFSC Sustentável:
1. Potencial de Economia (%) vs Volume do Reservatório (L)
2. Delta Marginal (%/m³) vs Volume do Reservatório (L)
3. Volume Reservado Médio (m³) vs Volume do Reservatório (L)
4. Percentual de Dias de Atendimento (%) vs Volume do Reservatório (L)
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QComboBox, QScrollArea, QFrame, QSizePolicy, QDialog, QFormLayout, QDialogButtonBox, QCheckBox
from triton.core.numero import milhar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
import numpy as np
from math import ceil, floor
import os

from triton.ui.translation import tr, get_current_lang
from triton.ui.textos_da_edicao import nome_sugerido
from triton.core.parser import format_ptbr

# Proporção padrão dos gráficos (16:9)
_CHART_ASPECT_W = 16
_CHART_ASPECT_H = 9
_CHART_MIN_HEIGHT_PX = 260   # altura mínima em pixels
_CHART_DPI = 96
_EXPORT_RATIOS = {"1:1": (1, 1), "3:2": (3, 2), "4:3": (4, 3), "16:9": (16, 9)}


def configure_matplotlib_locale():
    """Seleciona uma fonte CJK do sistema quando a interface está em chinês.

    Microsoft YaHei acompanha as versões suportadas do Windows e é descoberta
    pelo Matplotlib pelo nome da família; Noto e PingFang cobrem instalações
    alternativas. O restante dos idiomas preserva a configuração padrão.
    """
    if get_current_lang() == "zh":
        rcParams["font.sans-serif"] = [
            "Microsoft YaHei", "Microsoft YaHei UI", "Noto Sans CJK SC",
            "PingFang SC", "WenQuanYi Micro Hei", "DejaVu Sans",
        ]
        rcParams["axes.unicode_minus"] = False


def _sweep_xmax(sweep_results, selected_vol=None) -> float:
    """Domínio X para gráficos de varredura, sempre iniciado em zero."""
    volumes = [float(r.lower_tank_vol) for r in (sweep_results or [])]
    if selected_vol is not None:
        volumes.append(float(selected_vol))
    return max(1.0, max(volumes, default=0.0))


def _upper_multiple(values, step: float) -> float:
    """Limite Y superior arredondado para o múltiplo solicitado."""
    highest = max(0.0, *(float(v) for v in values if v is not None))
    return max(step, ceil(highest / step) * step)


class TritonBaseChart(QWidget):
    """Classe base para gráficos Matplotlib no Triton — proporção responsiva."""
    def __init__(self, title="", parent=None, aspect_ratio=(16, 9), min_height=None):
        super().__init__(parent)
        configure_matplotlib_locale()
        self.chart_title = title
        self._aspect_w = float(aspect_ratio[0])
        self._aspect_h = float(aspect_ratio[1])
        self._canvas_min_height = min_height if min_height is not None else (_CHART_MIN_HEIGHT_PX if self._aspect_h >= 9 else int(_CHART_MIN_HEIGHT_PX * self._aspect_h / 9.0))
        self._canvas_max_height = None

        # figsize em polegadas a 96 dpi — será redimensionado via resizeEvent
        self.figure = Figure(figsize=(9.6, 9.6 * self._aspect_h / self._aspect_w), dpi=_CHART_DPI, facecolor='#ffffff')
        self.canvas = FigureCanvas(self.figure)
        # Canvas cresce horizontalmente mas tem altura proporcional ao aspecto
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(4, 2, 4, 2)
        h_layout.addStretch()

        ratio_str = "16:9" if (self._aspect_w == 16 and self._aspect_h == 9) else f"{int(self._aspect_w)}:{int(self._aspect_h)}"
        lbl_ratio = QLabel(ratio_str)
        lbl_ratio.setStyleSheet("font-size: 10px; color: #94a3b8; font-style: italic;")
        h_layout.addWidget(lbl_ratio)

        btn_export = QPushButton(tr("📸 Exportar"))
        if is_dark:
            btn_export.setStyleSheet("font-size: 10px; padding: 2px 8px; background-color: #27272a; border: 1px solid #3f3f46; color: #ffffff; border-radius: 4px;")
        else:
            btn_export.setStyleSheet("font-size: 10px; padding: 2px 8px; background-color: #ffffff; border: 1px solid #005a36; color: #005a36; border-radius: 4px;")
        btn_export.clicked.connect(self.export_figure)
        h_layout.addWidget(btn_export)
        layout.addLayout(h_layout)

        # Canvas direto no layout — sem QScrollArea interno
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Altura inicial: largura padrão de referência
        self._update_canvas_height(800)
        self.plot_empty(tr("Execute a varredura para gerar o grafico"))

    def _update_canvas_height(self, width_px: int):
        """Recalcula altura do canvas para manter a proporção configurada."""
        h = max(self._canvas_min_height, int(width_px * self._aspect_h / self._aspect_w))
        if self._canvas_max_height is not None:
            h = min(h, self._canvas_max_height)
        self.canvas.setFixedHeight(h)
        # Atualiza figsize para que matplotlib use resolução correta
        w_in = width_px / _CHART_DPI
        h_in = h / _CHART_DPI
        self.figure.set_size_inches(w_in, h_in)

    def set_canvas_height_range(self, minimum=None, maximum=None):
        """Define limites de altura sem perder a largura responsiva do gráfico."""
        if minimum is not None:
            self._canvas_min_height = minimum
        self._canvas_max_height = maximum
        self._update_canvas_height(max(1, self.width()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_canvas_height(self.width())

    def export_figure(self):
        from triton import get_kebab_filename
        # ``bbox_inches='tight'`` changes the page size according to labels
        # and legends.  That was distorting the requested export ratios.
        dialog = QDialog(self)
        dialog.setWindowTitle(tr("Exportar Figura do Grafico"))
        form = QFormLayout(dialog)
        ratio_combo = QComboBox()
        ratio_combo.addItems(_EXPORT_RATIOS.keys())
        ratio_combo.setCurrentText("16:9")
        form.addRow(tr("Proporcao da figura:"), ratio_combo)

        formats = QHBoxLayout()
        checks = {}
        for extension in ("png", "pdf", "svg"):
            checkbox = QCheckBox(extension.upper())
            checkbox.setChecked(True)
            checks[extension] = checkbox
            formats.addWidget(checkbox)
        formats.addStretch()
        form.addRow(tr("Formatos:"), formats)
        hint = QLabel(tr("PNG e raster; PDF e SVG preservam vetores. A proporcao escolhida e aplicada exatamente."))
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #475569; font-size: 11px;")
        form.addRow(hint)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)
        if dialog.exec() != QDialog.Accepted:
            return

        selected_formats = [extension for extension, checkbox in checks.items() if checkbox.isChecked()]
        if not selected_formats:
            QMessageBox.warning(self, tr("Exportar Figura do Grafico"), tr("Selecione ao menos um formato de exportacao."))
            return

        base_t = self.chart_title or "triton-grafico"
        first_extension = selected_formats[0]
        def_name = get_kebab_filename(f"{nome_sugerido('triton-grafico')}-{base_t}", first_extension)
        file_path, _ = QFileDialog.getSaveFileName(
            self, tr("Exportar Figura do Grafico"), def_name,
            f"{tr('Arquivos de figura')} (*.{first_extension})"
        )
        if not file_path:
            return
        try:
            base_path = os.path.splitext(file_path)[0]
            ratio_w, ratio_h = _EXPORT_RATIOS[ratio_combo.currentText()]
            export_width_px = 2400
            export_height_px = round(export_width_px * ratio_h / ratio_w)
            original_size = self.figure.get_size_inches()
            try:
                self.figure.set_size_inches(export_width_px / 300, export_height_px / 300, forward=True)
                paths = []
                for extension in selected_formats:
                    output_path = f"{base_path}.{extension}"
                    self.figure.savefig(
                        output_path, dpi=300, bbox_inches=None, pad_inches=0,
                        facecolor=self.figure.get_facecolor(), transparent=False,
                    )
                    paths.append(output_path)
            finally:
                self.figure.set_size_inches(*original_size, forward=True)
                self.safe_draw()
            QMessageBox.information(self, tr("Sucesso"), f"{tr('Figuras exportadas com sucesso em:')}\n" + "\n".join(paths))
        except Exception as e:
            QMessageBox.critical(self, tr("Erro ao Exportar"), f"{tr('Falha ao salvar a imagem:')}\n{str(e)}")
    def safe_draw(self):
        try:
            from PySide6.QtWidgets import QApplication
            app = QApplication.instance()
            if app and app.platformName() == "offscreen":
                return
            self.canvas.draw_idle()
        except Exception:
            pass

    def plot_empty(self, msg="Sem dados"):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#f8fafc')
        ax.text(0.5, 0.5, msg, color='#64748b', ha='center', va='center', fontsize=9, fontweight='500')
        ax.tick_params(colors='#475569', labelsize=7.5)
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                self.figure.tight_layout(pad=1.0)
            except Exception:
                pass
        self.safe_draw()


class SensitivityChart(TritonBaseChart):
    """Gráfico de Sensibilidade Multivariável (VPL vs Variação %)."""
    def __init__(self, parent=None):
        super().__init__("Análise de Sensibilidade Multivariável (VPL)", parent)

    def update_chart(self, sensitivity_data=None, currency_symbol="R$"):
        if not sensitivity_data:
            self.plot_empty(tr("Execute o cálculo financeiro para gerar a sensibilidade"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#cbd5e1'

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)

        # Paleta ampliada para 10 variáveis
        colors = [
            '#0284c7', '#dc2626', '#16a34a', '#d97706', '#8b5cf6',
            '#0f766e', '#be123c', '#65a30d', '#ea580c', '#1d4ed8'
        ]
        styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--']

        for idx, (label, points) in enumerate(sensitivity_data.items()):
            x_vals = [p[0] for p in points]
            y_vals = [p[1] for p in points]
            c = colors[idx % len(colors)]
            s = styles[idx % len(styles)]
            ax.plot(x_vals, y_vals, color=c, linestyle=s, linewidth=1.8, marker='o', markersize=3, label=label)

        ax.axvline(x=0, color='#64748b', linestyle=':', linewidth=1.0)
        ax.axhline(y=0, color='#64748b', linestyle='-', linewidth=0.8, alpha=0.5)

        ax.set_xlabel(tr("Variação dos Parâmetros (%)"), color=text_color, fontsize=8.5, fontweight='bold')
        ax.set_ylabel(f"{tr('VPL')} ({currency_symbol})", color=text_color, fontsize=8.5, fontweight='bold')
        ax.tick_params(colors=text_color, labelsize=8)
        ax.grid(True, linestyle=':', alpha=0.6, color=grid_color)

        # Legenda posicionada à direita da figura
        ax.legend(
            bbox_to_anchor=(1.02, 0.5),
            loc='center left',
            ncol=1,
            borderaxespad=0.0,
            fontsize=7,
            frameon=True,
            facecolor=bg_color,
            edgecolor=grid_color,
            labelcolor=text_color,
            title=tr("Parâmetros Variados"),
            title_fontsize=7.5
        )
        ax.margins(x=0.05, y=0.10)
        for spine in ax.spines.values():
            spine.set_color(grid_color)

        self.figure.subplots_adjust(left=0.14, bottom=0.16, right=0.62, top=0.92)
        self.safe_draw()


class PotentialVsVolumeChart(TritonBaseChart):
    """Gráfico 1: Potencial de Economia de Água Potável (%) vs Volume (L)."""
    def __init__(self, parent=None):
        super().__init__("1. Potencial de Economia de Água Potável (%)", parent)

    def update_chart(self, sweep_results=None, single_result=None, optimal_vol=None):
        if not sweep_results and not single_result:
            self.plot_empty(tr("Execute a simulação na Etapa 3"))
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#f8fafc')

        selected_vol = single_result.lower_tank_vol if single_result else None
        selected_pot = single_result.potential_potable_savings_pct if single_result else None

        if sweep_results and len(sweep_results) > 1:
            vols = [r.lower_tank_vol for r in sweep_results]
            pots = [r.potential_potable_savings_pct for r in sweep_results]
            ax.plot(vols, pots, color='#059669', linewidth=2.0, marker='o', markersize=3, label=tr("Curva de Potencial (%)"))
        else:
            pots = [selected_pot or 0.0]

        # Destaque do ponto único selecionado (sem poluir a legenda)
        if selected_vol is not None and selected_pot is not None:
            ax.plot(selected_vol, selected_pot, color='#dc2626', marker='*', markersize=12, linestyle='')
            ax.annotate(f"{format_ptbr(selected_pot, 1)}% ({format_ptbr(selected_vol, 0)} L)", 
                        (selected_vol, selected_pot), 
                        textcoords="offset points", xytext=(0, 8), ha='center',
                        fontsize=8, fontweight='bold', color='#dc2626')

        ax.set_xlabel(tr("Volume do Reservatório (L)"), color='#334155', fontsize=8, fontweight='bold')
        ax.set_ylabel(tr("Economia (%)"), color='#059669', fontsize=8, fontweight='bold')
        ax.set_xlim(0, _sweep_xmax(sweep_results, selected_vol))
        ax.set_ylim(0, _upper_multiple(pots + ([selected_pot] if selected_pot is not None else []), 5))
        ax.tick_params(colors='#334155', labelsize=7.5)
        ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')

        if ax.get_legend_handles_labels()[0]:
            ax.legend(loc='lower right', facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.9, fontsize=7.5)
        for spine in ax.spines.values():
            spine.set_color('#cbd5e1')

        self.figure.tight_layout(pad=1.0)
        self.safe_draw()


class DeltaVsVolumeChart(TritonBaseChart):
    """Gráfico 2: Delta Marginal / Variação do Potencial (%/m³) vs Volume (L)."""
    def __init__(self, parent=None):
        super().__init__("2. Delta Marginal (%/m³)", parent)

    def update_chart(self, sweep_results=None, single_result=None, delta_threshold=1.0):
        if not sweep_results and not single_result:
            self.plot_empty(tr("Execute a simulação na Etapa 3"))
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#f8fafc')

        selected_vol = single_result.lower_tank_vol if single_result else None
        selected_delta = None

        if sweep_results and len(sweep_results) > 1:
            vols = [r.lower_tank_vol for r in sweep_results]
            deltas = [r.delta_potential_per_m3 for r in sweep_results]
            ax.plot(vols, deltas, color='#dc2626', linewidth=2.0, marker='s', markersize=3, label=tr("Delta (%/m³)"))

            if selected_vol is not None:
                closest_r = min(sweep_results, key=lambda r: abs(r.lower_tank_vol - selected_vol))
                selected_delta = closest_r.delta_potential_per_m3
        else:
            deltas = [selected_delta or 0.0]

        ax.axhline(
            delta_threshold, color='#f59e0b', linestyle='--', linewidth=1.3,
            label=tr("Threshold técnico") + f" ({format_ptbr(delta_threshold, 2)} %/m³)",
        )

        if selected_vol is not None and selected_delta is not None:
            ax.plot(selected_vol, selected_delta, color='#0284c7', marker='*', markersize=12, linestyle='')
            ax.annotate(f"Delta: {format_ptbr(selected_delta, 2)} %/m³", 
                        (selected_vol, selected_delta), 
                        textcoords="offset points", xytext=(0, 8), ha='center',
                        fontsize=8, fontweight='bold', color='#0284c7')

        ax.set_xlabel(tr("Volume do Reservatório (L)"), color='#334155', fontsize=8, fontweight='bold')
        ax.set_ylabel(tr("Delta (%/m³)"), color='#dc2626', fontsize=8, fontweight='bold')
        ax.set_xlim(0, _sweep_xmax(sweep_results, selected_vol))
        ax.set_ylim(0, _upper_multiple(deltas + [delta_threshold] + ([selected_delta] if selected_delta is not None else []), 5))
        ax.tick_params(colors='#334155', labelsize=7.5)
        ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')

        if ax.get_legend_handles_labels()[0]:
            ax.legend(loc='upper right', facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.9, fontsize=7.5)
        for spine in ax.spines.values():
            spine.set_color('#cbd5e1')

        self.figure.tight_layout(pad=1.0)
        self.safe_draw()


class SpillAndConsumptionVsVolumeChart(TritonBaseChart):
    """Gráfico 3: extravasamento e consumo pluvial na mesma escala anual."""
    def __init__(self, parent=None):
        super().__init__("3. Volume Extravasado & Consumo Pluvial", parent)

    def update_chart(self, sweep_results=None, single_result=None):
        if not sweep_results and not single_result:
            self.plot_empty("Execute a simulação na Etapa 3")
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#f8fafc')

        selected_vol = single_result.lower_tank_vol if single_result else None
        selected_spill = single_result.annual_spill_m3 if single_result else None
        selected_pluvial = single_result.annual_pluvial_consumed_m3 if single_result else None

        if sweep_results and len(sweep_results) > 1:
            vols = [r.lower_tank_vol for r in sweep_results]
            spills = [r.annual_spill_m3 for r in sweep_results]
            pluvials = [r.annual_pluvial_consumed_m3 for r in sweep_results]

            ax.plot(vols, spills, color='#dc2626', linewidth=2.0, marker='s', markersize=3, label=tr("Extravasado (m³/ano)"))
            ax.plot(vols, pluvials, color='#0284c7', linewidth=2.0, marker='^', markersize=3, label=tr("Consumo Pluvial (m³/ano)"))
        else:
            spills = [selected_spill or 0.0]
            pluvials = [selected_pluvial or 0.0]

        if selected_vol is not None:
            if selected_spill is not None:
                ax.plot(selected_vol, selected_spill, color='#dc2626', marker='*', markersize=12, linestyle='')
                ax.annotate(f"{format_ptbr(selected_spill, 1)} m³", (selected_vol, selected_spill), textcoords="offset points", xytext=(0, 6), ha='center', fontsize=7.5, color='#dc2626', fontweight='bold')
            if selected_pluvial is not None:
                ax.plot(selected_vol, selected_pluvial, color='#0284c7', marker='*', markersize=12, linestyle='')
                ax.annotate(f"{format_ptbr(selected_pluvial, 1)} m³", (selected_vol, selected_pluvial), textcoords="offset points", xytext=(0, -12), ha='center', fontsize=7.5, color='#0284c7', fontweight='bold')

        ax.set_xlabel(tr("Volume do Reservatório (L)"), color='#334155', fontsize=8, fontweight='bold')
        ax.set_ylabel(tr("Volume Anual (m³/ano)"), color='#334155', fontsize=8, fontweight='bold')
        ax.set_xlim(0, _sweep_xmax(sweep_results, selected_vol))
        ax.set_ylim(0, _upper_multiple(spills + pluvials + ([selected_spill] if selected_spill is not None else []) + ([selected_pluvial] if selected_pluvial is not None else []), 50))
        ax.tick_params(colors='#334155', labelsize=7.5)
        ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')
        if ax.get_legend_handles_labels()[0]:
            ax.legend(loc='upper right', facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.9, fontsize=7.5)

        for spine in ax.spines.values():
            spine.set_color('#cbd5e1')

        self.figure.tight_layout(pad=1.0)
        self.safe_draw()


class StoredVolumeVsTankVolumeChart(TritonBaseChart):
    """Gráfico 5: Volume Médio Mantido no Reservatório (m³) vs Volume (L)."""
    def __init__(self, parent=None):
        super().__init__("5. Volume Médio Mantido no Reservatório (m³)", parent)

    def update_chart(self, sweep_results=None, single_result=None):
        if not sweep_results and not single_result:
            self.plot_empty(tr("Execute a simulação na Etapa 3"))
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#f8fafc')

        selected_vol = single_result.lower_tank_vol if single_result else None
        selected_stored = None

        if single_result and single_result.daily_results:
            selected_stored = float(np.mean([d.lower_tank_end_liters for d in single_result.daily_results])) / 1000.0

        if sweep_results and len(sweep_results) > 1:
            vols = [r.lower_tank_vol for r in sweep_results]
            avg_stored = []
            for r in sweep_results:
                if r.daily_results:
                    avg_stored.append(float(np.mean([d.lower_tank_end_liters for d in r.daily_results])) / 1000.0)
                else:
                    avg_stored.append((r.lower_tank_vol / 1000.0) * (min(r.pct_days_full_satisfaction + 20.0, 100.0) / 100.0))
            ax.plot(vols, avg_stored, color='#0284c7', linewidth=2.0, marker='^', markersize=3, label=tr("Vol. Médio (m³)"))
            ax.fill_between(vols, avg_stored, color='#e0f2fe', alpha=0.5)

            if selected_vol is not None:
                closest_r = min(sweep_results, key=lambda r: abs(r.lower_tank_vol - selected_vol))
                if closest_r.daily_results:
                    selected_stored = float(np.mean([d.lower_tank_end_liters for d in closest_r.daily_results])) / 1000.0

        if selected_vol is not None and selected_stored is not None:
            ax.plot(selected_vol, selected_stored, color='#dc2626', marker='*', markersize=12, linestyle='')
            ax.annotate(f"{format_ptbr(selected_stored, 1)} m³", 
                        (selected_vol, selected_stored), 
                        textcoords="offset points", xytext=(0, 8), ha='center',
                        fontsize=8, fontweight='bold', color='#dc2626')

        ax.set_xlabel(tr("Volume do Reservatório (L)"), color='#334155', fontsize=8, fontweight='bold')
        ax.set_ylabel(tr("Volume Reservado (m³)"), color='#0284c7', fontsize=8, fontweight='bold')
        ax.tick_params(colors='#334155', labelsize=7.5)
        ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')

        ax.legend(loc='upper left', facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.9, fontsize=7.5)
        for spine in ax.spines.values():
            spine.set_color('#cbd5e1')

        self.figure.tight_layout(pad=1.0)
        self.safe_draw()


class DailyBalanceTimeSeriesChart(TritonBaseChart):
    """Gráfico 6: Flutuação Diária do Nível da Cisterna (L) e Chuva (mm) ao Longo do Ano."""
    def __init__(self, parent=None):
        super().__init__("6. Flutuação Diária do Nível da Cisterna & Chuva", parent)

    def update_chart(self, single_result=None):
        if not single_result or not single_result.daily_results:
            self.plot_empty(tr("Execute a simulação na Etapa 3 para visualizar a série temporal diária"))
            return

        self.figure.clear()
        ax1 = self.figure.add_subplot(111)
        ax2 = ax1.twinx()

        ax1.set_facecolor('#f8fafc')

        days = [d.day_index for d in single_result.daily_results]
        precip = [d.precip_mm for d in single_result.daily_results]
        level_liters = [d.lower_tank_end_liters for d in single_result.daily_results]

        l1 = ax1.plot(days, level_liters, color='#0284c7', linewidth=1.5, label=tr("Nível Cisterna (L)"))
        l2 = ax2.bar(days, precip, color='#94a3b8', alpha=0.35, width=1.0, label=tr("Chuva (mm/dia)"))

        ax1.set_xlabel(tr("Dia do Ano (1-365)"), color='#334155', fontsize=8, fontweight='bold')
        ax1.set_ylabel(tr("Nível da Cisterna (L)"), color='#0284c7', fontsize=8, fontweight='bold')
        ax2.set_ylabel(tr("Chuva (mm/dia)"), color='#64748b', fontsize=8, fontweight='bold')

        ax1.tick_params(colors='#334155', labelsize=7.5)
        ax2.tick_params(colors='#334155', labelsize=7.5)
        ax1.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')

        lines = l1 + [l2]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right', facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.9, fontsize=7.5)

        for spine in ax1.spines.values():
            spine.set_color('#cbd5e1')

        self.figure.tight_layout(pad=1.0)
        self.safe_draw()


class DaysSatisfactionVsVolumeChart(TritonBaseChart):
    """Gráfico 4: Percentual de Atendimento dos Dias (%) vs Volume do Reservatório (L)."""
    def __init__(self, parent=None):
        super().__init__("4. Atendimento de Dias no Ano (%)", parent)

    def update_chart(self, sweep_results=None, single_result=None):
        if not sweep_results and not single_result:
            self.plot_empty(tr("Execute a simulação na Etapa 3"))
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#f8fafc')

        selected_vol = single_result.lower_tank_vol if single_result else None

        if sweep_results and len(sweep_results) > 1:
            vols = [r.lower_tank_vol for r in sweep_results]
            full_days = [r.pct_days_full_satisfaction for r in sweep_results]
            part_days = [r.pct_days_partial_satisfaction for r in sweep_results]
            null_days = [r.pct_days_null_satisfaction for r in sweep_results]

            ax.plot(vols, full_days, color='#16a34a', linewidth=1.8, label=tr("Atendimento Total (%)"))
            ax.plot(vols, part_days, color='#d97706', linewidth=1.6, linestyle='--', label=tr("Atendimento Parcial (%)"))
            ax.plot(vols, null_days, color='#dc2626', linewidth=1.6, linestyle=':', label=tr("Sem Atendimento (%)"))

        if single_result and selected_vol is not None:
            ax.plot(selected_vol, single_result.pct_days_full_satisfaction, color='#16a34a', marker='*', markersize=12, linestyle='')
            ax.annotate(f"{single_result.pct_days_full_satisfaction:.1f}% {tr('Total')}", 
                        (selected_vol, single_result.pct_days_full_satisfaction), 
                        textcoords="offset points", xytext=(0, 8), ha='center',
                        fontsize=8, fontweight='bold', color='#16a34a')

        ax.set_xlabel(tr("Volume do Reservatório (L)"), color='#334155', fontsize=8, fontweight='bold')
        ax.set_ylabel(tr("Dias (%)"), color='#334155', fontsize=8, fontweight='bold')
        ax.set_xlim(0, _sweep_xmax(sweep_results, selected_vol))
        ax.set_ylim(0, 100)
        ax.tick_params(colors='#334155', labelsize=7.5)
        ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')

        if ax.get_legend_handles_labels()[0]:
            ax.legend(loc='center right', facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.9, fontsize=7.5)
        for spine in ax.spines.values():
            spine.set_color('#cbd5e1')

        try:
            self.figure.tight_layout(pad=1.0)
        except Exception:
            pass
        self.canvas.draw()


class TOPSISComparisonChart(TritonBaseChart):
    """Gráfico da Pontuação Multi-Critério TOPSIS (C_i) ou Aceitabilidade SMAA-VIKOR (b_i^1) vs Volume do Reservatório."""
    def __init__(self, parent=None):
        super().__init__("", parent)

    def update_chart(self, topsis_result=None, smaa_result=None, method="topsis"):
        res = smaa_result if (method == "smaa_vikor" and smaa_result is not None) else (topsis_result or smaa_result)
        if not res or not hasattr(res, 'candidates') or not res.candidates:
            self.plot_empty(tr("Execute o recálculo para gerar a otimização multicritério"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#e2e8f0'

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)
        ax.set_title("")

        vols = [float(c.lower_tank_vol) for c in res.candidates]
        n_bars = len(vols)
        best_i = int(res.best_index)

        is_smaa = hasattr(res, "first_rank_probs") or method == "smaa_vikor"
        if is_smaa:
            # `first_rank_acceptabilities` é fração de 0 a 1, e o gráfico mostra
            # percentual. A conversão é fixa: multiplicar só o que fosse <= 1
            # misturava as duas unidades na mesma série de barras.
            raw_scores = getattr(res, "first_rank_acceptabilities", None)
            if raw_scores is not None:
                scores = [float(s) * 100.0 for s in raw_scores]
            elif getattr(res, "first_rank_probs", None) is not None:
                scores = [float(s) for s in res.first_rank_probs]  # já em percentual
            else:
                scores = [0.0] * n_bars
            y_label = tr("Aceitabilidade de 1º Lugar — SMAA-VIKOR (%)")
            val_fmt = lambda s: f"{s:.1f}%"
            annot_best_label = tr("Ótimo SMAA-VIKOR")
            samples_str = milhar(f" ({res.num_simulations:,} simulações)") if hasattr(res, "num_simulations") else ""
            annot_text = f"{annot_best_label}: {vols[best_i]:.0f} L ({scores[best_i]:.1f}%{samples_str})"

            # Eixo Y como múltiplo de 20 imediatamente superior ao maior valor
            highest_score = max(scores) if scores else 0.0
            if highest_score <= 0.0:
                max_y = 20.0
            else:
                max_y = float((floor(highest_score / 20.0) + 1) * 20.0)
        else:
            scores = [float(s) for s in getattr(res, "scores", [0.0]*n_bars)]
            y_label = tr("Escore TOPSIS")
            val_fmt = lambda s: f"{s:.2f}"
            annot_best_label = tr("Ótimo TOPSIS")
            annot_text = f"{annot_best_label}: {vols[best_i]:.0f} L ({scores[best_i]:.2f})"
            # O escore vai de 0 a 1; a folga até 1,2 abriga a anotação do ótimo.
            max_y = 1.20

        if n_bars <= 15:
            # Gráfico de barras discreto para poucas alternativas
            bars = ax.bar(range(n_bars), scores, color='#6366f1', alpha=0.85, width=0.45, edgecolor='#4f46e5', linewidth=1.2)
            if best_i < len(bars):
                bars[best_i].set_color('#10b981')
                bars[best_i].set_edgecolor('#059669')
                bars[best_i].set_linewidth(2.0)

            for idx, (b, sc) in enumerate(zip(bars, scores)):
                yval = b.get_height()
                y_text = yval + (max_y * 0.02)
                ax.text(
                    b.get_x() + b.get_width()/2.0, y_text, val_fmt(sc),
                    ha='center', va='bottom', fontsize=8, fontweight='bold', color=text_color,
                    clip_on=False
                )

            if best_i < len(bars):
                best_bar = bars[best_i]
                star_y = best_bar.get_height() + (max_y * 0.07)
                ax.text(
                    best_bar.get_x() + best_bar.get_width() / 2.0,
                    star_y,
                    "★", ha='center', va='bottom', fontsize=14, fontweight='bold', color='#059669',
                    clip_on=False
                )

            rot_x = 45 if n_bars > 8 else 0
            ha_x = 'right' if n_bars > 8 else 'center'
            ax.set_xticks(range(n_bars))
            ax.set_xticklabels([f"{v:.0f} L" for v in vols], rotation=rot_x, ha=ha_x, fontsize=8, color=text_color)
        else:
            # Curva contínua para varreduras longas (> 15 alternativas)
            ax.plot(vols, scores, color='#4f46e5', linewidth=2.2, label=y_label)
            ax.fill_between(vols, scores, color='#6366f1', alpha=0.15)

            best_vol = vols[best_i]
            best_score = scores[best_i]

            ax.plot(best_vol, best_score, marker='*', markersize=14, color='#10b981', markeredgecolor='#059669', markeredgewidth=1.5, zorder=5)
            ax.annotate(
                annot_text,
                xy=(best_vol, best_score),
                xytext=(best_vol, min(max_y * 0.92, best_score + max_y * 0.08)),
                ha='center', va='bottom',
                fontsize=8.5, fontweight='bold', color='#059669',
                arrowprops=dict(arrowstyle='->', color='#059669', lw=1.2)
            )

        ax.set_ylim(0, max_y)
        if n_bars > 15:
            ax.set_xlim(0.0, _upper_multiple(vols, 1000.0))
        if not is_smaa:
            import matplotlib.ticker as ticker
            ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
        if is_smaa:
            import matplotlib.ticker as ticker
            step_ticks = 20.0 if max_y >= 40.0 else 10.0
            ax.yaxis.set_major_locator(ticker.MultipleLocator(step_ticks))
        ax.set_xlabel(tr("Volume do Reservatório Inferior (Litros)"), color=text_color, fontsize=8.5, fontweight='bold')
        ax.set_ylabel(y_label, color=text_color, fontsize=8.5, fontweight='bold')
        ax.tick_params(colors=text_color, labelsize=8)
        ax.grid(True, axis='y', linestyle=':', alpha=0.6, color=grid_color)

        for spine in ax.spines.values():
            spine.set_color(grid_color)

        try:
            bot_margin = 0.22 if n_bars > 8 else 0.15
            self.figure.subplots_adjust(left=0.08, bottom=bot_margin, right=0.96, top=0.88)
        except Exception:
            pass
        self.safe_draw()


class TOPSISProximityChart(TritonBaseChart):
    """Proximidade relativa aos sete critérios usados na análise multicritério.

    A escala é adimensional e independente dos pesos: 100% significa que o
    volume atinge o melhor valor observado no eixo; 0%, o pior. O gráfico
    complementa o escore agregado e torna visível se a solução ótima é uma
    alternativa próxima dos três ótimos ou uma concessão assimétrica.
    """

    def __init__(self, parent=None):
        super().__init__("", parent)

    def update_chart(self, topsis_result=None, selected_best_index=None, method_label="TOPSIS"):
        proximity = getattr(topsis_result, "criterion_proximity_to_best", None) if topsis_result else None
        if proximity is None or not getattr(topsis_result, "candidates", None):
            self.plot_empty(tr("Execute o recálculo para gerar as proximidades aos ótimos"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = "#18181b" if is_dark else "#ffffff"
        text_color = "#f4f4f5" if is_dark else "#0f172a"
        grid_color = "#3f3f46" if is_dark else "#e2e8f0"

        proximity_pct = np.asarray(proximity, dtype=float) * 100.0
        vols = np.asarray([float(c.lower_tank_vol) for c in topsis_result.candidates], dtype=float)
        original_best_i = int(selected_best_index if selected_best_index is not None else topsis_result.best_index)
        order = np.argsort(vols, kind="stable")
        vols = vols[order]
        proximity_pct = proximity_pct[order]
        best_i = int(np.flatnonzero(order == original_best_i)[0])

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)

        labels = getattr(topsis_result, "criterion_labels", ())
        series = (
            (tr(labels[0] if len(labels) > 0 else "Potencial máximo"), "#0284c7", "o"),
            (tr(labels[1] if len(labels) > 1 else "Mínimo extravasamento"), "#0ea5e9", "v"),
            (tr(labels[2] if len(labels) > 2 else "Maior VPL"), "#16a34a", "s"),
            (tr(labels[3] if len(labels) > 3 else "Menor payback descontado"), "#65a30d", "P"),
            (tr(labels[4] if len(labels) > 4 else "Maior TIR"), "#059669", "D"),
            (tr(labels[5] if len(labels) > 5 else "Menor CO₂ no fim da vida"), "#d97706", "^"),
            (tr(labels[6] if len(labels) > 6 else "Menor consumo de água potável"), "#9333ea", "X"),
        )
        for col, (label, color, marker) in enumerate(series):
            ax.plot(
                vols, proximity_pct[:, col], label=label, color=color, linewidth=2.0,
                marker=marker, markersize=4.0, alpha=0.92,
            )
            ax.scatter(
                [vols[best_i]], [proximity_pct[best_i, col]], s=65, color=color,
                marker=marker, edgecolor=text_color, linewidth=0.8, zorder=6,
            )

        selected_vol = vols[best_i]
        tag = tr("SMAA-VIKOR") if "smaa" in method_label.lower() or "vikor" in method_label.lower() else tr("TOPSIS")
        ax.axvline(selected_vol, color="#7c3aed", linestyle="--", linewidth=1.4, alpha=0.9)
        ax.annotate(
            f"{tag}: {selected_vol:.0f} L",
            xy=(selected_vol, min(100.0, float(np.max(proximity_pct[best_i])))),
            xytext=(6, 8), textcoords="offset points", fontsize=8.5,
            fontweight="bold", color="#7c3aed",
        )

        ax.set_ylim(-3, 105)
        if len(vols) == 1:
            ax.set_xlim(vols[0] - 1.0, vols[0] + 1.0)
        ax.set_xlabel(tr("Volume do Reservatório Inferior (Litros)"), color=text_color, fontsize=8.5, fontweight="bold")
        ax.set_ylabel(tr("Proximidade relativa ao ótimo do critério (%)"), color=text_color, fontsize=8.5, fontweight="bold")
        ax.tick_params(colors=text_color, labelsize=8)
        ax.grid(True, linestyle=":", alpha=0.6, color=grid_color)
        legend = ax.legend(loc="best", fontsize=7, ncol=2, frameon=True)
        legend.get_frame().set_facecolor(bg_color)
        legend.get_frame().set_edgecolor(grid_color)
        for label in legend.get_texts():
            label.set_color(text_color)
        for spine in ax.spines.values():
            spine.set_color(grid_color)

        try:
            self.figure.subplots_adjust(left=0.09, bottom=0.17, right=0.97, top=0.94)
        except Exception:
            pass
        self.safe_draw()


# Nome histórico preservado para integrações que importavam o gráfico antigo.
TOPSISDistanceChart = TOPSISProximityChart


class VplVsVolumeChart(TritonBaseChart):
    """Gráfico da Varredura Econômica vs Volume do Reservatório (VPL, TIR, Paybacks e Custos)."""
    def __init__(self, parent=None):
        super().__init__("Indicadores Financeiros vs Volume do Reservatório", parent)

    def update_chart(
        self,
        sweep_data=None,
        metric="vpl",
        currency_symbol="R$",
        optimal_tech_vol=None,
        tma_rate=None
    ):
        if not sweep_data:
            self.plot_empty(tr("Execute a simulação na Etapa 3 para visualizar os indicadores econômicos por volume"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#e2e8f0'

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)

        # Normaliza sweep_data para dicionário ou lista de dicionários
        items = []
        if isinstance(sweep_data, dict):
            items = list(sweep_data.values())
        elif isinstance(sweep_data, list):
            if len(sweep_data) > 0 and isinstance(sweep_data[0], dict):
                items = sweep_data
            else:
                # Formato legado: [(vol, vpl), ...]
                items = [{"volume_l": float(v[0]), "vpl": float(v[1])} for v in sweep_data]

        if not items:
            self.plot_empty(tr("Nenhum dado de varredura disponível"))
            return

        items = sorted(items, key=lambda d: d.get("volume_l", 0.0))
        vols = [float(d.get("volume_l", 0.0)) for d in items]

        if metric == "vpl":
            vals = [float(d.get("vpl", 0.0)) for d in items]
            ax.plot(vols, vals, color='#0284c7', linewidth=2.2, marker='o', markersize=4.5, label=f"{tr('VPL Líquido')} ({currency_symbol})")
            ax.axhline(y=0, color='#94a3b8', linestyle='--', linewidth=1.0)

            best_idx = int(np.argmax(vals))
            best_vol = vols[best_idx]
            best_val = vals[best_idx]

            tech_idx = int(np.argmin([abs(v - optimal_tech_vol) for v in vols])) if optimal_tech_vol is not None else None
            same_opt = (tech_idx is not None and tech_idx == best_idx)

            if same_opt:
                ax.plot(best_vol, best_val, color='#eab308', marker='*', markersize=16, linestyle='',
                        markeredgecolor='#a16207', markeredgewidth=1.2,
                        label=f"{tr('Ótimo Técnico = Econômico')}: {format_ptbr(best_vol, 0)} L ({currency_symbol} {format_ptbr(best_val, 2)})")
            else:
                ax.plot(best_vol, best_val, color='#059669', marker='*', markersize=14, linestyle='',
                        markeredgecolor='#047857', markeredgewidth=1.0,
                        label=f"{tr('VPL Máximo')}: {format_ptbr(best_vol, 0)} L ({currency_symbol} {format_ptbr(best_val, 2)})")
                if tech_idx is not None:
                    t_vol = vols[tech_idx]; t_val = vals[tech_idx]
                    ax.plot(t_vol, t_val, color='#0284c7', marker='D', markersize=10, linestyle='',
                            markeredgecolor='#0369a1', markeredgewidth=1.2,
                            label=f"{tr('Ótimo Técnico')}: {format_ptbr(t_vol, 0)} L ({currency_symbol} {format_ptbr(t_val, 2)})")

            ax.set_ylabel(f"{tr('VPL Líquido')} ({currency_symbol})", color=text_color, fontsize=8.5, fontweight='bold')

        elif metric == "tir":
            vals = [float(d.get("tir", 0.0)) for d in items]
            ax.plot(vols, vals, color='#10b981', linewidth=2.2, marker='o', markersize=4.5, label=tr("TIR (% a.a.)"))
            if tma_rate is not None and tma_rate > 0:
                ax.axhline(y=tma_rate, color='#ef4444', linestyle=':', linewidth=1.3, label=f"TMA ({tma_rate:.1f}% a.a.)")
            else:
                ax.axhline(y=0, color='#94a3b8', linestyle='--', linewidth=0.9)

            best_idx = int(np.argmax(vals))
            best_vol = vols[best_idx]; best_val = vals[best_idx]
            ax.plot(best_vol, best_val, color='#059669', marker='*', markersize=14, linestyle='',
                    markeredgecolor='#047857', markeredgewidth=1.0,
                    label=f"{tr('TIR Máxima')}: {format_ptbr(best_vol, 0)} L ({format_ptbr(best_val, 1)}% a.a.)")

            ax.set_ylabel(tr("Taxa Interna de Retorno — TIR (% a.a.)"), color=text_color, fontsize=8.5, fontweight='bold')

        elif metric in ("payback_simple", "payback_discounted"):
            is_disc = (metric == "payback_discounted")
            key = "payback_discounted" if is_disc else "payback_simple"
            raw_vals = [d.get(key, d.get("payback")) for d in items]
            plot_vals = [float(v) if (v is not None and float(v) > 0 and float(v) < 90) else np.nan for v in raw_vals]

            lbl_name = tr("Payback Descontado (Anos)") if is_disc else tr("Payback Simples (Anos)")
            color_line = '#d97706' if is_disc else '#0891b2'

            ax.plot(vols, plot_vals, color=color_line, linewidth=2.2, marker='s', markersize=4.5, label=lbl_name)

            # Destaca menor tempo de retorno viável
            valid_pts = [(v, p) for v, p in zip(vols, plot_vals) if not np.isnan(p)]
            if valid_pts:
                best_vol, min_pb = min(valid_pts, key=lambda t: t[1])
                ax.plot(best_vol, min_pb, color='#059669', marker='*', markersize=14, linestyle='',
                        markeredgecolor='#047857', markeredgewidth=1.0,
                        label=f"{tr('Ótimo Econômico (Menor Payback)')}: {format_ptbr(best_vol, 0)} L ({format_ptbr(min_pb, 1)}a)")

            ax.set_ylabel(lbl_name, color=text_color, fontsize=8.5, fontweight='bold')

        elif metric == "costs":
            capex_vals = [float(d.get("capex", 0.0)) for d in items]
            opex_vals = [float(d.get("total_opex", d.get("opex_annual", 0.0) * 20.0)) for d in items]
            total_cost_vals = [c + o for c, o in zip(capex_vals, opex_vals)]

            ax.plot(vols, capex_vals, color='#3b82f6', linewidth=2.0, marker='o', markersize=4, label=f"{tr('CAPEX Inicial')} ({currency_symbol})")
            ax.plot(vols, opex_vals, color='#f59e0b', linewidth=2.0, marker='^', markersize=4, label=f"{tr('OPEX Acumulado (20 anos)')} ({currency_symbol})")
            ax.plot(vols, total_cost_vals, color='#ef4444', linewidth=2.4, marker='s', markersize=4.5, label=f"{tr('Custo Global Total (CAPEX + OPEX)')} ({currency_symbol})")

            ax.set_ylabel(f"{tr('Custos do Sistema')} ({currency_symbol})", color=text_color, fontsize=8.5, fontweight='bold')

        elif metric == "opex_annual":
            annual_opex_vals = [float(d.get("annual_opex", 0.0)) for d in items]
            ax.plot(vols, annual_opex_vals, color='#d97706', linewidth=2.2, marker='o', markersize=4.5, label=f"{tr('OPEX Anual (1º ano)')} ({currency_symbol}/ano)")

            ax.set_ylabel(f"{tr('Custo Operacional Anual')} ({currency_symbol}/ano)", color=text_color, fontsize=8.5, fontweight='bold')

        ax.set_xlabel(tr("Volume do Reservatório (Litros)"), color=text_color, fontsize=8.5, fontweight='bold')
        from matplotlib.ticker import FuncFormatter, MaxNLocator
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: milhar(f"{int(x):,}")))
        ax.tick_params(axis='x', colors=text_color, labelsize=8.5, pad=4)
        ax.tick_params(axis='y', colors=text_color, labelsize=8)
        ax.grid(True, linestyle=':', alpha=0.6, color=grid_color)
        ax.legend(fontsize=8, loc='best', facecolor=bg_color, edgecolor=grid_color, labelcolor=text_color)

        if vols:
            ax.set_xlim(left=0, right=_upper_multiple(vols, 1000.0 if max(vols, default=0) >= 5000 else 500.0))

        for spine in ax.spines.values():
            spine.set_color(grid_color)

        try:
            self.figure.subplots_adjust(left=0.18, bottom=0.19, right=0.96, top=0.92)
        except Exception:
            try:
                self.figure.tight_layout(pad=1.2)
            except Exception:
                pass
        self.safe_draw()


class EnvironmentalBalanceSummaryChart(TritonBaseChart):
    """Decompõe os fatores que formam o saldo climático do sistema ao longo da vida útil."""
    def __init__(self, parent=None):
        super().__init__("Contribuições para o Balanço de Carbono (20 Anos)", parent)

    def update_chart(self, lca_result=None, lifespan_years=20.0):
        if not lca_result:
            self.plot_empty(tr("Execute a simulação na Etapa 3 para visualizar o balanço ambiental"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#cbd5e1'

        avoided = lca_result.annual_avoided_co2_kg * lifespan_years
        embodied = lca_result.total_embodied_co2_kg
        operational = (lca_result.annual_pumping_co2_kg + lca_result.annual_treatment_co2_kg) * lifespan_years
        # Convenção solicitada:
        # Negativo (-) = Retirada / Evitação de CO2
        # Positivo (+) = Emissões de CO2
        net_balance = (embodied + operational) - avoided
        labels = [
            tr("Retirada de CO2 (Água Evitada)"),
            tr("Emissão Incorporada (Materiais)"),
            tr("Emissão Operacional (Energia & Cloro)"),
            tr("Saldo Líquido (Balanço em 20 Anos)"),
        ]
        values = [-avoided, embodied, operational, net_balance]
        net_color = '#10b981' if net_balance <= 0 else '#ef4444'
        colors = ['#10b981', '#0284c7', '#f59e0b', net_color]

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)
        bars = ax.barh(range(len(values)), values, color=colors, alpha=0.9, height=0.58)
        ax.axvline(0, color=text_color, linewidth=0.9)
        span = max(1.0, max(abs(value) for value in values))

        from matplotlib import patheffects
        stroke_emerald = [patheffects.withStroke(linewidth=2.5, foreground='#064e3b' if is_dark else '#047857')]
        stroke_blue = [patheffects.withStroke(linewidth=2.5, foreground='#0c4a6e' if is_dark else '#0369a1')]

        # Posicionamento inteligente dos valores numéricos para evitar qualquer
        # sobreposição com os rótulos de categoria à esquerda ou cortes na moldura:
        for bar, value in zip(bars, values):
            prefix = "+" if value > 0 else ""
            txt_str = f"{prefix}{format_ptbr(value, 0)} kg"
            y_pos = bar.get_y() + bar.get_height() / 2

            if value < 0:
                # Barras negativas crescem para a esquerda (de 0 até value).
                # Se a barra tem largura suficiente (> 18% do span), o texto fica
                # por DENTRO da barra (em direção ao 0), em branco com contorno contrastante.
                # Isso elimina a colisão com os rótulos do eixo Y à esquerda da moldura.
                # Se for muito curta (<= 18%), fica por fora à esquerda mas ainda próxima de zero.
                if abs(value) > 0.18 * span:
                    posicao = value + 0.03 * span
                    ax.text(posicao, y_pos, txt_str, va='center', ha='left',
                            fontsize=8, fontweight='bold', color='#ffffff',
                            path_effects=stroke_emerald)
                else:
                    posicao = value - 0.03 * span
                    ax.text(posicao, y_pos, txt_str, va='center', ha='right',
                            fontsize=8, fontweight='bold', color=text_color)
            else:
                # Barras positivas crescem para a direita.
                if value > 0.65 * span:
                    posicao = value - 0.03 * span
                    ax.text(posicao, y_pos, txt_str, va='center', ha='right',
                            fontsize=8, fontweight='bold', color='#ffffff',
                            path_effects=stroke_blue)
                else:
                    posicao = value + 0.03 * span
                    ax.text(posicao, y_pos, txt_str, va='center', ha='left',
                            fontsize=8, fontweight='bold', color=text_color)

        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=8, color=text_color)
        ax.invert_yaxis()
        ax.set_xlabel(tr("Carbono no ciclo de vida (kg CO2e em 20 anos)\nnegativo retira, positivo emite"), color=text_color, fontsize=8, fontweight='bold')
        ax.tick_params(colors=text_color, labelsize=7.5)
        ax.grid(True, axis='x', linestyle=':', alpha=0.6, color=grid_color)
        ax.set_xlim(min(-span * 1.35, -1), max(span * 1.35, 1))
        for spine in ax.spines.values():
            spine.set_color(grid_color)
        try:
            self.figure.tight_layout(pad=0.9)
        except Exception:
            pass
        self.safe_draw()


class CO2ComparisonChart(TritonBaseChart):
    """Gráfico Comparativo de Emissão Total de CO2 na Vida Útil (20 Anos): Sem Sistema vs Com Sistema."""
    def __init__(self, parent=None):
        super().__init__("Comparativo de Emissão Total de CO2 na Vida Útil (20 Anos)", parent)

    def update_chart(self, lca_result=None, total_demand_m3=200.0, lifespan_years=20.0):
        if not lca_result:
            self.plot_empty(tr("Execute a simulação na Etapa 3 para visualizar o comparativo de CO2"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#cbd5e1'

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)

        water_saved_annual = getattr(lca_result, 'annual_water_saved_m3', getattr(lca_result, 'annual_pluvial_m3', 0.0))
        potable_residual_annual = max(0.0, total_demand_m3 - water_saved_annual)

        # O fator da água potável evitada era 0,35 fixo aqui, de modo que editá-lo
        # na interface não mudava este gráfico. Recupera-se agora o fator
        # efetivamente usado no cálculo, já que
        # `annual_avoided_co2_kg = annual_pluvial_m3 × potable_water_co2_kg_m3`.
        pluvial_annual = getattr(lca_result, 'annual_pluvial_m3', 0.0) or 0.0
        avoided_annual = getattr(lca_result, 'annual_avoided_co2_kg', 0.0) or 0.0
        if pluvial_annual > 0:
            potable_co2_factor = avoided_annual / pluvial_annual
        else:
            from triton.core.environmental import potable_water_factor_default
            potable_co2_factor = potable_water_factor_default()

        baseline_co2_lifetime = total_demand_m3 * potable_co2_factor * lifespan_years
        system_embodied = lca_result.total_embodied_co2_kg
        system_op_lifetime = (lca_result.annual_pumping_co2_kg + lca_result.annual_treatment_co2_kg) * lifespan_years
        system_potable_lifetime = potable_residual_annual * potable_co2_factor * lifespan_years
        system_total_co2_lifetime = system_embodied + system_op_lifetime + system_potable_lifetime

        net_avoided = baseline_co2_lifetime - system_total_co2_lifetime

        categories = [
            tr("Sem Sistema\n(100% Rede)"),
            tr("Com Sistema\nPluvial")
        ]
        values = [baseline_co2_lifetime, system_total_co2_lifetime]
        colors = ['#ef4444', '#10b981']

        bars = ax.bar(range(2), values, color=colors, alpha=0.85, width=0.42, edgecolor=colors, linewidth=1.2)

        for b, v in zip(bars, values):
            yval = b.get_height()
            ax.text(b.get_x() + b.get_width()/2.0, yval + (max(values)*0.02), f"{format_ptbr(v, 0)} kg",
                    ha='center', va='bottom', fontsize=8, fontweight='bold', color=text_color)

        reduction_pct = (net_avoided / baseline_co2_lifetime * 100.0) if baseline_co2_lifetime else 0.0
        ax.text(
            0.5, 0.96,
            f"{tr('Retirada / Redução estimada')}: -{format_ptbr(net_avoided, 0)} kg CO2e ({format_ptbr(reduction_pct, 1)}%)",
            transform=ax.transAxes, ha='center', va='top', fontsize=8.5, fontweight='bold',
            color='#059669', bbox=dict(boxstyle='round,pad=0.35', facecolor='#dcfce7', edgecolor='#86efac'),
        )

        ax.set_xticks(range(2))
        ax.set_xticklabels(categories, fontsize=8, color=text_color)
        ax.set_ylim(0, max(1.0, max(values) * 1.25))
        ax.set_ylabel(tr("Emissão Total (kg CO2e / 20 Anos)"), color=text_color, fontsize=8, fontweight='bold')
        ax.tick_params(colors=text_color, labelsize=8)
        ax.grid(True, axis='y', linestyle=':', alpha=0.6, color=grid_color)

        for spine in ax.spines.values():
            spine.set_color(grid_color)

        try:
            self.figure.tight_layout(pad=0.8)
        except Exception:
            pass
        self.safe_draw()


class LCAComponentBreakdownChart(TritonBaseChart):
    """Gráfico Empilhado por Volume: Emissões (+kg) vs Retirada da Água Potável (-kg)."""
    def __init__(self, parent=None):
        super().__init__("Balanço Acumulado de CO2 por Volume da Cisterna", parent)

    def update_chart(self, lca_result=None, sweep_details=None):
        if not lca_result and not sweep_details:
            self.plot_empty(tr("Execute a simulação na Etapa 3 para visualizar o balanço ambiental"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#cbd5e1'

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)

        if sweep_details:
            vols = [d["volume_l"] for d in sweep_details]
            x_indices = np.arange(len(vols))
            bar_width = 0.45

            # Componentes Positivos (+ CO2): Materiais + Energia Operacional
            pos_emb = np.array([d.get("embodied_co2_kg", 0.0) for d in sweep_details])
            pos_op = np.array([d.get("op_co2_lifetime_kg", 0.0) for d in sweep_details])

            # Componente Negativo (- CO2): Retirada / Offset da Água Potável Economizada
            neg_offset = np.array([-abs(d.get("offset_co2_lifetime_kg", d.get("annual_m3", 0.0)*0.35*20.0)) for d in sweep_details])

            # Saldo Líquido Acumulado: (Emissões) - (Retirada)
            # Se retirou mais do que emitiu, o saldo líquido é NEGATIVO!
            net_line = np.array([(d.get("embodied_co2_kg", 0.0) + d.get("op_co2_lifetime_kg", 0.0)) - abs(d.get("offset_co2_lifetime_kg", d.get("annual_m3", 0.0)*0.35*20.0)) for d in sweep_details])

            # Empilhamento no Eixo Positivo (Materiais + Operação)
            ax.bar(x_indices, pos_emb, width=bar_width, color='#0284c7', alpha=0.85, label=tr("Emissões Materiais (+kg)"), edgecolor='#0284c7')
            ax.bar(x_indices, pos_op, bottom=pos_emb, width=bar_width, color='#d97706', alpha=0.85, label=tr("Emissões Energia & Cloração (+kg)"), edgecolor='#d97706')

            # Barra no Eixo Negativo (Retirada / Offset)
            ax.bar(x_indices, neg_offset, width=bar_width, color='#10b981', alpha=0.85, label=tr("Retirada Água Potável (-kg)"), edgecolor='#059669')

            # Linha do Saldo Líquido de Carbono (Linha Roxa)
            ax.plot(x_indices, net_line, color='#8b5cf6', linewidth=2.2, marker='o', markersize=5, label=tr("Saldo Líquido [- Retirada] (kg CO2e)"))

            ax.axhline(y=0, color=text_color, linestyle='-', linewidth=0.9, alpha=0.8)

            ax.set_xticks(x_indices)
            ax.set_xticklabels([f"{v:.0f} L" for v in vols], rotation=45, ha='right', fontsize=8, color=text_color)
            ax.set_xlabel(tr("Volume Inferior do Reservatório (Litros)"), color=text_color, fontsize=8, fontweight='bold')
            ax.set_ylabel(tr("Carbono em 20 Anos: [- Retirada / + Emissão] (kg CO2e)"), color=text_color, fontsize=8, fontweight='bold')
            ax.tick_params(colors=text_color, labelsize=7.5)
            ax.grid(True, axis='y', linestyle=':', alpha=0.6, color=grid_color)
            ax.legend(fontsize=7, loc='best', facecolor=bg_color, edgecolor=grid_color, labelcolor=text_color)
        else:
            emb = lca_result.total_embodied_co2_kg
            op = (lca_result.annual_pumping_co2_kg + lca_result.annual_treatment_co2_kg) * 20.0
            avoided = -(lca_result.annual_avoided_co2_kg * 20.0)

            ax.bar([0], [emb], width=0.4, color='#0284c7', label=tr("Emissões Materiais (+kg)"))
            ax.bar([0], [op], bottom=[emb], width=0.4, color='#d97706', label=tr("Emissões Operação (+kg)"))
            ax.bar([1], [avoided], width=0.4, color='#10b981', label=tr("Retirada Água Potável (-kg)"))
            ax.axhline(y=0, color=text_color, linestyle='-', linewidth=0.9)
            ax.set_xticks([0, 1])
            ax.set_xticklabels([tr("Emissões (+kg)"), tr("Retirada (-kg)")], fontsize=8, color=text_color)
            ax.set_ylabel(tr("Carbono acumulado (kg CO2e)\nnegativo retira, positivo emite"), color=text_color, fontsize=8, fontweight='bold')
            ax.legend(fontsize=7, loc='best')

        for spine in ax.spines.values():
            spine.set_color(grid_color)

        try:
            self.figure.subplots_adjust(left=0.16, bottom=0.24, right=0.96, top=0.90)
        except Exception:
            try:
                self.figure.tight_layout(pad=1.2)
            except Exception:
                pass
        self.safe_draw()


class PrcptotAnnualChart(TritonBaseChart):
    """Gráfico de Precipitação Total Anual (PRCPTOT em mm/ano)."""
    def __init__(self, parent=None):
        super().__init__("Precipitação Total Anual (PRCPTOT)", parent, aspect_ratio=(32, 9), min_height=130)

    def plot_data(self, df_indices):
        if df_indices is None or df_indices.empty or 'PRCPTOT' not in df_indices.columns:
            self.plot_empty(tr("Carregue uma série de precipitação para visualizar o gráfico"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#cbd5e1'

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)

        # O calculador devolve o ano numa coluna, e o indice e apenas
        # posicional: usar o indice rotulava o eixo «Ano» com 0, 1, 2...
        years = (df_indices["year"] if "year" in df_indices.columns
                 else df_indices.index).astype(int)
        prcp = df_indices['PRCPTOT'].values
        mean_prcp = np.mean(prcp)

        bars = ax.bar(years, prcp, color='#0284c7', alpha=0.85, width=0.65, label=tr("PRCPTOT (mm/ano)"))
        ax.axhline(mean_prcp, color='#ef4444', linestyle='--', linewidth=1.8, label=f"{tr('Média')}: {mean_prcp:.1f} mm")

        ax.set_xlabel(tr("Ano"), color=text_color, fontsize=8, fontweight='bold')
        ax.set_ylabel(tr("Precipitação Anual (mm)"), color=text_color, fontsize=8, fontweight='bold')
        ax.tick_params(colors=text_color, labelsize=7.5)
        ax.grid(True, axis='y', linestyle=':', alpha=0.6, color=grid_color)
        # O eixo começa em zero e termina num múltiplo de 500 mm, e a legenda
        # fica acima da área do gráfico: dentro dela cobria as barras mais altas.
        from matplotlib.ticker import MultipleLocator
        ax.set_ylim(0.0, _upper_multiple([float(v) * 1.04 for v in prcp], 500.0))
        ax.yaxis.set_major_locator(MultipleLocator(500.0))
        ax.legend(fontsize=7.5, loc='lower right', bbox_to_anchor=(1.0, 1.0), ncol=2,
                  frameon=False, labelcolor=text_color)

        for spine in ax.spines.values():
            spine.set_color(grid_color)

        try:
            self.figure.tight_layout(pad=0.8)
        except Exception:
            pass
        self.safe_draw()


class SdiiVsR95pChart(TritonBaseChart):
    """Gráfico de Intensidade Diária (SDII) vs Chuva Extrema (R95p)."""
    def __init__(self, parent=None):
        super().__init__("Intensidade (SDII) & Extremos (R95p)", parent, aspect_ratio=(32, 9), min_height=130)

    def plot_data(self, df_indices):
        if df_indices is None or df_indices.empty or 'SDII' not in df_indices.columns:
            self.plot_empty(tr("Carregue uma série de precipitação para visualizar o gráfico"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#cbd5e1'

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax1 = self.figure.add_subplot(111)
        ax2 = ax1.twinx()
        ax1.set_facecolor(bg_color)

        # O calculador devolve o ano numa coluna, e o indice e apenas
        # posicional: usar o indice rotulava o eixo «Ano» com 0, 1, 2...
        years = (df_indices["year"] if "year" in df_indices.columns
                 else df_indices.index).astype(int)
        sdii = df_indices['SDII'].values
        r95p = df_indices['R95p'].values

        l1 = ax1.plot(years, sdii, color='#d97706', linewidth=2.0, marker='o', markersize=4, label=tr("SDII (mm/dia úmido)"))
        l2 = ax2.bar(years, r95p, color='#10b981', alpha=0.4, width=0.5, label=tr("R95p (mm > P95)"))

        ax1.set_xlabel(tr("Ano"), color=text_color, fontsize=8, fontweight='bold')
        ax1.set_ylabel(tr("SDII (mm/dia)"), color='#d97706', fontsize=8, fontweight='bold')
        ax2.set_ylabel(tr("R95p Extremo (mm)"), color='#10b981', fontsize=8, fontweight='bold')

        ax1.tick_params(colors=text_color, labelsize=7.5)
        ax2.tick_params(colors=text_color, labelsize=7.5)
        ax1.grid(True, linestyle=':', alpha=0.6, color=grid_color)

        lines = l1 + [l2]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', facecolor=bg_color, edgecolor=grid_color, labelcolor=text_color, fontsize=7.5)

        for spine in ax1.spines.values():
            spine.set_color(grid_color)
        for spine in ax2.spines.values():
            spine.set_color(grid_color)

        try:
            self.figure.tight_layout(pad=0.8)
        except Exception:
            pass
        self.safe_draw()


class CddCwdAnnualChart(TritonBaseChart):
    """Gráfico de Estiagens (CDD) vs Dias Chuvosos Consecutivos (CWD)."""
    def __init__(self, parent=None):
        super().__init__("Estiagens (CDD) vs Dias Chuvosos (CWD)", parent, aspect_ratio=(32, 9), min_height=130)

    def plot_data(self, df_indices):
        if df_indices is None or df_indices.empty or 'CDD' not in df_indices.columns:
            self.plot_empty(tr("Carregue uma série de precipitação para visualizar o gráfico"))
            return

        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#cbd5e1'

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)

        # O calculador devolve o ano numa coluna, e o indice e apenas
        # posicional: usar o indice rotulava o eixo «Ano» com 0, 1, 2...
        years = (df_indices["year"] if "year" in df_indices.columns
                 else df_indices.index).astype(int)
        cdd = df_indices['CDD'].values
        cwd = df_indices['CWD'].values

        ax.plot(years, cdd, color='#dc2626', linewidth=2.0, marker='s', markersize=4, label=tr("CDD — Máx. Dias Secos"))
        ax.plot(years, cwd, color='#059669', linewidth=2.0, marker='^', markersize=4, label=tr("CWD — Máx. Dias Chuvosos"))

        ax.set_xlabel(tr("Ano"), color=text_color, fontsize=8, fontweight='bold')
        ax.set_ylabel(tr("Duração Contínua (Dias)"), color=text_color, fontsize=8, fontweight='bold')
        ax.tick_params(colors=text_color, labelsize=7.5)
        ax.grid(True, linestyle=':', alpha=0.6, color=grid_color)
        # O eixo começa em zero e termina num múltiplo de 2,5 dias; acima de
        # 30 dias as marcas passam a 5, que continua múltiplo de 2,5. A legenda
        # fica acima do gráfico, fora das linhas.
        from matplotlib.ticker import MultipleLocator
        teto = _upper_multiple([float(v) * 1.04 for v in list(cdd) + list(cwd)], 2.5)
        ax.set_ylim(0.0, teto)
        ax.yaxis.set_major_locator(MultipleLocator(2.5 if teto <= 30.0 else 5.0))
        ax.legend(fontsize=7.5, loc='lower right', bbox_to_anchor=(1.0, 1.0), ncol=2,
                  frameon=False, labelcolor=text_color)

        for spine in ax.spines.values():
            spine.set_color(grid_color)

        try:
            self.figure.tight_layout(pad=0.8)
        except Exception:
            pass
        self.safe_draw()


class SeasonalPrecipChart(TritonBaseChart):
    """Gráfico do Ciclo Sazonal Médio Mensal (Janeiro a Dezembro)."""
    def __init__(self, parent=None):
        super().__init__("Ciclo Sazonal Médio Mensal", parent, aspect_ratio=(32, 9), min_height=130)

    def plot_data(self, precip_data, start_date=None):
        if precip_data is None or len(precip_data) == 0:
            self.plot_empty(tr("Carregue uma série de precipitação para visualizar o gráfico"))
            return

        import pandas as pd
        from datetime import datetime
        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        bg_color = '#18181b' if is_dark else '#ffffff'
        text_color = '#f4f4f5' if is_dark else '#0f172a'
        grid_color = '#3f3f46' if is_dark else '#cbd5e1'

        start_dt = start_date if start_date else datetime(1980, 1, 1)
        dates = pd.date_range(start=start_dt, periods=len(precip_data), freq='D')
        df = pd.DataFrame({'precip': precip_data}, index=dates)

        monthly_totals = df.groupby([df.index.year, df.index.month])['precip'].sum()
        monthly_means = monthly_totals.groupby(level=1).mean()

        months_abbr = [tr("Jan"), tr("Fev"), tr("Mar"), tr("Abr"), tr("Mai"), tr("Jun"), 
                       tr("Jul"), tr("Ago"), tr("Set"), tr("Out"), tr("Nov"), tr("Dez")]
        vals = [monthly_means.get(m, 0.0) for m in range(1, 13)]

        self.figure.clear()
        self.figure.set_facecolor(bg_color)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(bg_color)

        bars = ax.bar(range(12), vals, color='#0284c7', alpha=0.85, width=0.6, edgecolor='#0369a1')

        for b, v in zip(bars, vals):
            yval = b.get_height()
            ax.text(b.get_x() + b.get_width()/2.0, yval + 1.0, f"{v:.0f}",
                    ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=text_color)

        ax.set_xticks(range(12))
        ax.set_xticklabels(months_abbr, fontsize=8, color=text_color)
        ax.set_ylabel(tr("Precipitação Média Mensal (mm)"), color=text_color, fontsize=8, fontweight='bold')
        ax.tick_params(colors=text_color, labelsize=7.5)
        ax.grid(True, axis='y', linestyle=':', alpha=0.6, color=grid_color)

        for spine in ax.spines.values():
            spine.set_color(grid_color)

        try:
            self.figure.tight_layout(pad=0.8)
        except Exception:
            pass
        self.safe_draw()


# Aliases para retrocompatibilidade
DailyWaterBalanceChart = TritonBaseChart
VolumeSweepChart = PotentialVsVolumeChart
LCAPaybackChart = CO2ComparisonChart
WaterAndCarbonComparisonChart = CO2ComparisonChart
