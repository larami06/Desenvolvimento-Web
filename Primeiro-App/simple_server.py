from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        message = "<html><body<h1>Ola mundo!</h1></body></html>"
        self.wfile.write(message.encode())

if __name__ == "__main__":
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Servidor rodando em http://127.0.0.1:8000")
    httpd.serve_forever()