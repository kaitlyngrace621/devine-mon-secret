from http.server import BaseHTTPRequestHandler
import os, json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ready=bool(os.environ.get('OPENAI_API_KEY')) and bool(os.environ.get('GAME_ACCESS_CODE'))
        raw=json.dumps({'ready': ready}).encode()
        self.send_response(200)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
