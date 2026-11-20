from __future__ import annotations

import csv
import logging
import tkinter as tk
from collections.abc import Callable
from typing import ClassVar

from editor import (
    CubeEditor,
    EllipseEditor,
    LineCirclesEditor,
    LineEditor,
    PointEditor,
    RectEditor,
    ShapeEditor,
)
from shape import (
    CubeShape,
    EllipseShape,
    LineCirclesShape,
    LineShape,
    PointShape,
    RectShape,
    Shape,
)

__all__ = ["MyEditor"]

logger = logging.getLogger("Lab5.MyEditor")


class MyEditor:
    _instance: ClassVar[MyEditor | None] = None
    MAX_CAPACITY: ClassVar[int] = 115

    def __init__(self) -> None:
        if MyEditor._instance is not None:
            msg = "Use MyEditor.get_instance() to access the Singleton."
            raise RuntimeError(msg)

        self.canvas: tk.Canvas | None = None
        self._on_mode_change: Callable[[str, str], None] | None = None
        self._on_data_change: Callable[[], None] | None = None
        self._pcshape: list[Shape] = []
        self._selected_index: int | None = None

        self._editors: dict[str, ShapeEditor] = {
            "point": PointEditor(self),
            "line": LineEditor(self),
            "rect": RectEditor(self),
            "ellipse": EllipseEditor(self),
            "line_circles": LineCirclesEditor(self),
            "cube": CubeEditor(self),
        }
        self._shape_classes: dict[str, type[Shape]] = {
            cls.SHAPE_NAME: cls
            for cls in (
                PointShape,
                LineShape,
                RectShape,
                EllipseShape,
                LineCirclesShape,
                CubeShape,
            )
        }
        self._shape_labels: dict[str, str] = {
            "point": PointShape.SHAPE_NAME,
            "line": LineShape.SHAPE_NAME,
            "rect": RectShape.SHAPE_NAME,
            "ellipse": EllipseShape.SHAPE_NAME,
            "line_circles": LineCirclesShape.SHAPE_NAME,
            "cube": CubeShape.SHAPE_NAME,
        }

        self._current_type_name: str = "point"
        self._current_editor: ShapeEditor = self._editors[self._current_type_name]

    @classmethod
    def get_instance(cls) -> MyEditor:
        if cls._instance is None:
            logger.info("Allocating classic Singleton MyEditor instance.")
            cls._instance = cls()
        return cls._instance

    @classmethod
    def destroy_instance(cls) -> None:
        if cls._instance is not None:
            logger.info("Destroying classic Singleton MyEditor instance.")
            cls._instance._cleanup()
            cls._instance = None

    def configure(
        self,
        canvas: tk.Canvas,
        on_mode_change: Callable[[str, str], None] | None = None,
        on_data_change: Callable[[], None] | None = None,
    ) -> None:
        self.canvas = canvas
        self._on_mode_change = on_mode_change
        self._on_data_change = on_data_change

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
        if self.canvas is None:
            return
        self.canvas.delete("shape")
        for index, shape in enumerate(self._pcshape):
            shape.show(self.canvas, is_selected=(index == self._selected_index))

    def add_shape(self, shape: Shape) -> None:
        if len(self._pcshape) < self.MAX_CAPACITY:
            self._pcshape.append(shape)
            logger.info(
                "Shape added. Current size: %d/%d.",
                len(self._pcshape),
                self.MAX_CAPACITY,
            )
            self.on_paint()
            self._notify_data_changed()
        else:
            logger.warning("Dynamic array capacity reached (%d).", self.MAX_CAPACITY)

    def select_shape_at(self, index: int | None) -> None:
        if index is None or not (0 <= index < len(self._pcshape)):
            self._selected_index = None
        else:
            self._selected_index = index
        self.on_paint()

    def remove_shape_at(self, index: int) -> None:
        if 0 <= index < len(self._pcshape):
            self._pcshape.pop(index)
            if self._selected_index == index:
                self._selected_index = None
            elif self._selected_index is not None and self._selected_index > index:
                self._selected_index -= 1
            logger.info("Shape removed at index %d.", index)
            self.on_paint()
            self._notify_data_changed()

    def get_table_rows(self) -> list[tuple[str, int, int, int, int]]:
        return [
            (shape.SHAPE_NAME, shape.xs1, shape.ys1, shape.xs2, shape.ys2)
            for shape in self._pcshape
        ]

    def save_to_csv(self, file_path: str) -> None:
        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            for row in self.get_table_rows():
                writer.writerow(row)
        logger.info("Saved %d shapes to '%s'.", len(self._pcshape), file_path)

    def load_from_csv(self, file_path: str) -> None:
        loaded_shapes: list[Shape] = []
        with open(file_path, mode="r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 5:
                    continue
                shape_cls = self._shape_classes.get(row[0].strip())
                if shape_cls is None:
                    continue
                shape = shape_cls()
                shape.set(int(row[1]), int(row[2]), int(row[3]), int(row[4]))
                loaded_shapes.append(shape)
                if len(loaded_shapes) >= self.MAX_CAPACITY:
                    break
        self._pcshape = loaded_shapes
        self._selected_index = None
        logger.info("Loaded %d shapes from '%s'.", len(self._pcshape), file_path)
        self.on_paint()
        self._notify_data_changed()

    def on_init_menu_popup(self, menu_var: tk.StringVar) -> None:
        menu_var.set(self._current_type_name)

    def _notify_data_changed(self) -> None:
        if self._on_data_change is not None:
            self._on_data_change()

    def _cleanup(self) -> None:
        if self.canvas is not None:
            self.canvas.delete("all")
        self._pcshape.clear()
        self._editors.clear()
        self._selected_index = None
