import logging
import math
import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

__all__ = ["ToolTip", "Toolbar"]

logger = logging.getLogger("Lab4.Toolbar")


class ToolTip:
    def __init__(
        self,
        widget: tk.Widget,
        text: str,
        notify_callback: Callable[[str], None] | None = None,
    ) -> None:
        self._widget = widget
        self._text = text
        self._notify_callback = notify_callback
        self._tip_window: tk.Toplevel | None = None

        self._widget.bind("<Enter>", self.on_notify_enter)
        self._widget.bind("<Leave>", self.on_notify_leave)

    def on_notify_enter(self, _event: tk.Event) -> None:
        if self._notify_callback is not None:
            self._notify_callback(self._text)
        if self._tip_window is not None:
            return
        x = self._widget.winfo_rootx() + 10
        y = self._widget.winfo_rooty() + self._widget.winfo_height() + 4
        self._tip_window = tk.Toplevel(self._widget)
        self._tip_window.wm_overrideredirect(True)
        self._tip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self._tip_window,
            text=self._text,
            background="#FFFFE0",
            foreground="#000000",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", 9),
            padx=6,
            pady=2,
        )
        label.pack()

    def on_notify_leave(self, _event: tk.Event) -> None:
        if self._tip_window is not None:
            self._tip_window.destroy()
            self._tip_window = None


class Toolbar(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        on_select_tool: Callable[[str], None],
    ) -> None:
        super().__init__(parent, relief=tk.RAISED, borderwidth=1)
        self._on_select_tool = on_select_tool
        self._icons: dict[str, tk.PhotoImage] = {}
        self._buttons: dict[str, tk.Button] = {}
        self._tooltips: list[ToolTip] = []

        self._build_icons()
        self._build_buttons()

    def _build_icons(self) -> None:
        size = 24

        point_img = tk.PhotoImage(width=size, height=size)
        for y in range(size):
            for x in range(size):
                if (x - 12) ** 2 + (y - 12) ** 2 <= 9:
                    point_img.put("#000000", (x, y))
        self._icons["point"] = point_img

        line_img = tk.PhotoImage(width=size, height=size)
        for i in range(4, 20):
            line_img.put("#000000", (i, 23 - i))
            line_img.put("#000000", (i, 22 - i))
        self._icons["line"] = line_img

        rect_img = tk.PhotoImage(width=size, height=size)
        for y in range(5, 19):
            for x in range(4, 20):
                if x in (4, 19) or y in (5, 18):
                    rect_img.put("#000000", (x, y))
                else:
                    rect_img.put("#FFFFFF", (x, y))
        self._icons["rect"] = rect_img

        ellipse_img = tk.PhotoImage(width=size, height=size)
        rx, ry = 8.0, 5.5
        cx, cy = 12.0, 12.0
        for angle in range(360):
            rad = math.radians(angle)
            x = round(cx + rx * math.cos(rad))
            y = round(cy + ry * math.sin(rad))
            ellipse_img.put("#000000", (x, y))
        self._icons["ellipse"] = ellipse_img

        lc_img = tk.PhotoImage(width=size, height=size)
        for i in range(7, 17):
            lc_img.put("#000000", (i, 23 - i))
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx * dx + dy * dy <= 4:
                    lc_img.put("#000000", (6 + dx, 17 + dy))
                    lc_img.put("#000000", (17 + dx, 6 + dy))
        self._icons["line_circles"] = lc_img

        cube_img = tk.PhotoImage(width=size, height=size)

        for x in range(4, 16):
            cube_img.put("#000000", (x, 10))
            cube_img.put("#000000", (x, 20))
        for y in range(10, 21):
            cube_img.put("#000000", (4, y))
            cube_img.put("#000000", (15, y))

        for x in range(8, 20):
            cube_img.put("#000000", (x, 5))
            cube_img.put("#000000", (x, 15))
        for y in range(5, 16):
            cube_img.put("#000000", (8, y))
            cube_img.put("#000000", (19, y))
        for step in range(5):
            cube_img.put("#000000", (4 + step, 10 - step))
            cube_img.put("#000000", (15 + step, 10 - step))
            cube_img.put("#000000", (4 + step, 20 - step))
            cube_img.put("#000000", (15 + step, 20 - step))
        self._icons["cube"] = cube_img

    def _build_buttons(self) -> None:
        tools = [
            ("point", "Крапка"),
            ("line", "Лінія"),
            ("rect", "Прямокутник"),
            ("ellipse", "Еліпс"),
            ("line_circles", "Лінія з кружечками"),
            ("cube", "Каркас куба"),
        ]
        for shape_type, tooltip_text in tools:
            btn = tk.Button(
                self,
                image=self._icons[shape_type],
                width=28,
                height=28,
                relief=tk.RAISED,
                bd=1,
                command=lambda t=shape_type: self._on_button_pressed(t),
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self._buttons[shape_type] = btn
            self._tooltips.append(ToolTip(btn, tooltip_text, self.on_notify))

    def _on_button_pressed(self, shape_type: str) -> None:
        logger.info("Toolbar button clicked: '%s'.", shape_type)
        self._on_select_tool(shape_type)

    def on_notify(self, tooltip_text: str) -> None:
        logger.debug("OnNotify triggered: displaying tooltip '%s'.", tooltip_text)

    def set_active_button(self, shape_type: str) -> None:
        for key, btn in self._buttons.items():
            if key == shape_type:
                btn.config(relief=tk.SUNKEN, bg="#D0E0F0")
            else:
                btn.config(relief=tk.RAISED, bg="SystemButtonFace")
