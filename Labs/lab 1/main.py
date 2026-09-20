import logging
import tkinter as tk
from tkinter import messagebox

from module1 import func_mod1
from module2 import func_mod2
from module3 import func_mod3

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
        self.title("Lab 1: Modular Application (Variant 14)")
        self.geometry("640x420")

        self._display_text: str = "Select an action from the 'Actions' menu."

        self._init_menu()
        self._init_canvas()

    def _init_menu(self) -> None:
        logger.debug("Building system menu bar.")
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
        logger.info("Action dispatched: Work 1 (Sequential Dialogs).")
        step = 1

        while True:
            if step == 1:
                res1 = func_mod1(self)
                if res1 == 1:
                    step = 2
                else:
                    logger.info("Work 1 terminated at Step 1.")
                    break
            elif step == 2:
                res2 = func_mod2(self)
                if res2 == -1:
                    step = 1
                elif res2 == 1:
                    logger.info("Work 1 successfully completed.")
                    self._display_text = (
                        "Result of Work 1:\n\nTwo-step wizard successfully completed."
                    )
                    self._redraw()
                    break
                else:
                    logger.info("Work 1 terminated at Step 2.")
                    break

    def _on_work2(self) -> None:
        logger.info("Action dispatched: Work 2 (ListBox Selection).")
        group = func_mod3(self)
        if group is not None:
            logger.info("Work 2 completed with group: '%s'.", group)
            self._display_text = f"Result of Work 2 (Selected Group):\n\n{group}"
            self._redraw()
        else:
            logger.info("Work 2 dismissed without selection.")

    def _on_about(self) -> None:
        logger.info("Help action triggered: About dialog.")
        messagebox.showinfo(
            "About",
            "Laboratory Work #1\nVariant 14 (B1=2, B2=3)\nModular GUI Architecture",
        )


def main() -> None:
    logger.info("Starting main application loop.")
    app = MainWindow()
    app.mainloop()
    logger.info("Application loop terminated.")


if __name__ == "__main__":
    main()
