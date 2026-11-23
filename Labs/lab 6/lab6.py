import json
import socket
import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

OBJECT2_PORT = 50002
OBJECT3_PORT = 50003
BASE_DIR = Path(__file__).resolve().parent


class ParamsDialog(tk.Toplevel):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.title("Параметри вектора")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result: tuple[int, float, float] | None = None

        self._n_var = tk.StringVar(value="25")
        self._min_var = tk.StringVar(value="-50.0")
        self._max_var = tk.StringVar(value="50.0")

        self._build_ui()
        self.geometry(f"+{parent.winfo_rootx() + 40}+{parent.winfo_rooty() + 40}")
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Кількість елементів (n):").grid(
            row=0, column=0, sticky="w", pady=4
        )
        n_entry = ttk.Entry(frame, textvariable=self._n_var, width=18)
        n_entry.grid(row=0, column=1, padx=(10, 0), pady=4)
        n_entry.focus_set()

        ttk.Label(frame, text="Мінімум (Min):").grid(
            row=1, column=0, sticky="w", pady=4
        )
        ttk.Entry(frame, textvariable=self._min_var, width=18).grid(
            row=1, column=1, padx=(10, 0), pady=4
        )

        ttk.Label(frame, text="Максимум (Max):").grid(
            row=2, column=0, sticky="w", pady=4
        )
        ttk.Entry(frame, textvariable=self._max_var, width=18).grid(
            row=2, column=1, padx=(10, 0), pady=4
        )

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(12, 0))

        ttk.Button(btn_frame, text="Виконати", command=self._on_ok).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btn_frame, text="Скасувати", command=self._on_cancel).pack(
            side=tk.LEFT, padx=4
        )

        self.bind("<Return>", lambda _e: self._on_ok())
        self.bind("<Escape>", lambda _e: self._on_cancel())

    def _on_ok(self) -> None:
        try:
            n = int(self._n_var.get().strip())
            min_val = float(self._min_var.get().strip().replace(",", "."))
            max_val = float(self._max_var.get().strip().replace(",", "."))
        except ValueError:
            messagebox.showerror(
                "Помилка вводу",
                "Введіть коректні числові значення.",
                parent=self,
            )
            return

        if n <= 0:
            messagebox.showerror(
                "Помилка вводу",
                "Параметр n має бути більшим за 0.",
                parent=self,
            )
            return

        if min_val > max_val:
            messagebox.showerror(
                "Помилка вводу",
                "Значення Min не може перевищувати Max.",
                parent=self,
            )
            return

        self.result = (n, min_val, max_val)
        self.destroy()

    def _on_cancel(self) -> None:
        self.result = None
        self.destroy()


class Lab6App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Lab6 — Менеджер")
        self.geometry("320x220+20+40")
        self._spawned_processes: list[subprocess.Popen[bytes]] = []
        self._is_busy = False

        self._init_menu()
        self._init_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _init_menu(self) -> None:
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Вихід", command=self._on_close)
        menubar.add_cascade(label="Файл", menu=file_menu)

        work_menu = tk.Menu(menubar, tearoff=0)
        work_menu.add_command(label="Виконати завдання...", command=self._open_dialog)
        menubar.add_cascade(label="Робота", menu=work_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self._on_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.config(menu=menubar)

    def _init_ui(self) -> None:
        frame = ttk.Frame(self, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text="Лабораторна робота №6\nВаріант 2 (Ж = 14)",
            justify=tk.CENTER,
            font=("Segoe UI", 10, "bold"),
        ).pack(pady=(0, 10))

        self._status_var = tk.StringVar(
            value="Оберіть «Робота -> Виконати завдання...»"
        )
        ttk.Label(
            frame,
            textvariable=self._status_var,
            wraplength=280,
            justify=tk.CENTER,
        ).pack(pady=6)

    def _open_dialog(self) -> None:
        if self._is_busy:
            return
        dialog = ParamsDialog(self)
        self.wait_window(dialog)
        if dialog.result is None:
            return

        n, min_val, max_val = dialog.result
        self._is_busy = True
        self._status_var.set("Обмін повідомленнями з Object2 та Object3...")
        worker = threading.Thread(
            target=self._run_workflow,
            args=(n, min_val, max_val),
            daemon=True,
        )
        worker.start()

    def _run_workflow(self, n: int, min_val: float, max_val: float) -> None:
        try:
            resp2 = self._send_or_launch(
                OBJECT2_PORT,
                "object2.py",
                {"cmd": "generate", "n": n, "min": min_val, "max": max_val},
            )
            if resp2.get("status") != "ok":
                raise RuntimeError(resp2.get("error", "Помилка Object2"))

            resp3 = self._send_or_launch(
                OBJECT3_PORT,
                "object3.py",
                {"cmd": "process"},
            )
            if resp3.get("status") != "ok":
                raise RuntimeError(resp3.get("error", "Помилка Object3"))

            self.after(
                0,
                self._on_workflow_done,
                f"Виконано: n={n}, діапазон [{min_val}; {max_val}].",
                None,
            )
        except (OSError, RuntimeError) as exc:
            self.after(0, self._on_workflow_done, "Помилка виконання.", str(exc))

    def _on_workflow_done(self, status: str, error: str | None) -> None:
        self._is_busy = False
        self._status_var.set(status)
        self.lift()
        if error is not None:
            messagebox.showerror("Помилка взаємодії", error, parent=self)

    def _send_or_launch(
        self,
        port: int,
        script_name: str,
        payload: dict[str, object],
    ) -> dict[str, str]:
        response = self._try_send(port, payload, timeout=10.0)
        if response is not None:
            return response

        script_path = BASE_DIR / script_name
        proc = subprocess.Popen([sys.executable, str(script_path)])
        self._spawned_processes.append(proc)

        deadline = time.monotonic() + 6.0
        while time.monotonic() < deadline:
            response = self._try_send(port, payload, timeout=10.0)
            if response is not None:
                return response
            time.sleep(0.1)

        msg = f"Не вдалося підключитися до {script_name}."
        raise TimeoutError(msg)

    def _try_send(
        self,
        port: int,
        payload: dict[str, object],
        timeout: float,
    ) -> dict[str, str] | None:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.3) as sock:
                sock.settimeout(timeout)
                sock.sendall(json.dumps(payload).encode("utf-8"))
                sock.shutdown(socket.SHUT_WR)
                chunks: list[bytes] = []
                while True:
                    data = sock.recv(4096)
                    if not data:
                        break
                    chunks.append(data)
                if not chunks:
                    return {"status": "ok"}
                return json.loads(b"".join(chunks).decode("utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def _on_about(self) -> None:
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №6\nВзаємодія незалежних програм\nВаріант 2 (Ж = 14)",
            parent=self,
        )

    def _on_close(self) -> None:
        for port in (OBJECT2_PORT, OBJECT3_PORT):
            self._try_send(port, {"cmd": "close"}, timeout=0.5)
        for proc in self._spawned_processes:
            if proc.poll() is None:
                try:
                    proc.wait(timeout=0.5)
                except subprocess.TimeoutExpired:
                    proc.terminate()
        self.destroy()


def main() -> None:
    app = Lab6App()
    app.mainloop()


if __name__ == "__main__":
    main()
