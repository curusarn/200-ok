from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import gzip
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'  # Default file to serve

        if os.path.exists(self.path[1:]):  # Check if file exists
            _, file_extension = os.path.splitext(self.path)
            content_type = self.get_content_type(file_extension)

            with open(self.path[1:], 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'200 OK')

    def get_content_type(self, file_extension):
        mime_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'text/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.gif': 'image/gif'
            # Add more MIME types as needed
        }
        return mime_types.get(file_extension, 'application/octet-stream')
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = None
        if content_length > 0:
            raw_body = self.rfile.read(content_length)
            if self.headers.get('Content-Encoding') == 'gzip':
                try:
                    body = gzip.decompress(raw_body)
                except Exception as e:
                    print(f"Failed to decompress gzip body: {e}")
                    body = raw_body
            else:
                body = raw_body

            try:
                data = json.loads(body)
                if len(str(data)) > 120:
                    print(f"Received POST data: {str(data)[:120]}...")
                else:
                    print(f"Received POST data: {data}")
            except json.JSONDecodeError:
                print(f"Received non-JSON POST data: {body[:120]}..." if len(body) > 120 else f"Received non-JSON POST data: {body}")

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
