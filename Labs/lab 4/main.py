import logging
import tkinter as tk
from tkinter import messagebox

from my_editor import MyEditor
from toolbar import Toolbar

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("Lab4.Main")


class MainWindow(tk.Tk):
    BASE_TITLE = "OOP_lab4"

    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing MainWindow.")
        self.title(self.BASE_TITLE)
        self.geometry("780x560")

        self._menu_shape_var = tk.StringVar(value="point")

        self._init_toolbar()
        self._init_canvas()

        self._editor: MyEditor | None = None
        self._create_dynamic_editor()

        self._init_menu()
        self._bind_events()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        if self._editor is not None:
            self._editor.start_editor("point")

    def _create_dynamic_editor(self) -> None:
        logger.info("Dynamically allocating MyEditor instance.")
        self._editor = MyEditor(
            self._canvas,
            on_mode_change=self._on_editor_mode_changed,
        )

    def _destroy_dynamic_editor(self) -> None:
        if self._editor is not None:
            logger.info("Dynamically deallocating/destroying MyEditor instance.")
            self._editor.destroy()
            del self._editor
            self._editor = None

    def _init_toolbar(self) -> None:
        logger.debug("Configuring Toolbar.")
        self._toolbar = Toolbar(
            self,
            on_select_tool=lambda shape_type: (
                self._editor.start_editor(shape_type)
                if self._editor is not None
                else None
            ),
        )
        self._toolbar.pack(side=tk.TOP, fill=tk.X)

    def _init_canvas(self) -> None:
        self._canvas = tk.Canvas(self, bg="#FFFFFF", cursor="crosshair")
        self._canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _init_menu(self) -> None:
        logger.debug("Configuring menu bar.")
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Вихід", command=self._on_close)
        menubar.add_cascade(label="Файл", menu=file_menu)

        objects_menu = tk.Menu(
            menubar,
            tearoff=0,
            postcommand=lambda: (
                self._editor.on_init_menu_popup(self._menu_shape_var)
                if self._editor is not None
                else None
            ),
        )
        tools = [
            ("point", "Крапка"),
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
                command=lambda t=shape_type: (
                    self._editor.start_editor(t) if self._editor is not None else None
                ),
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
        self._canvas.bind(
            "<Button-1>",
            lambda e: self._editor.on_lb_down(e) if self._editor else None,
        )
        self._canvas.bind(
            "<B1-Motion>",
            lambda e: self._editor.on_mouse_move(e) if self._editor else None,
        )
        self._canvas.bind(
            "<ButtonRelease-1>",
            lambda e: self._editor.on_lb_up(e) if self._editor else None,
        )
        self._canvas.bind(
            "<Configure>",
            lambda _e: self._editor.on_paint() if self._editor else None,
        )

    def _on_about(self) -> None:
        logger.info("Displaying About dialog.")
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №4\nВдосконалення структури коду графічного редактора об'єктів\nВаріант 14 (Ж = 14, динамічний MyEditor)",
        )

    def _on_close(self) -> None:
        logger.info("Closing application window.")
        self._destroy_dynamic_editor()
        self.destroy()


def main() -> None:
    logger.info("Starting application loop.")
    app = MainWindow()
    app.mainloop()
    logger.info("Application loop ended.")


if __name__ == "__main__":
    main()
