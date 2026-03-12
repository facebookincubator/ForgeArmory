import http.server
import socketserver


class PersistentHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Length", 13)
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        self.wfile.write(b"Hello, World!")


class PersistentHTTPServer(socketserver.TCPServer):
    allow_reuse_address = True


with PersistentHTTPServer(("", 80), PersistentHTTPHandler) as httpd:
    httpd.serve_forever()
