import logging
import tkinter as tk
from tkinter import ttk

__all__ = ["func_mod3"]

logger = logging.getLogger("Lab1.Module3")


class _ListDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        logger.info("Initializing ListDialog window.")
        self.title("Select Faculty Group")
        self.geometry("320x280")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._result: str | None = None
        self._groups = ["IM-51", "IM-52", "IM-53", "IM-54", "IM-o51"]

        self._build_ui()

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.wait_window(self)

    def _build_ui(self) -> None:
        lbl = ttk.Label(self, text="Select student group from the list:")
        lbl.pack(anchor=tk.W, padx=20, pady=(15, 5))

        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        self._listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            font=("Segoe UI", 10),
        )
        scrollbar.config(command=self._listbox.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for group in self._groups:
            self._listbox.insert(tk.END, group)
        self._listbox.select_set(0)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, pady=15)

        btn_ok = ttk.Button(btn_frame, text="OK", command=self._on_ok)
        btn_ok.pack(side=tk.LEFT, padx=10)

        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self._on_cancel)
        btn_cancel.pack(side=tk.LEFT, padx=10)

    def _on_ok(self) -> None:
        selection = self._listbox.curselection()
        if selection:
            self._result = self._listbox.get(selection[0])
            logger.info("ListDialog confirmed selection: '%s'", self._result)
        else:
            self._result = None
            logger.info("ListDialog confirmed with no selection.")
        self.destroy()

    def _on_cancel(self) -> None:
        self._result = None
        logger.info("ListDialog cancelled by user.")
        self.destroy()

    @property
    def result(self) -> str | None:
        return self._result


def func_mod3(parent: tk.Tk) -> str | None:
    logger.info("func_mod3 invoked.")
    dialog = _ListDialog(parent)
    return dialog.result
