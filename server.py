from http.server import SimpleHTTPRequestHandler, HTTPServer

class CORS(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

HTTPServer(("localhost", 8000), CORS).serve_forever()
