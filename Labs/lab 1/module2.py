import logging
import tkinter as tk
from tkinter import ttk

__all__ = ["func_mod2"]

logger = logging.getLogger("Lab1.Module2")


class _SecondDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        logger.info("Initializing SecondDialog window (Step 2).")
        self.title("Step 2 of 2")
        self.geometry("360x160")
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
            text="Wizard Step 2:\nPress 'OK' to finish or '< Back' to return.",
            font=("Segoe UI", 10),
            justify=tk.CENTER,
        )
        lbl.pack(expand=True, padx=20, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, pady=15)

        btn_back = ttk.Button(btn_frame, text="< Back", command=self._on_back)
        btn_back.pack(side=tk.LEFT, padx=5)

        btn_ok = ttk.Button(btn_frame, text="OK", command=self._on_ok)
        btn_ok.pack(side=tk.LEFT, padx=5)

        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self._on_cancel)
        btn_cancel.pack(side=tk.LEFT, padx=5)

    def _on_back(self) -> None:
        logger.info("SecondDialog: navigating back to Step 1.")
        self._result = -1
        self.destroy()

    def _on_ok(self) -> None:
        logger.info("SecondDialog confirmed: completing wizard.")
        self._result = 1
        self.destroy()

    def _on_cancel(self) -> None:
        logger.info("SecondDialog cancelled by user.")
        self._result = 0
        self.destroy()

    @property
    def result(self) -> int:
        return self._result


def func_mod2(parent: tk.Tk) -> int:
    logger.info("func_mod2 invoked.")
    dialog = _SecondDialog(parent)
    return dialog.result
