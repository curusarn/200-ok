from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'200 OK')

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            try:
                import json
                data = json.loads(body)
            except json.JSONDecodeError:
                data = None
        if data:
            if len(str(data)) > 120:
                print(f"Received POST data: {str(data)[:120]}...")
            else:
                print(f"Received POST data: {data}")
            import random
            import string
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            filename = f'/tmp/always-200-ok-{random_str}.json'
            with open(filename, 'w') as f:
                json.dump(data, f)
            print(f"Saved POST data to {filename}")

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'200 OK')

    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'200 OK')

    def do_DELETE(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'200 OK')
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'200 OK')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
