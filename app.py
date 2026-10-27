"""Aplicación local de Saturno: sirve la interfaz en el navegador usando solo Python estándar."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import webbrowser

APP_DIR = Path(__file__).resolve().parent
PAGE = APP_DIR / "saturno.html"


class SaturnoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/saturno.html"):
            self.send_error(404, "No encontrado")
            return
        try:
            content = PAGE.read_bytes()
        except OSError:
            self.send_error(500, "No se pudo leer saturno.html")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, fmt, *args):
        # Mantén la consola limpia durante el uso normal.
        if args and str(args[1]) not in ("200",):
            super().log_message(fmt, *args)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), SaturnoHandler)
    host, port = server.server_address
    url = f"http://{host}:{port}/"
    print("Mi pequeño universo está listo.")
    print(f"Abre esta dirección: {url}")
    print("Para cerrar la aplicación, presiona Ctrl+C en esta ventana.")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando la aplicación...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
