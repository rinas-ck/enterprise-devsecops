from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status = 200
            response = {"status": "healthy"}
        elif self.path == "/":
            status = 200
            response = {"service": "devsecops-api", "version": "1.0.0"}
        else:
            status = 404
            response = {"error": "not found"}

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("API listening on port 8000")
    server.serve_forever()
