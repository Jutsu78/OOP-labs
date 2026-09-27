import tkinter as tk
from abc import ABC, abstractmethod

__all__ = ["EllipseShape", "LineShape", "PointShape", "RectShape", "Shape"]


class Shape(ABC):
    def __init__(self) -> None:
        self.xs1: int = 0
        self.ys1: int = 0
        self.xs2: int = 0
        self.ys2: int = 0

    def set(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.xs1 = x1
        self.ys1 = y1
        self.xs2 = x2
        self.ys2 = y2

    @abstractmethod
    def show(self, canvas: tk.Canvas) -> None:
        pass


class PointShape(Shape):
    def show(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(
            self.xs1 - 1,
            self.ys1 - 1,
            self.xs1 + 1,
            self.ys1 + 1,
            fill="black",
            outline="black",
            tags="shape",
        )


class LineShape(Shape):
    def show(self, canvas: tk.Canvas) -> None:
        canvas.create_line(
            self.xs1,
            self.ys1,
            self.xs2,
            self.ys2,
            fill="black",
            width=1,
            tags="shape",
        )


class RectShape(Shape):
    def show(self, canvas: tk.Canvas) -> None:
        x_min = min(self.xs1, self.xs2)
        y_min = min(self.ys1, self.ys2)
        x_max = max(self.xs1, self.xs2)
        y_max = max(self.ys1, self.ys2)
        canvas.create_rectangle(
            x_min,
            y_min,
            x_max,
            y_max,
            fill="",
            outline="black",
            width=1,
            tags="shape",
        )


class EllipseShape(Shape):
    def show(self, canvas: tk.Canvas) -> None:
        x_min = min(self.xs1, self.xs2)
        y_min = min(self.ys1, self.ys2)
        x_max = max(self.xs1, self.xs2)
        y_max = max(self.ys1, self.ys2)
        canvas.create_oval(
            x_min,
            y_min,
            x_max,
            y_max,
            fill="#90EE90",
            outline="black",
            width=1,
            tags="shape",
        )
