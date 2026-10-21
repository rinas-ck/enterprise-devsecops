from http.server import BaseHTTPRequestHandler, HTTPServer
import json

SERVICE = 'notifications-service'
ROUTE = '/notifications'
PAYLOAD = {'service': 'notifications-service', 'status': 'ready'}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status, response = 200, {"status": "healthy", "service": SERVICE}
        elif self.path == ROUTE:
            status, response = 200, PAYLOAD
        else:
            status, response = 404, {"error": "not found"}

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print(f"{SERVICE} listening on port 8000")
    server.serve_forever()
