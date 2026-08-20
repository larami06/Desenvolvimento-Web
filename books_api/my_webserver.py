"""
Módulo de inicialização e execução do servidor Web.
"""

from http.server import HTTPServer
from server import BooksHandler


class MyWebServer:

    def __init__(self, handler=BooksHandler, host="", port=8000):
        self.host = host
        self.port = port
        self.handler = handler

    def run(self):
        server = HTTPServer((self.host, self.port), self.handler)
        print(f"Servidor rodando em http://localhost:{self.port}")
        server.serve_forever()


if __name__ == "__main__":
    app = MyWebServer()
    app.run()