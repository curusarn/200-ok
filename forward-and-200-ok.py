from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import gzip
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError

FORWARD_URL = os.environ.get('FORWARD_URL')
if not FORWARD_URL:
    print("ERROR: FORWARD_URL environment variable is required")
    print("Example: FORWARD_URL=http://example.com:8080 python forward-and-200-ok.py")
    sys.exit(1)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def forward_request(self, method):
        headers = dict(self.headers)
        headers.pop('Host', None)
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = None
        if content_length > 0:
            raw_body = self.rfile.read(content_length)
            if self.headers.get('Content-Encoding') == 'gzip':
                try:
                    body = gzip.decompress(raw_body)
                    headers['Content-Encoding'] = 'identity'
                    headers['Content-Length'] = str(len(body))
                except Exception as e:
                    print(f"Failed to decompress gzip body: {e}")
                    body = raw_body
            else:
                body = raw_body

        url = FORWARD_URL + self.path
        
        try:
            print(f"Forwarding {method} request to: {url}")
            req = Request(url, data=body, headers=headers, method=method)
            response = urlopen(req)
            print(f"Forward response status: {response.status}")
        except Exception as e:
            print(f"Failed to forward request: {e}")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'200 OK')

    def do_GET(self):
        self.forward_request('GET')

    def do_POST(self):
        self.forward_request('POST')

    def do_PUT(self):
        self.forward_request('PUT')

    def do_DELETE(self):
        self.forward_request('DELETE')
    
    def do_HEAD(self):
        self.forward_request('HEAD')
    
    def do_PATCH(self):
        self.forward_request('PATCH')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started on port {port}")
    print(f"Forwarding requests to: {FORWARD_URL}")
    httpd.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        run(port=port)
    else:
        run()