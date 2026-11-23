import json
import random
import socket
import threading
import tkinter as tk
from tkinter import ttk

PORT = 50002
COLUMNS = 5


class Object2App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Object2 — Генератор вектора")
        self.geometry("460x420+360+40")

        self._running = True
        self._server_socket: socket.socket | None = None

        self._init_ui()
        self.protocol("WM_DELETE_WINDOW", self._shutdown)

        if not self._start_server():
            self.destroy()
            return

    def _init_ui(self) -> None:
        self._info_var = tk.StringVar(value="Очікування повідомлення від Lab6...")
        ttk.Label(self, textvariable=self._info_var, padding=(8, 6)).pack(
            side=tk.TOP, fill=tk.X
        )

        frame = ttk.Frame(self, padding=(8, 0, 8, 8))
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        col_ids = tuple(f"c{i}" for i in range(1, COLUMNS + 1))
        self._tree = ttk.Treeview(frame, columns=col_ids, show="headings")
        for i, col in enumerate(col_ids, start=1):
            self._tree.heading(col, text=f"Стовпець {i}")
            self._tree.column(col, width=82, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _start_server(self) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", PORT))
            sock.listen(5)
            self._server_socket = sock
        except OSError:
            return False

        thread = threading.Thread(target=self._serve_loop, daemon=True)
        thread.start()
        return True

    def _serve_loop(self) -> None:
        while self._running and self._server_socket is not None:
            try:
                conn, _ = self._server_socket.accept()
            except OSError:
                break
            with conn:
                self._handle_connection(conn)

    def _handle_connection(self, conn: socket.socket) -> None:
        try:
            chunks: list[bytes] = []
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                chunks.append(data)
            payload = json.loads(b"".join(chunks).decode("utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        cmd = payload.get("cmd")
        if cmd == "close":
            conn.sendall(json.dumps({"status": "ok"}).encode("utf-8"))
            self.after(0, self._shutdown)
            return

        if cmd == "generate":
            done = threading.Event()
            result: dict[str, str] = {"status": "ok"}
            self.after(0, self._generate_vector, payload, done, result)
            done.wait(timeout=10.0)
            try:
                conn.sendall(json.dumps(result).encode("utf-8"))
            except OSError:
                pass

    def _generate_vector(
        self,
        payload: dict[str, object],
        done: threading.Event,
        result: dict[str, str],
    ) -> None:
        try:
            n = int(payload["n"])
            min_val = float(payload["min"])
            max_val = float(payload["max"])

            values = [round(random.uniform(min_val, max_val), 3) for _ in range(n)]

            for item in self._tree.get_children():
                self._tree.delete(item)

            lines: list[str] = []
            for start in range(0, len(values), COLUMNS):
                chunk = values[start : start + COLUMNS]
                formatted = [f"{v:.3f}" for v in chunk]
                lines.append("\t".join(formatted))
                padded = formatted + [""] * (COLUMNS - len(formatted))
                self._tree.insert("", tk.END, values=padded)

            clipboard_text = "\n".join(lines)
            self.clipboard_clear()
            self.clipboard_append(clipboard_text)
            self.update()

            self._info_var.set(
                f"Згенеровано {n} чисел у діапазоні [{min_val}; {max_val}] (скопійовано в буфер)"
            )
            self.deiconify()
            self.lift()
        except (KeyError, TypeError, ValueError, tk.TclError) as exc:
            result["status"] = "error"
            result["error"] = str(exc)
        finally:
            done.set()

    def _shutdown(self) -> None:
        self._running = False
        if self._server_socket is not None:
            try:
                self._server_socket.close()
            except OSError:
                pass
            self._server_socket = None
        if self.winfo_exists():
            self.destroy()


def main() -> None:
    app = Object2App()
    if app.winfo_exists():
        app.mainloop()


if __name__ == "__main__":
    main()
