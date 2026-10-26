import logging
import tkinter as tk
from abc import ABC, abstractmethod
from typing import Any

from shape import (
    CubeShape,
    EllipseShape,
    LineCirclesShape,
    LineShape,
    PointShape,
    RectShape,
)

__all__ = [
    "CubeEditor",
    "Editor",
    "EllipseEditor",
    "LineCirclesEditor",
    "LineEditor",
    "PointEditor",
    "RectEditor",
    "ShapeEditor",
]

logger = logging.getLogger("Lab4.Editor")


class Editor(ABC):
    @abstractmethod
    def on_lb_down(self, event: tk.Event) -> None:
        pass

    @abstractmethod
    def on_lb_up(self, event: tk.Event) -> None:
        pass

    @abstractmethod
    def on_mouse_move(self, event: tk.Event) -> None:
        pass

    @abstractmethod
    def on_paint(self, canvas: tk.Canvas) -> None:
        pass


class ShapeEditor(Editor):
    def __init__(self, owner: Any) -> None:
        self._owner = owner
        self._x_start: int = 0
        self._y_start: int = 0
        self._x_end: int = 0
        self._y_end: int = 0
        self._is_drawing: bool = False

    def on_paint(self, canvas: tk.Canvas) -> None:
        pass

    def _clear_rubber_band(self) -> None:
        self._owner.canvas.delete("rubber_band")


class PointEditor(ShapeEditor):
    def on_lb_down(self, event: tk.Event) -> None:
        logger.debug("PointEditor mouse down at (%d, %d).", event.x, event.y)
        shape = PointShape()
        shape.set(event.x, event.y, event.x, event.y)
        self._owner.add_shape(shape)

    def on_lb_up(self, event: tk.Event) -> None:
        pass

    def on_mouse_move(self, event: tk.Event) -> None:
        pass


class LineEditor(ShapeEditor):
    def on_lb_down(self, event: tk.Event) -> None:
        logger.debug("LineEditor start drag at (%d, %d).", event.x, event.y)
        self._is_drawing = True
        self._x_start = event.x
        self._y_start = event.y
        self._x_end = event.x
        self._y_end = event.y

    def on_mouse_move(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        self._x_end = event.x
        self._y_end = event.y
        self._clear_rubber_band()
        self._owner.canvas.create_line(
            self._x_start,
            self._y_start,
            self._x_end,
            self._y_end,
            fill="black",
            dash=(4, 2),
            width=1,
            tags="rubber_band",
        )

    def on_lb_up(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        logger.debug("LineEditor end drag at (%d, %d).", event.x, event.y)
        self._is_drawing = False
        self._clear_rubber_band()
        shape = LineShape()
        shape.set(self._x_start, self._y_start, event.x, event.y)
        self._owner.add_shape(shape)


class RectEditor(ShapeEditor):
    def on_lb_down(self, event: tk.Event) -> None:
        logger.debug("RectEditor center placed at (%d, %d).", event.x, event.y)
        self._is_drawing = True
        self._x_start = event.x
        self._y_start = event.y
        self._x_end = event.x
        self._y_end = event.y

    def on_mouse_move(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        self._x_end = event.x
        self._y_end = event.y
        self._clear_rubber_band()
        radius_x = abs(self._x_end - self._x_start)
        radius_y = abs(self._y_end - self._y_start)
        self._owner.canvas.create_rectangle(
            self._x_start - radius_x,
            self._y_start - radius_y,
            self._x_start + radius_x,
            self._y_start + radius_y,
            fill="",
            outline="black",
            dash=(4, 2),
            width=1,
            tags="rubber_band",
        )

    def on_lb_up(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        logger.debug("RectEditor corner released at (%d, %d).", event.x, event.y)
        self._is_drawing = False
        self._clear_rubber_band()
        radius_x = abs(event.x - self._x_start)
        radius_y = abs(event.y - self._y_start)
        shape = RectShape()
        shape.set(
            self._x_start - radius_x,
            self._y_start - radius_y,
            self._x_start + radius_x,
            self._y_start + radius_y,
        )
        self._owner.add_shape(shape)


class EllipseEditor(ShapeEditor):
    def on_lb_down(self, event: tk.Event) -> None:
        logger.debug("EllipseEditor start drag at (%d, %d).", event.x, event.y)
        self._is_drawing = True
        self._x_start = event.x
        self._y_start = event.y
        self._x_end = event.x
        self._y_end = event.y

    def on_mouse_move(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        self._x_end = event.x
        self._y_end = event.y
        self._clear_rubber_band()
        x_min = min(self._x_start, self._x_end)
        y_min = min(self._y_start, self._y_end)
        x_max = max(self._x_start, self._x_end)
        y_max = max(self._y_start, self._y_end)
        self._owner.canvas.create_oval(
            x_min,
            y_min,
            x_max,
            y_max,
            fill="",
            outline="black",
            dash=(4, 2),
            width=1,
            tags="rubber_band",
        )

    def on_lb_up(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        logger.debug("EllipseEditor end drag at (%d, %d).", event.x, event.y)
        self._is_drawing = False
        self._clear_rubber_band()
        shape = EllipseShape()
        shape.set(self._x_start, self._y_start, event.x, event.y)
        self._owner.add_shape(shape)


class LineCirclesEditor(ShapeEditor):
    def on_lb_down(self, event: tk.Event) -> None:
        logger.debug("LineCirclesEditor start drag at (%d, %d).", event.x, event.y)
        self._is_drawing = True
        self._x_start = event.x
        self._y_start = event.y
        self._x_end = event.x
        self._y_end = event.y

    def on_mouse_move(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        self._x_end = event.x
        self._y_end = event.y
        self._clear_rubber_band()

        self._owner.canvas.create_line(
            self._x_start,
            self._y_start,
            self._x_end,
            self._y_end,
            fill="black",
            dash=(4, 2),
            width=1,
            tags="rubber_band",
        )

        radius = 5
        self._owner.canvas.create_oval(
            self._x_start - radius,
            self._y_start - radius,
            self._x_start + radius,
            self._y_start + radius,
            outline="black",
            dash=(4, 2),
            width=1,
            tags="rubber_band",
        )
        self._owner.canvas.create_oval(
            self._x_end - radius,
            self._y_end - radius,
            self._x_end + radius,
            self._y_end + radius,
            outline="black",
            dash=(4, 2),
            width=1,
            tags="rubber_band",
        )

    def on_lb_up(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        logger.debug("LineCirclesEditor end drag at (%d, %d).", event.x, event.y)
        self._is_drawing = False
        self._clear_rubber_band()
        shape = LineCirclesShape()
        shape.set(self._x_start, self._y_start, event.x, event.y)
        self._owner.add_shape(shape)


class CubeEditor(ShapeEditor):
    def on_lb_down(self, event: tk.Event) -> None:
        logger.debug("CubeEditor start drag at (%d, %d).", event.x, event.y)
        self._is_drawing = True
        self._x_start = event.x
        self._y_start = event.y
        self._x_end = event.x
        self._y_end = event.y

    def on_mouse_move(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        self._x_end = event.x
        self._y_end = event.y
        self._clear_rubber_band()

        x_min = min(self._x_start, self._x_end)
        y_min = min(self._y_start, self._y_end)
        x_max = max(self._x_start, self._x_end)
        y_max = max(self._y_start, self._y_end)
        dx = max((x_max - x_min) // 3, 5)
        dy = max((y_max - y_min) // 3, 5)

        self._owner.canvas.create_rectangle(
            x_min,
            y_min,
            x_max,
            y_max,
            outline="black",
            dash=(4, 2),
            width=1,
            tags="rubber_band",
        )

        self._owner.canvas.create_rectangle(
            x_min + dx,
            y_min - dy,
            x_max + dx,
            y_max - dy,
            outline="black",
            dash=(4, 2),
            width=1,
            tags="rubber_band",
        )

        for vx, vy in [
            (x_min, y_min),
            (x_max, y_min),
            (x_min, y_max),
            (x_max, y_max),
        ]:
            self._owner.canvas.create_line(
                vx,
                vy,
                vx + dx,
                vy - dy,
                fill="black",
                dash=(4, 2),
                width=1,
                tags="rubber_band",
            )

    def on_lb_up(self, event: tk.Event) -> None:
        if not self._is_drawing:
            return
        logger.debug("CubeEditor end drag at (%d, %d).", event.x, event.y)
        self._is_drawing = False
        self._clear_rubber_band()
        shape = CubeShape()
        shape.set(self._x_start, self._y_start, event.x, event.y)
        self._owner.add_shape(shape)
