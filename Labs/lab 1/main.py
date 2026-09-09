import logging
import tkinter as tk
from tkinter import messagebox

from module1 import func_mod1
from module2 import func_mod2

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("Lab1.Main")


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing MainWindow.")
        self.title("Lab 1: Modular Application")
        self.geometry("600x400")

        self._display_text: str = "Select an action from the 'Actions' menu."

        self._init_menu()
        self._init_canvas()

    def _init_menu(self) -> None:
        logger.debug("Configuring main menu bar.")
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        actions_menu = tk.Menu(menubar, tearoff=0)
        actions_menu.add_command(label="Work 1", command=self._on_work1)
        actions_menu.add_command(label="Work 2", command=self._on_work2)
        menubar.add_cascade(label="Actions", menu=actions_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._on_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _init_canvas(self) -> None:
        logger.debug("Configuring canvas area.")
        self._canvas = tk.Canvas(self, bg="#FFFFFF")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Configure>", lambda _event: self._redraw())

    def _redraw(self) -> None:
        self._canvas.delete("all")
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        self._canvas.create_text(
            width // 2,
            height // 2,
            text=self._display_text,
            font=("Segoe UI", 14),
            fill="#111111",
            justify=tk.CENTER,
        )

    def _on_work1(self) -> None:
        logger.info("Action dispatched: Work 1.")
        value = func_mod1(self)
        if value is not None:
            logger.info("Work 1 returned value: %d. Redrawing canvas.", value)
            self._display_text = f"Result of Work 1 (Slider):\n\n{value}"
            self._redraw()
        else:
            logger.info("Work 1 dismissed without result.")

    def _on_work2(self) -> None:
        logger.info("Action dispatched: Work 2.")
        text = func_mod2(self)
        if text is not None:
            logger.info("Work 2 returned text: '%s'. Redrawing canvas.", text)
            self._display_text = f'Result of Work 2 (Text):\n\n"{text}"'
            self._redraw()
        else:
            logger.info("Work 2 dismissed without result.")

    def _on_about(self) -> None:
        logger.info("Help dispatched: About dialog.")
        messagebox.showinfo(
            "About",
            "Laboratory Work #1\nObject-Oriented Programming\nModular GUI Implementation",
        )


def main() -> None:
    logger.info("Starting main loop.")
    app = MainWindow()
    app.mainloop()
    logger.info("Main loop terminated.")


if __name__ == "__main__":
    main()
