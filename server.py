import http.server
import os

PORT = 5000
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), NoCacheHandler)
    print(f"Serving frontend on http://0.0.0.0:{PORT}")
    server.serve_forever()
