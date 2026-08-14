from my_webserver import MyWebServer
from http.server import SimpleHTTPRequestHandler
import os

PORT = int(os.getenv('PORT', 3001))

class ManuseioHttpRequest(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html, charset=utf-8")
            self.end_headers()
            self.wfile.write("<p>Ola Mundo</p>".encode())

        if self.path == "/pagina1":
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html, charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<p>Essa seria a rota para a pagina 1</p>".encode())    

        if self.path == "/index":
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html, charset=utf-8")
                    self.end_headers()
                    with open("index.html", 'r') as f:
                           res_body = f.read().format_map({"PORT": PORT})
                    self.wfile.write(res_body.encode())

        else:
               self.send_error(418)

app = MyWebServer(ManuseioHttpRequest)

if __name__ == "__main__":
    app.run()