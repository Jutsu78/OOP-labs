import logging
import tkinter as tk
from tkinter import ttk

__all__ = ["func_mod1"]

logger = logging.getLogger("Lab1.Module1")


class _FirstDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        logger.info("Initializing FirstDialog window (Step 1).")
        self.title("Step 1 of 2")
        self.geometry("340x160")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._result: int = 0
        self._build_ui()

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.wait_window(self)

    def _build_ui(self) -> None:
        lbl = ttk.Label(
            self,
            text="Wizard Step 1:\nPress 'Next >' to proceed to the next step.",
            font=("Segoe UI", 10),
            justify=tk.CENTER,
        )
        lbl.pack(expand=True, padx=20, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, pady=15)

        btn_next = ttk.Button(btn_frame, text="Next >", command=self._on_next)
        btn_next.pack(side=tk.LEFT, padx=10)

        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self._on_cancel)
        btn_cancel.pack(side=tk.LEFT, padx=10)

    def _on_next(self) -> None:
        logger.info("FirstDialog confirmed: proceeding to Step 2.")
        self._result = 1
        self.destroy()

    def _on_cancel(self) -> None:
        logger.info("FirstDialog cancelled by user.")
        self._result = 0
        self.destroy()

    @property
    def result(self) -> int:
        return self._result


def func_mod1(parent: tk.Tk) -> int:
    logger.info("func_mod1 invoked.")
    dialog = _FirstDialog(parent)
    return dialog.result
