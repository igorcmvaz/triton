"""Visualizador 3D girável da volumetria, desenhado só com QPainter.

Não usa OpenGL de propósito: o Triton roda em máquinas de escritório, em
máquinas virtuais e por acesso remoto, onde drivers 3D falham com frequência.
As cenas têm centenas de faces, e o algoritmo do pintor (faces ordenadas da mais
distante para a mais próxima) resolve bem esse tamanho com a pilha 2D do Qt.

Interação: arrastar gira; botão direito, do meio ou Shift + arrastar desloca;
roda aproxima; clique seleciona uma peça e emite ``picked`` com a ficha dela.
Teclado: 1–4 escolhem a vista, F ou Home enquadram, Esc limpa a seleção.

Desempenho: todos os vértices são projetados de uma vez (numpy), as faces de
costas e as menores que um pixel são descartadas, e tubos mais finos que
``_LOD_PIXELS`` na tela viram linhas, idênticas à vista e muito mais baratas.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

import numpy as np
from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget

from triton.core.volumetry import Scene, Solid, face_normal
from triton.core.volumetry_export import feature_edges
from triton.ui.translation import tr

_LIGHTS = (
    (np.array([0.4, 0.3, 0.85]) / np.linalg.norm([0.4, 0.3, 0.85]), 0.45),
    (np.array([-0.6, -0.5, 0.2]) / np.linalg.norm([-0.6, -0.5, 0.2]), 0.18),
)
_HIGHLIGHT = (245, 158, 11)
_DOUBLE_SIDED = {"building", "slab", "ground"}
# Abaixo desta espessura na tela, o prisma do tubo é desenhado como linha.
_LOD_PIXELS = 6.0
_FOV_HALF_TAN = math.tan(0.35)
VIEWS = {
    "persp": (-0.75, 0.55, False),
    "top": (-math.pi / 2, math.pi / 2 - 1e-4, True),
    "front": (-math.pi / 2, 0.0, True),
    "side": (0.0, 0.0, True),
}


class _Face:
    __slots__ = ("solid", "points", "normal", "center", "edges", "shade")

    def __init__(self, solid: int, points: np.ndarray, normal: np.ndarray, edges: List[Tuple[int, int]]):
        self.solid = solid
        self.points = points
        self.normal = normal
        self.center = points.mean(axis=0)
        self.edges = edges
        # Iluminação fixa no mundo: calculada uma vez, não a cada quadro.
        self.shade = 0.42 + sum(w * max(float(normal @ d), 0.0) for d, w in _LIGHTS)


class VolumetryView(QWidget):
    picked = Signal(object)  # Solid ou None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 240)
        self.setMouseTracking(False)
        self.setFocusPolicy(Qt.StrongFocus)
        self.scene: Optional[Scene] = None
        self._faces: List[_Face] = []
        self.show_building = True
        self.show_ground = True
        self.show_labels = True
        self.selected: Optional[Solid] = None
        self._drag = None
        self.reset_view()

    # ── Cena e câmera ──

    def set_scene(self, scene: Optional[Scene]) -> None:
        """Achata a cena em arrays: cada quadro projeta todos os vértices de uma vez."""
        self.scene = scene
        self._faces = []
        if scene is not None:
            for index, solid in enumerate(scene.solids):
                edges_by_face = feature_edges(solid) if solid.outline else [[] for _ in solid.faces]
                for face, edges in zip(solid.faces, edges_by_face):
                    pts = np.array(face, dtype=float)
                    lookup = {tuple(np.round(p, 3)): i for i, p in enumerate(pts)}
                    pairs = [(lookup[tuple(np.round(a, 3))], lookup[tuple(np.round(b, 3))]) for a, b in edges]
                    self._faces.append(_Face(index, pts, np.array(face_normal(face)), pairs))
        faces = self._faces
        if faces:
            counts = np.array([len(f.points) for f in faces])
            self._starts = np.concatenate([[0], np.cumsum(counts)[:-1]])
            self._counts = counts
            self._vertices = np.vstack([f.points for f in faces])
            self._normals = np.array([f.normal for f in faces])
            self._centers = np.array([f.center for f in faces])
            self._face_solid = np.array([f.solid for f in faces])
            kinds = [scene.solids[f.solid].kind for f in faces]
            self._double = np.array([k in _DOUBLE_SIDED for k in kinds])
            self._kind_mask = {k: np.array([kk == k for kk in kinds]) for k in ("building", "slab", "ground")}
            self._colors = [self._face_color(scene.solids[f.solid], f, False) for f in faces]
            # Tubos (e nós) que podem virar linha: um registro por sólido.
            tubes = [i for i, solid in enumerate(scene.solids) if solid.axis is not None]
            self._tube_solids = np.array(tubes, dtype=int)
            self._tube_axes = np.array([[*scene.solids[i].axis[0], *scene.solids[i].axis[1]] for i in tubes]).reshape(-1, 6)
            self._tube_radius = np.array([scene.solids[i].axis[2] for i in tubes])
        if self.selected is not None and scene is not None:
            self.selected = next((s for s in scene.solids if s.key == self.selected.key), None)
        else:
            self.selected = None
        self.reset_view(keep_angles=True)

    @staticmethod
    def _face_color(solid: Solid, face: "_Face", highlighted: bool) -> QColor:
        base = _HIGHLIGHT if highlighted else solid.color
        shade = 1.0 if solid.kind in {"ground", "slab"} else face.shade
        alpha = solid.opacity
        if highlighted:
            alpha = 0.3 if solid.kind == "building" else max(alpha, 0.9)
        color = QColor(*(min(255, int(c * shade)) for c in base))
        color.setAlphaF(alpha)
        return color

    def reset_view(self, view: str = "persp", keep_angles: bool = False) -> None:
        if not keep_angles or not hasattr(self, "yaw"):
            self.yaw, self.pitch, self.ortho = VIEWS[view]
        center = np.array(self.scene.center if self.scene else (0.0, 0.0, 0.0))
        self.radius = self.scene.diagonal if self.scene else 1000.0
        self.target = center
        self.dist = self.radius * 1.35
        self._auto_fit = True
        self.fit()
        self.update()

    def fit(self, fill: float = 0.82) -> None:
        """Aproxima até a cena ocupar ``fill`` da área, pelas extensões projetadas."""
        if not self._faces or self.width() < 50 or self.height() < 50:
            return
        keep = ~self._kind_mask["ground"]
        if not self.show_building:
            keep &= ~(self._kind_mask["building"] | self._kind_mask["slab"])
        points = self._centers[keep] if keep.any() else self._centers
        points = np.vstack([self._faces[i].points for i in np.nonzero(keep)[0]]) if keep.any() else points
        for _ in range(4):
            project, *_ = self._projector()
            sx, sy, _ = project(points)
            ratio = max((sx.max() - sx.min()) / self.width(), (sy.max() - sy.min()) / self.height())
            if ratio <= 0:
                return
            self.dist = max(self.radius * 0.05, min(self.radius * 8, self.dist * ratio / fill))
            # Recentra: o ponto médio projetado vai para o centro da tela.
            project, *_ = self._projector()
            sx, sy, _ = project(points)
            _, _, right, up = self._basis()
            k = self.dist / self.height() * (0.9 if self.ortho else 0.7)
            dx, dy = (sx.max() + sx.min()) / 2 - self.width() / 2, (sy.max() + sy.min()) / 2 - self.height() / 2
            self.target = self.target + (dx * right - dy * up) * k

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if getattr(self, "_auto_fit", False):
            self.fit()

    def set_view(self, view: str) -> None:
        self.yaw, self.pitch, self.ortho = VIEWS[view]
        self.reset_view(view, keep_angles=True)

    def _basis(self):
        c = math.cos(self.pitch)
        eye = self.target + self.dist * np.array([c * math.cos(self.yaw), c * math.sin(self.yaw), math.sin(self.pitch)])
        forward = self.target - eye
        forward /= np.linalg.norm(forward)
        up = np.array([0.0, 0.0, 1.0])
        if abs(forward @ up) > 0.999:
            # Vista de cima: o "à frente" horizontal passa a ser o alto da tela.
            up = np.array([-math.cos(self.yaw), -math.sin(self.yaw), 0.0])
        right = np.cross(forward, up)
        right /= np.linalg.norm(right)
        return eye, forward, right, np.cross(right, forward)

    def _projector(self):
        eye, forward, right, up = self._basis()
        w, h = max(self.width(), 1), max(self.height(), 1)
        near = self.dist / 200

        def project(points: np.ndarray):
            rel = points - eye
            x, y, depth = rel @ right, rel @ up, rel @ forward
            if self.ortho:
                half = self.dist * 0.45
                scale = (h / 2) / half
                sx, sy = w / 2 + x * scale, h / 2 - y * scale
            else:
                safe = np.maximum(depth, near)
                scale = (h / 2) / (_FOV_HALF_TAN * safe)
                sx, sy = w / 2 + x * scale, h / 2 - y * scale
            return sx, sy, depth

        return project, eye, forward, near

    def _visible(self, solid: Solid) -> bool:
        if solid.kind in {"building", "slab"} and not self.show_building:
            return False
        return not (solid.kind == "ground" and not self.show_ground)

    # ── Desenho ──

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        # Girando, a fluidez vale mais que o antisserrilhado; ao soltar, redesenha fino.
        smooth = not (self._drag and self._drag["moved"])
        painter.setRenderHint(QPainter.Antialiasing, smooth)
        painter.fillRect(self.rect(), QColor("#f8fafc"))
        self._drawn = []
        if not self.scene or not self._faces:
            painter.setPen(QColor("#64748b"))
            painter.drawText(self.rect(), Qt.AlignCenter, tr("A volumetria aparece quando a organização estiver válida."))
            return
        project, eye, forward, near = self._projector()
        sx, sy, depth = project(self._vertices)
        starts, counts = self._starts, self._counts
        mean_depth = np.add.reduceat(depth, starts) / counts
        in_front = np.maximum.reduceat(depth, starts) > near
        # Faces de costas só interessam nas cascas abertas (edificação, lajes,
        # terreno); nos demais, até translúcidos, só criariam listras.
        facing = self._normals @ forward if self.ortho else np.einsum("ij,ij->i", self._normals, self._centers - eye)
        width = np.maximum.reduceat(sx, starts) - np.minimum.reduceat(sx, starts)
        height = np.maximum.reduceat(sy, starts) - np.minimum.reduceat(sy, starts)
        mask = in_front & (self._double | (facing < 0)) & ((width * height > 0.25) | self._double)
        if not self.show_building:
            mask &= ~(self._kind_mask["building"] | self._kind_mask["slab"])
        if not self.show_ground:
            mask &= ~self._kind_mask["ground"]
        solids = self.scene.solids
        # Nível de detalhe: tubo fino na tela vira uma linha espessa, idêntica à vista.
        lines = []
        if len(self._tube_solids):
            ax, ay, ad = project(self._tube_axes[:, :3])
            bx, by, bd = project(self._tube_axes[:, 3:])
            mid = np.maximum((ad + bd) / 2, near)
            pixels = 2 * self._tube_radius * self._pixels_per_unit(mid)
            thin = pixels < _LOD_PIXELS
            if thin.any():
                thin_solids = self._tube_solids[thin]
                mask &= ~np.isin(self._face_solid, thin_solids)
                for k in np.nonzero(thin & (ad > near) & (bd > near))[0]:
                    if solids[self._tube_solids[k]].pickable:  # nós somem sob a ponta arredondada
                        lines.append((float(mid[k]), k, float(ax[k]), float(ay[k]), float(bx[k]), float(by[k]), float(pixels[k])))
        order = np.nonzero(mask)[0]
        items = [(float(mean_depth[i]), 0, int(i)) for i in order] + [(line[0], 1, n) for n, line in enumerate(lines)]
        items.sort(key=lambda item: -item[0])

        no_pen = QPen(Qt.NoPen)
        for _, is_line, index in items:
            if is_line:
                self._draw_tube_line(painter, lines[index])
                continue
            face = self._faces[index]
            solid = solids[face.solid]
            a, n = starts[index], counts[index]
            xs, ys = sx[a:a + n], sy[a:a + n]
            polygon = QPolygonF([QPointF(x, y) for x, y in zip(xs, ys)])
            highlighted = self._is_selected(solid)
            color = self._face_color(solid, face, True) if highlighted else self._colors[index]
            # Contorno fino da própria cor fecha as frestas de antisserrilhado entre faces opacas.
            opaque = color.alphaF() >= 1.0
            painter.setPen(QPen(color, 0.8) if opaque else no_pen)
            painter.setBrush(color)
            # Translúcidas sem antisserrilhado: senão a costura entre faces vizinhas
            # recebe transparência dobrada e o cilindro fica listrado.
            if not opaque:
                painter.setRenderHint(QPainter.Antialiasing, False)
            painter.drawPolygon(polygon)
            if not opaque:
                painter.setRenderHint(QPainter.Antialiasing, smooth)
            if face.edges:
                base = _HIGHLIGHT if highlighted else solid.color
                k = 0.45 if solid.kind in _DOUBLE_SIDED else 0.35
                edge = QColor(*(int(c * k) for c in base))
                edge.setAlphaF(0.35 if solid.kind == "slab" else 0.85)
                painter.setPen(QPen(edge, 1.0))
                for i, j in face.edges:
                    painter.drawLine(QPointF(xs[i], ys[i]), QPointF(xs[j], ys[j]))
            if solid.pickable:
                self._drawn.append((polygon, solid))
        if self.show_labels:
            self._draw_labels(painter, project, near)
        self._draw_axes(painter)

    def _pixels_per_unit(self, depth):
        h = max(self.height(), 1)
        if self.ortho:
            return np.full_like(depth, (h / 2) / (self.dist * 0.45))
        return (h / 2) / (_FOV_HALF_TAN * depth)

    def _draw_tube_line(self, painter: QPainter, line) -> None:
        _, k, x0, y0, x1, y1, pixels = line
        solid = self.scene.solids[self._tube_solids[k]]
        highlighted = self._is_selected(solid)
        color = QColor(*(_HIGHLIGHT if highlighted else solid.color))
        painter.setPen(QPen(color, max(1.2, pixels), Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(QPointF(x0, y0), QPointF(x1, y1))
        # Área de clique: faixa de pelo menos 8 px em volta da linha.
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / length * 4, dx / length * 4
        band = QPolygonF([QPointF(x0 + nx, y0 + ny), QPointF(x1 + nx, y1 + ny), QPointF(x1 - nx, y1 - ny), QPointF(x0 - nx, y0 - ny)])
        self._drawn.append((band, solid))

    def _is_selected(self, solid: Solid) -> bool:
        if self.selected is None:
            return False
        if self.selected.group:
            return solid.group == self.selected.group
        return solid.key == self.selected.key

    def _draw_labels(self, painter: QPainter, project, near: float) -> None:
        font = QFont("Segoe UI", 9)
        font.setBold(True)
        painter.setFont(font)
        for solid in self.scene.solids:
            if solid.label_at is None or not self._visible(solid):
                continue
            sx, sy, depth = project(np.array([solid.label_at]))
            if depth[0] <= near:
                continue
            x, y = float(sx[0]), float(sy[0])
            path = QPainterPath()
            path.addText(QPointF(x + 6, y - 6), font, solid.key)
            painter.setPen(QPen(QColor("#f8fafc"), 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#0f172a"))
            painter.drawPath(path)
            painter.drawEllipse(QPointF(x, y), 2.5, 2.5)

    def _draw_axes(self, painter: QPainter) -> None:
        """Rosa de eixos no canto: orienta a leitura depois de girar."""
        _, _, right, up = self._basis()
        origin = QPointF(46, self.height() - 40)
        for axis, name, color in (((1, 0, 0), "x", "#dc2626"), ((0, 1, 0), "y · N", "#16a34a"), ((0, 0, 1), "z", "#2563eb")):
            v = np.array(axis, dtype=float)
            tip = QPointF(origin.x() + 26 * float(v @ right), origin.y() - 26 * float(v @ up))
            painter.setPen(QPen(QColor(color), 2))
            painter.drawLine(origin, tip)
            painter.drawText(tip + QPointF(3, -3), name)

    # ── Interação ──

    def mousePressEvent(self, event) -> None:
        self._auto_fit = False
        pan = event.button() in (Qt.RightButton, Qt.MiddleButton) or bool(event.modifiers() & Qt.ShiftModifier)
        self._drag = {"pos": event.position(), "pan": pan, "moved": False}
        self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event) -> None:
        if not self._drag:
            return
        delta = event.position() - self._drag["pos"]
        if abs(delta.x()) + abs(delta.y()) > 2:
            self._drag["moved"] = True
        self._drag["pos"] = event.position()
        if self._drag["pan"]:
            _, _, right, up = self._basis()
            k = self.dist / max(self.height(), 1)
            self.target = self.target + (-delta.x() * right + delta.y() * up) * k
        else:
            self.yaw -= delta.x() * 0.008
            self.pitch = max(-1.55, min(math.pi / 2 - 1e-4, self.pitch + delta.y() * 0.008))
            self.ortho = False
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        self.unsetCursor()
        drag, self._drag = self._drag, None
        if drag and not drag["moved"]:
            self.select_at(event.position())
        else:
            self.update()  # redesenha com antisserrilhado

    def wheelEvent(self, event) -> None:
        self._auto_fit = False
        factor = math.exp(-event.angleDelta().y() * 0.0012)
        self.dist = max(self.radius * 0.05, min(self.radius * 8, self.dist * factor))
        self.update()

    def keyPressEvent(self, event) -> None:
        """1–4: vistas; F ou Home: enquadrar; Esc: limpar seleção."""
        views = {Qt.Key_1: "persp", Qt.Key_2: "top", Qt.Key_3: "front", Qt.Key_4: "side"}
        if event.key() in views:
            self.set_view(views[event.key()])
        elif event.key() in (Qt.Key_F, Qt.Key_Home):
            self.fit()
            self.update()
        elif event.key() == Qt.Key_F11:
            win = self.window()
            if win:
                if hasattr(win, "toggle_fullscreen"):
                    win.toggle_fullscreen()
                elif win.isFullScreen():
                    win.showMaximized()
                else:
                    win.showFullScreen()
            event.accept()
        elif event.key() == Qt.Key_Escape:
            win = self.window()
            if win and win.isFullScreen():
                if hasattr(win, "toggle_fullscreen"):
                    win.toggle_fullscreen()
                else:
                    win.showMaximized()
                event.accept()
                return
            if self.selected is not None:
                self.selected = None
                self.picked.emit(None)
                self.update()
                event.accept()
        else:
            super().keyPressEvent(event)

    def select_at(self, point: QPointF) -> Optional[Solid]:
        """Peça mais próxima sob o cursor; a edificação só se nada estiver dentro dela."""
        hit = None
        for polygon, solid in reversed(getattr(self, "_drawn", [])):
            if polygon.containsPoint(point, Qt.OddEvenFill):
                if solid.kind != "building":
                    hit = solid
                    break
                hit = hit or solid
        self.selected = hit
        self.picked.emit(hit)
        self.update()
        return hit


class VolumetryPanel(QWidget):
    """Visualizador com barra de vistas, camadas e ficha da peça selecionada."""

    def __init__(self, parent=None):
        super().__init__(parent)
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        left = QVBoxLayout()
        self.view = VolumetryView()
        left.addWidget(self.view, 1)
        bar = QHBoxLayout()
        for label, key in ((tr("Perspectiva"), "persp"), (tr("Planta"), "top"), (tr("Frente"), "front"), (tr("Lateral"), "side")):
            btn = QPushButton(label)
            btn.clicked.connect(lambda _=False, k=key: self.view.set_view(k))
            bar.addWidget(btn)
        bar.addSpacing(12)
        for label, attr in ((tr("Edificação"), "show_building"), (tr("Terreno"), "show_ground"), (tr("Rótulos"), "show_labels")):
            box = QCheckBox(label)
            box.setChecked(True)
            box.toggled.connect(lambda on, a=attr: (setattr(self.view, a, on), self.view.update()))
            bar.addWidget(box)
        bar.addSpacing(12)
        self.btn_fs = QPushButton(tr("⛶ Tela cheia"))
        self.btn_fs.setToolTip(tr("Alternar modo tela cheia (F11)"))
        self.btn_fs.clicked.connect(self._toggle_fullscreen)
        bar.addWidget(self.btn_fs)
        bar.addStretch()
        hint = QLabel(tr("Arraste: girar · Shift/botão direito: deslocar · roda: aproximar · 1–4: vistas · F: enquadrar · F11: tela cheia"))
        hint.setStyleSheet("color:#64748b; font-size:11px;")
        bar.addWidget(hint)
        left.addLayout(bar)
        root.addLayout(left, 1)
        self.scroll_info = QScrollArea()
        self.scroll_info.setWidgetResizable(True)
        self.scroll_info.setFixedWidth(340)
        self.scroll_info.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_info.setStyleSheet("QScrollArea { border: 1px solid #cbd5e1; border-radius: 8px; background: #ffffff; }")
        self.lbl_info = QLabel()
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.lbl_info.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_info.setStyleSheet("background: transparent; border: none; padding: 12px; font-size: 12px; color: #1e293b;")
        self.scroll_info.setWidget(self.lbl_info)
        root.addWidget(self.scroll_info)
        self.view.picked.connect(self._show_info)
        self._show_info(None)

    def set_scene(self, scene: Optional[Scene]) -> None:
        self.view.set_scene(scene)
        self._show_info(self.view.selected)

    def _show_info(self, solid: Optional[Solid]) -> None:
        from html import escape

        notes = self.view.scene.notes if self.view.scene else []
        foot = "".join(f"<div style='margin-top:10px; padding-top:8px; border-top:1px dashed #e2e8f0; color:#64748b; font-size:11px;'>ℹ️ {escape(n)}</div>" for n in notes)
        if solid is None:
            self.lbl_info.setText(
                f"<div style='color:#64748b; font-size:12px; line-height:1.5;'>"
                f"<b style='color:#334155; font-size:13px;'>{tr('Ficha Técnica do Objeto 3D')}</b><br><br>"
                f"{tr('Clique em qualquer componente (motobomba, filtro, descarte, cisterna, reservatório ou tubulação) para inspecionar todas as características hidráulicas e normativas.')}"
                f"</div>{foot}"
            )
            return

        icon_map = {
            "pump": ("⚙️", "#dc2626", "Bomba"),
            "tank": ("🛢️", "#0284c7", "Reservatório"),
            "filter": ("🌪️", "#475569", "Filtro"),
            "pipe": ("📏", "#0891b2", "Tubulação"),
            "building": ("🏢", "#475569", "Edificação"),
            "slab": ("🧱", "#64748b", "Laje"),
            "ground": ("🌱", "#16a34a", "Terreno"),
        }
        icon, badge_col, badge_txt = icon_map.get(solid.kind, ("💧", "#2563eb", solid.kind))
        if solid.kind == "tank" and "Descarte" in solid.title:
            icon, badge_col, badge_txt = "⏳", "#b45309", "First Flush"

        header_html = (
            f"<div style='border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 10px;'>"
            f"<span style='display:inline-block; font-size:10px; font-weight:700; background:{badge_col}; color:#ffffff; padding:2px 7px; border-radius:10px; text-transform:uppercase;'>{badge_txt}</span>"
            f"<h3 style='margin:6px 0 0; font-size:14px; font-weight:700; color:#0f172a;'>{icon} {escape(solid.title)}</h3>"
            f"</div>"
        )

        body_lines = []
        for line in solid.info:
            if line.startswith(" • "):
                body_lines.append(f"<div style='margin-left: 12px; margin-top: 2px; margin-bottom: 2px; color: #475569; font-size: 11.5px;'>• {escape(line[3:])}</div>")
            elif ": " in line:
                body_lines.append(f"<div style='margin-bottom: 5px; font-size: 12px; line-height: 1.4; color: #1e293b;'>{escape(line)}</div>")
            else:
                body_lines.append(f"<div style='margin-top: 6px; margin-bottom: 4px; color: #0f172a; font-weight: 600; font-size: 12px;'>{escape(line)}</div>")

        self.lbl_info.setText(header_html + "".join(body_lines) + foot)

    def _toggle_fullscreen(self) -> None:
        win = self.window()
        if win is None:
            return
        if hasattr(win, "toggle_fullscreen"):
            win.toggle_fullscreen()
        elif win.isFullScreen():
            win.showMaximized()
        else:
            win.showFullScreen()
        self._sync_fs_button()

    def _sync_fs_button(self) -> None:
        win = self.window()
        if win and win.isFullScreen():
            self.btn_fs.setText(tr("🗗 Minimizar"))
            self.btn_fs.setToolTip(tr("Sair da tela cheia (F11 ou Esc)"))
        else:
            self.btn_fs.setText(tr("⛶ Tela cheia"))
            self.btn_fs.setToolTip(tr("Alternar modo tela cheia (F11)"))
