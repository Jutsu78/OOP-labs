import logging
import tkinter as tk
from collections.abc import Callable

from editor import (
    CubeEditor,
    EllipseEditor,
    LineCirclesEditor,
    LineEditor,
    PointEditor,
    RectEditor,
    ShapeEditor,
)
from shape import Shape

__all__ = ["MyEditor", "ShapeObjectsEditor"]

logger = logging.getLogger("Lab4.MyEditor")


class MyEditor:
    MAX_CAPACITY = 115

    def __init__(
        self,
        canvas: tk.Canvas,
        on_mode_change: Callable[[str, str], None] | None = None,
    ) -> None:
        logger.info("Initializing MyEditor instance (dynamic lifecycle).")
        self.canvas = canvas
        self._on_mode_change = on_mode_change
        self._pcshape: list[Shape] = []

        self._editors: dict[str, ShapeEditor] = {
            "point": PointEditor(self),
            "line": LineEditor(self),
            "rect": RectEditor(self),
            "ellipse": EllipseEditor(self),
            "line_circles": LineCirclesEditor(self),
            "cube": CubeEditor(self),
        }
        self._shape_labels: dict[str, str] = {
            "point": "Крапка",
            "line": "Лінія",
            "rect": "Прямокутник",
            "ellipse": "Еліпс",
            "line_circles": "Лінія з кружечками",
            "cube": "Каркас куба",
        }

        self._current_type_name: str = "point"
        self._current_editor: ShapeEditor = self._editors[self._current_type_name]

    @property
    def current_type_name(self) -> str:
        return self._current_type_name

    @property
    def current_label(self) -> str:
        return self._shape_labels.get(self._current_type_name, "")

    def start_editor(self, shape_type: str) -> None:
        if shape_type in self._editors:
            logger.info("Switching mode to %s.", shape_type)
            self._current_editor = self._editors[shape_type]
            self._current_type_name = shape_type
            if self._on_mode_change is not None:
                self._on_mode_change(shape_type, self.current_label)
        else:
            logger.error("Unknown editor type requested: '%s'.", shape_type)

    def on_lb_down(self, event: tk.Event) -> None:
        self._current_editor.on_lb_down(event)

    def on_lb_up(self, event: tk.Event) -> None:
        self._current_editor.on_lb_up(event)

    def on_mouse_move(self, event: tk.Event) -> None:
        self._current_editor.on_mouse_move(event)

    def on_paint(self) -> None:
        self.canvas.delete("shape")
        for shape in self._pcshape:
            shape.show(self.canvas)

    def add_shape(self, shape: Shape) -> None:
        if len(self._pcshape) < self.MAX_CAPACITY:
            self._pcshape.append(shape)
            logger.info(
                "Shape added to dynamic array. Current size: %d/%d.",
                len(self._pcshape),
                self.MAX_CAPACITY,
            )
            self.on_paint()
        else:
            logger.warning("Dynamic array capacity reached (%d).", self.MAX_CAPACITY)

    def on_init_menu_popup(self, menu_var: tk.StringVar) -> None:
        menu_var.set(self._current_type_name)
        logger.debug("Menu state synced: current mode '%s'.", self._current_type_name)

    def destroy(self) -> None:
        logger.info("Destroying MyEditor: cleaning shapes and references.")
        self.canvas.delete("all")
        self._pcshape.clear()
        self._editors.clear()


ShapeObjectsEditor = MyEditor
