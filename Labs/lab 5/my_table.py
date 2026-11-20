import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

__all__ = ["MyTable"]


class MyTable(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Widget,
        on_select: Callable[[int | None], None] | None = None,
        on_delete: Callable[[int], None] | None = None,
        on_save: Callable[[], None] | None = None,
        on_load: Callable[[], None] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(parent)
        self.title("Таблиця графічних об'єктів")
        self.geometry("560x360")

        self._on_select = on_select
        self._on_delete = on_delete
        self._on_save = on_save
        self._on_load = on_load
        self._on_close = on_close
        self._suppress_select = False

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._handle_close)

    def _build_ui(self) -> None:
        table_frame = ttk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=6)

        columns = ("name", "x1", "y1", "x2", "y2")
        self._tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        self._tree.heading("name", text="Назва")
        self._tree.heading("x1", text="x1")
        self._tree.heading("y1", text="y1")
        self._tree.heading("x2", text="x2")
        self._tree.heading("y2", text="y2")

        self._tree.column("name", width=180, anchor="w")
        self._tree.column("x1", width=80, anchor="center")
        self._tree.column("y1", width=80, anchor="center")
        self._tree.column("x2", width=80, anchor="center")
        self._tree.column("y2", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self._tree.yview,
        )
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._tree.bind("<<TreeviewSelect>>", self._handle_select)
        self._tree.bind("<Delete>", self._handle_delete_key)

        controls_frame = ttk.Frame(self)
        controls_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=6, pady=(0, 6))

        ttk.Button(
            controls_frame,
            text="Видалити об'єкт",
            command=self._handle_delete,
        ).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(
            controls_frame,
            text="Зберегти CSV",
            command=self._handle_save,
        ).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(
            controls_frame,
            text="Завантажити CSV",
            command=self._handle_load,
        ).pack(side=tk.LEFT)

    def set_rows(self, rows: list[tuple[str, int, int, int, int]]) -> None:
        self._suppress_select = True
        try:
            for item_id in self._tree.get_children():
                self._tree.delete(item_id)
            for row in rows:
                self._tree.insert("", tk.END, values=row)
        finally:
            self._suppress_select = False

    def add_row(self, name: str, x1: int, y1: int, x2: int, y2: int) -> None:
        self._tree.insert("", tk.END, values=(name, x1, y1, x2, y2))

    def clear(self) -> None:
        self.set_rows([])

    def _get_selected_index(self) -> int | None:
        selection = self._tree.selection()
        if not selection:
            return None
        children = self._tree.get_children()
        item_id = selection[0]
        if item_id in children:
            return children.index(item_id)
        return None

    def _handle_select(self, _event: tk.Event) -> None:
        if self._suppress_select:
            return
        if self._on_select is not None:
            self._on_select(self._get_selected_index())

    def _handle_delete(self) -> None:
        index = self._get_selected_index()
        if index is not None and self._on_delete is not None:
            self._on_delete(index)

    def _handle_delete_key(self, _event: tk.Event) -> None:
        self._handle_delete()

    def _handle_save(self) -> None:
        if self._on_save is not None:
            self._on_save()

    def _handle_load(self) -> None:
        if self._on_load is not None:
            self._on_load()

    def _handle_close(self) -> None:
        self.withdraw()
        if self._on_select is not None:
            self._on_select(None)
        if self._on_close is not None:
            self._on_close()
