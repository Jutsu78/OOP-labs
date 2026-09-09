import logging
import tkinter as tk
from tkinter import ttk

__all__ = ["func_mod1"]

logger = logging.getLogger("Lab1.Module1")


class _ScrollDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        logger.info("Initializing ScrollDialog.")
        self.title("Work 1: Slider Dialog")
        self.geometry("340x180")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._result: int | None = None
        self._current_value: tk.IntVar = tk.IntVar(value=50)

        self._build_ui()

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.wait_window(self)

    def _build_ui(self) -> None:
        self._label_display = ttk.Label(
            self,
            text=f"Current Value: {self._current_value.get()}",
            font=("Segoe UI", 11, "bold"),
        )
        self._label_display.pack(pady=(15, 5))

        self._slider = ttk.Scale(
            self,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._current_value,
            command=self._on_scroll,
        )
        self._slider.pack(fill=tk.X, padx=25, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, pady=15)

        btn_ok = ttk.Button(btn_frame, text="OK", command=self._on_ok)
        btn_ok.pack(side=tk.LEFT, padx=10)

        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self._on_cancel)
        btn_cancel.pack(side=tk.LEFT, padx=10)

    def _on_scroll(self, _event: str | None = None) -> None:
        val = round(self._current_value.get())
        self._label_display.config(text=f"Current Value: {val}")
        logger.debug("Slider position updated to: %d", val)

    def _on_ok(self) -> None:
        self._result = round(self._current_value.get())
        logger.info("ScrollDialog confirmed with value: %d", self._result)
        self.destroy()

    def _on_cancel(self) -> None:
        self._result = None
        logger.info("ScrollDialog cancelled.")
        self.destroy()

    @property
    def result(self) -> int | None:
        return self._result


def func_mod1(parent: tk.Tk) -> int | None:
    logger.info("func_mod1 invoked.")
    dialog = _ScrollDialog(parent)
    return dialog.result
