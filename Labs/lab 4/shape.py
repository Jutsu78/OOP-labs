import tkinter as tk
from abc import ABC, abstractmethod

__all__ = [
    "CubeShape",
    "EllipseShape",
    "LineCirclesShape",
    "LineShape",
    "PointShape",
    "RectShape",
    "Shape",
]


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
    def __init__(self, fill_color: str = "white") -> None:
        super().__init__()
        self.fill_color = fill_color

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
            fill=self.fill_color,
            outline="black",
            width=1,
            tags="shape",
        )


class EllipseShape(Shape):
    def __init__(self, fill_color: str = "") -> None:
        super().__init__()
        self.fill_color = fill_color

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
            fill=self.fill_color,
            outline="black",
            width=1,
            tags="shape",
        )


class LineCirclesShape(LineShape, EllipseShape):
    def __init__(self) -> None:
        super().__init__()
        self.fill_color = "white"

    def show(self, canvas: tk.Canvas) -> None:
        orig_x1, orig_y1, orig_x2, orig_y2 = self.xs1, self.ys1, self.xs2, self.ys2

        LineShape.show(self, canvas)

        radius = 5
        EllipseShape.set(
            self,
            orig_x1 - radius,
            orig_y1 - radius,
            orig_x1 + radius,
            orig_y1 + radius,
        )
        EllipseShape.show(self, canvas)

        EllipseShape.set(
            self,
            orig_x2 - radius,
            orig_y2 - radius,
            orig_x2 + radius,
            orig_y2 + radius,
        )
        EllipseShape.show(self, canvas)

        self.set(orig_x1, orig_y1, orig_x2, orig_y2)


class CubeShape(RectShape, LineShape):
    def __init__(self) -> None:
        super().__init__()
        self.fill_color = ""

    def show(self, canvas: tk.Canvas) -> None:
        orig_x1, orig_y1, orig_x2, orig_y2 = self.xs1, self.ys1, self.xs2, self.ys2

        x_min = min(orig_x1, orig_x2)
        y_min = min(orig_y1, orig_y2)
        x_max = max(orig_x1, orig_x2)
        y_max = max(orig_y1, orig_y2)

        dx = max((x_max - x_min) // 3, 5)
        dy = max((y_max - y_min) // 3, 5)

        RectShape.set(self, x_min + dx, y_min - dy, x_max + dx, y_max - dy)
        RectShape.show(self, canvas)

        RectShape.set(self, x_min, y_min, x_max, y_max)
        RectShape.show(self, canvas)

        LineShape.set(self, x_min, y_min, x_min + dx, y_min - dy)
        LineShape.show(self, canvas)

        LineShape.set(self, x_max, y_min, x_max + dx, y_min - dy)
        LineShape.show(self, canvas)

        LineShape.set(self, x_min, y_max, x_min + dx, y_max - dy)
        LineShape.show(self, canvas)

        LineShape.set(self, x_max, y_max, x_max + dx, y_max - dy)
        LineShape.show(self, canvas)

        self.set(orig_x1, orig_y1, orig_x2, orig_y2)
