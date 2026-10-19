import logging
import tkinter as tk
from tkinter import messagebox

from shape_objects_editor import ShapeObjectsEditor
from toolbar import Toolbar

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("Lab3.Main")


class MainWindow(tk.Tk):
    BASE_TITLE = "OOP_lab3"

    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing MainWindow.")
        self.title(self.BASE_TITLE)
        self.geometry("720x540")

        self._menu_shape_var = tk.StringVar(value="point")

        self._init_toolbar()
        self._init_canvas()
        self._editor = ShapeObjectsEditor(
            self._canvas,
            on_mode_change=self._on_editor_mode_changed,
        )
        self._init_menu()
        self._bind_events()

        self._editor.start_editor("point")

    def _init_toolbar(self) -> None:
        logger.debug("Configuring Toolbar.")
        self._toolbar = Toolbar(
            self,
            on_select_tool=lambda shape_type: self._editor.start_editor(shape_type),
        )
        self._toolbar.pack(side=tk.TOP, fill=tk.X)

    def _init_canvas(self) -> None:
        self._canvas = tk.Canvas(self, bg="#FFFFFF", cursor="crosshair")
        self._canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _init_menu(self) -> None:
        logger.debug("Configuring menu bar.")
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Вихід", command=self.destroy)
        menubar.add_cascade(label="Файл", menu=file_menu)

        objects_menu = tk.Menu(
            menubar,
            tearoff=0,
            postcommand=lambda: self._editor.on_init_menu_popup(self._menu_shape_var),
        )
        objects_menu.add_radiobutton(
            label="Крапка",
            variable=self._menu_shape_var,
            value="point",
            command=lambda: self._editor.start_editor("point"),
        )
        objects_menu.add_radiobutton(
            label="Лінія",
            variable=self._menu_shape_var,
            value="line",
            command=lambda: self._editor.start_editor("line"),
        )
        objects_menu.add_radiobutton(
            label="Прямокутник",
            variable=self._menu_shape_var,
            value="rect",
            command=lambda: self._editor.start_editor("rect"),
        )
        objects_menu.add_radiobutton(
            label="Еліпс",
            variable=self._menu_shape_var,
            value="ellipse",
            command=lambda: self._editor.start_editor("ellipse"),
        )
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self._on_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.config(menu=menubar)

    def _on_editor_mode_changed(self, shape_type: str, label_ukr: str) -> None:
        self.title(f"{self.BASE_TITLE} - Об'єкт: {label_ukr}")
        self._menu_shape_var.set(shape_type)
        self._toolbar.set_active_button(shape_type)

    def _bind_events(self) -> None:
        self._canvas.bind("<Button-1>", self._editor.on_lb_down)
        self._canvas.bind("<B1-Motion>", self._editor.on_mouse_move)
        self._canvas.bind("<ButtonRelease-1>", self._editor.on_lb_up)
        self._canvas.bind("<Configure>", lambda _event: self._editor.on_paint())

    def _on_about(self) -> None:
        logger.info("Displaying About dialog.")
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №3\nРозробка інтерфейсу користувача\nВаріант 14 (Ж = 15, N = 115)",
        )


def main() -> None:
    logger.info("Starting application loop.")
    app = MainWindow()
    app.mainloop()
    logger.info("Application loop ended.")


if __name__ == "__main__":
    main()
