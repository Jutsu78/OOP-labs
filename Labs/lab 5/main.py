import logging
import tkinter as tk
from functools import partial
from tkinter import filedialog, messagebox

from my_editor import MyEditor
from my_table import MyTable
from toolbar import Toolbar

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("Lab5.Main")


class MainWindow(tk.Tk):
    BASE_TITLE = "OOP_lab5"

    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing MainWindow.")
        self.title(self.BASE_TITLE)
        self.geometry("800x600")

        self._menu_shape_var = tk.StringVar(value="point")
        self._table_visible_var = tk.BooleanVar(value=False)
        self._table_window: MyTable | None = None

        self._init_toolbar()
        self._init_canvas()

        self._editor = MyEditor.get_instance()
        self._editor.configure(
            canvas=self._canvas,
            on_mode_change=self._on_editor_mode_changed,
            on_data_change=self._on_editor_data_changed,
        )

        self._init_menu()
        self._bind_events()

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._editor.start_editor("point")

    def _init_toolbar(self) -> None:
        self._toolbar = Toolbar(
            self,
            on_select_tool=lambda shape_type: self._editor.start_editor(shape_type),
        )
        self._toolbar.pack(side=tk.TOP, fill=tk.X)

    def _init_canvas(self) -> None:
        self._canvas = tk.Canvas(self, bg="#FFFFFF", cursor="crosshair")
        self._canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _init_menu(self) -> None:
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Зберегти у CSV...", command=self._on_save_csv)
        file_menu.add_command(label="Завантажити з CSV...", command=self._on_load_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self._on_close)
        menubar.add_cascade(label="Файл", menu=file_menu)

        objects_menu = tk.Menu(
            menubar,
            tearoff=0,
            postcommand=lambda: self._editor.on_init_menu_popup(self._menu_shape_var),
        )
        tools = [
            ("point", "Точка"),
            ("line", "Лінія"),
            ("rect", "Прямокутник"),
            ("ellipse", "Еліпс"),
            ("line_circles", "Лінія з кружечками"),
            ("cube", "Каркас куба"),
        ]
        for shape_type, label in tools:
            objects_menu.add_radiobutton(
                label=label,
                variable=self._menu_shape_var,
                value=shape_type,
                command=partial(self._editor.start_editor, shape_type),
            )
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)

        table_menu = tk.Menu(menubar, tearoff=0)
        table_menu.add_checkbutton(
            label="Таблиця об'єктів",
            variable=self._table_visible_var,
            command=self._toggle_table_window,
        )
        menubar.add_cascade(label="Таблиця", menu=table_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self._on_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.config(menu=menubar)

    def _toggle_table_window(self) -> None:
        if self._table_window is None or not self._table_window.winfo_exists():
            self._table_window = MyTable(
                self,
                on_select=self._editor.select_shape_at,
                on_delete=self._editor.remove_shape_at,
                on_save=self._on_save_csv,
                on_load=self._on_load_csv,
                on_close=self._on_table_closed,
            )
            self._table_window.set_rows(self._editor.get_table_rows())
            self._table_visible_var.set(True)
            return

        if self._table_visible_var.get():
            self._table_window.set_rows(self._editor.get_table_rows())
            self._table_window.deiconify()
            self._table_window.lift()
        else:
            self._table_window.withdraw()
            self._editor.select_shape_at(None)

    def _on_table_closed(self) -> None:
        self._table_visible_var.set(False)

    def _on_editor_mode_changed(self, shape_type: str, label_ukr: str) -> None:
        self.title(f"{self.BASE_TITLE} - Об'єкт: {label_ukr}")
        self._menu_shape_var.set(shape_type)
        self._toolbar.set_active_button(shape_type)

    def _on_editor_data_changed(self) -> None:
        if self._table_window is not None and self._table_window.winfo_exists():
            self._table_window.set_rows(self._editor.get_table_rows())

    def _on_save_csv(self) -> None:
        file_path = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not file_path:
            return
        try:
            self._editor.save_to_csv(file_path)
            messagebox.showinfo("Збереження", "Об'єкти успішно збережено у CSV.")
        except OSError as exc:
            messagebox.showerror("Помилка збереження", str(exc))

    def _on_load_csv(self) -> None:
        file_path = filedialog.askopenfilename(
            parent=self,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not file_path:
            return
        try:
            self._editor.load_from_csv(file_path)
            messagebox.showinfo("Завантаження", "Об'єкти успішно завантажено з CSV.")
        except (OSError, ValueError) as exc:
            messagebox.showerror("Помилка завантаження", str(exc))

    def _bind_events(self) -> None:
        self._canvas.bind("<Button-1>", self._editor.on_lb_down)
        self._canvas.bind("<B1-Motion>", self._editor.on_mouse_move)
        self._canvas.bind("<ButtonRelease-1>", self._editor.on_lb_up)
        self._canvas.bind("<Configure>", lambda _e: self._editor.on_paint())

    def _on_about(self) -> None:
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №5\n"
            "Багатовіконний інтерфейс користувача\n"
            "Варіант 14 (Класичний Singleton MyEditor + MyTable)",
        )

    def _on_close(self) -> None:
        logger.info("Closing application window.")
        if self._table_window is not None and self._table_window.winfo_exists():
            self._table_window.destroy()
        MyEditor.destroy_instance()
        self.destroy()


def main() -> None:
    logger.info("Starting application loop.")
    app = MainWindow()
    app.mainloop()
    logger.info("Application loop ended.")


if __name__ == "__main__":
    main()
