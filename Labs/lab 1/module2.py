import logging
import tkinter as tk
from tkinter import ttk

__all__ = ["func_mod2"]

logger = logging.getLogger("Lab1.Module2")


class _TextDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        logger.info("Initializing TextDialog.")
        self.title("Work 2: Text Entry Dialog")
        self.geometry("340x160")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._result: str | None = None
        self._text_var: tk.StringVar = tk.StringVar()

        self._build_ui()

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.wait_window(self)

    def _build_ui(self) -> None:
        lbl = ttk.Label(self, text="Enter text:")
        lbl.pack(anchor=tk.W, padx=25, pady=(15, 5))

        self._entry = ttk.Entry(self, textvariable=self._text_var, width=35)
        self._entry.pack(fill=tk.X, padx=25, pady=5)
        self._entry.focus_set()

        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, pady=15)

        btn_ok = ttk.Button(btn_frame, text="OK", command=self._on_ok)
        btn_ok.pack(side=tk.LEFT, padx=10)

        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self._on_cancel)
        btn_cancel.pack(side=tk.LEFT, padx=10)

    def _on_ok(self) -> None:
        entered = self._text_var.get().strip()
        self._result = entered if entered else "(empty)"
        logger.info("TextDialog confirmed with text: '%s'", self._result)
        self.destroy()

    def _on_cancel(self) -> None:
        self._result = None
        logger.info("TextDialog cancelled.")
        self.destroy()

    @property
    def result(self) -> str | None:
        return self._result


def func_mod2(parent: tk.Tk) -> str | None:
    logger.info("func_mod2 invoked.")
    dialog = _TextDialog(parent)
    return dialog.result
