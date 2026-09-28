import logging
import tkinter as tk

from editor import (
    EllipseEditor,
    LineEditor,
    PointEditor,
    RectEditor,
    ShapeEditor,
)
from shape import Shape

__all__ = ["ShapeObjectsEditor"]

logger = logging.getLogger("Lab2.ShapeObjectsEditor")


class ShapeObjectsEditor:
    ARRAY_CAPACITY = 114

    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas
        self._pcshape: list[Shape | None] = [None] * self.ARRAY_CAPACITY
        self._count: int = 0

        self._point_editor = PointEditor(self)
        self._line_editor = LineEditor(self)
        self._rect_editor = RectEditor(self)
        self._ellipse_editor = EllipseEditor(self)

        self._current_editor: ShapeEditor = self._point_editor
        self._current_type_name: str = "point"

    @property
    def current_type_name(self) -> str:
        return self._current_type_name

    def start_point_editor(self) -> None:
        logger.info("Switching mode to PointEditor.")
        self._current_editor = self._point_editor
        self._current_type_name = "point"

    def start_line_editor(self) -> None:
        logger.info("Switching mode to LineEditor.")
        self._current_editor = self._line_editor
        self._current_type_name = "line"

    def start_rect_editor(self) -> None:
        logger.info("Switching mode to RectEditor.")
        self._current_editor = self._rect_editor
        self._current_type_name = "rect"

    def start_ellipse_editor(self) -> None:
        logger.info("Switching mode to EllipseEditor.")
        self._current_editor = self._ellipse_editor
        self._current_type_name = "ellipse"

    def on_lb_down(self, event: tk.Event) -> None:
        self._current_editor.on_lb_down(event)

    def on_lb_up(self, event: tk.Event) -> None:
        self._current_editor.on_lb_up(event)

    def on_mouse_move(self, event: tk.Event) -> None:
        self._current_editor.on_mouse_move(event)

    def on_paint(self) -> None:
        self.canvas.delete("shape")
        for i in range(self._count):
            shape = self._pcshape[i]
            if shape is not None:
                shape.show(self.canvas)

    def add_shape(self, shape: Shape) -> None:
        if self._count < self.ARRAY_CAPACITY:
            self._pcshape[self._count] = shape
            self._count += 1
            logger.info(
                "Shape added. Current array size: %d/%d.",
                self._count,
                self.ARRAY_CAPACITY,
            )
            self.on_paint()
        else:
            logger.warning("Shape array capacity reached (%d).", self.ARRAY_CAPACITY)

    def on_init_menu_popup(self, menu_var: tk.StringVar) -> None:
        menu_var.set(self._current_type_name)
        logger.debug("Menu state synced: current mode '%s'.", self._current_type_name)
