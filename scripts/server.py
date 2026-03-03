import http.server
import os
from pathlib import Path

PORT = int(os.getenv("PORT", "5000"))

# project root = one level up from /scripts
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = PROJECT_ROOT / "frontend"


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control",
                         "no-cache, no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


if __name__ == "__main__":
    if not DIRECTORY.exists():
        raise RuntimeError(f"Frontend directory not found: {DIRECTORY}")

    server = http.server.HTTPServer(("0.0.0.0", PORT), NoCacheHandler)
    print(f"Serving frontend from {DIRECTORY} on http://0.0.0.0:{PORT}")
    server.serve_forever()
