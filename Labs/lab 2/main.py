import logging
import tkinter as tk
from tkinter import messagebox

from shape_objects_editor import ShapeObjectsEditor

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("Lab2.Main")


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing MainWindow.")
        self.title("OOP_lab2")
        self.geometry("700x500")

        self._menu_shape_var = tk.StringVar(value="point")

        self._init_canvas()
        self._editor = ShapeObjectsEditor(self._canvas)
        self._init_menu()
        self._bind_events()

    def _init_canvas(self) -> None:
        self._canvas = tk.Canvas(self, bg="#FFFFFF", cursor="crosshair")
        self._canvas.pack(fill=tk.BOTH, expand=True)

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

    def _bind_events(self) -> None:
        self._canvas.bind("<Button-1>", self._editor.on_lb_down)
        self._canvas.bind("<B1-Motion>", self._editor.on_mouse_move)
        self._canvas.bind("<ButtonRelease-1>", self._editor.on_lb_up)
        self._canvas.bind("<Configure>", lambda _event: self._editor.on_paint())

    def _on_about(self) -> None:
        logger.info("Displaying About dialog.")
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №2\nГрафічний редактор об'єктів\nВаріант 14 (N=114)",
        )


def main() -> None:
    logger.info("Starting application loop.")
    app = MainWindow()
    app.mainloop()
    logger.info("Application loop ended.")


if __name__ == "__main__":
    main()
