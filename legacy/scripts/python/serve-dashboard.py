#\!/usr/bin/env python3
"""
Simple HTTP server to serve the dashboard and JSONL files
Solves CORS issues with loading local files
"""

import http.server
import socketserver
import os
import sys

PORT = 8080

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        # Set correct content type for JSONL files
        if self.path.endswith('.jsonl'):
            self.send_response(200)
            self.send_header('Content-type', 'application/x-ndjson')
            self.end_headers()
            
            file_path = self.path.lstrip('/')
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, f"File not found: {file_path}")
        else:
            super().do_GET()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    
    Handler = CORSRequestHandler
    
    print(f"Starting server on http://localhost:{PORT}")
    print(f"Serving directory: {os.getcwd()}")
    print("\nOpen your browser to:")
    print(f"  http://localhost:{PORT}/VIRTUAL_SCROLL_DASHBOARD.html")
    print("\nPress Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            sys.exit(0)
EOF < /dev/null