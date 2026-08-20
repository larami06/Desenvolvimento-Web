"""
Módulo responsável por processar as requisições HTTP da API REST.
"""

from http.server import BaseHTTPRequestHandler
import json
import livros


class BooksHandler(BaseHTTPRequestHandler):

    # ---------- Funções Auxiliares ----------

    def send_json_response(self, status_code, data):
        """Manda uma resposta com corpo em JSON."""
        response_body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def send_empty_response(self, status_code):
        """Manda uma resposta sem corpo (usado no 204 do DELETE)."""
        self.send_response(status_code)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def send_error_json(self, status_code, message):
        self.send_json_response(status_code, {"error": message})

    def get_request_body(self):
        """Lê o corpo da requisição e tenta transformar em dicionário Python."""
        content_length = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(content_length)
        return json.loads(raw_data)

    # ---------- GET ----------

    def do_GET(self):
        # GET /api/books -> lista todos os livros
        if self.path == "/api/books":
            self.send_json_response(200, livros.books)
            return

        # GET /api/books/{id} -> um livro específico
        if self.path.startswith("/api/books/"):
            id_text = self.path.replace("/api/books/", "")

            if not id_text.isdigit():
                self.send_error_json(400, "Id inválido, deve ser um número.")
                return

            book_id = int(id_text)
            book = livros.find_book(book_id)

            if book is None:
                self.send_error_json(404, "Livro não encontrado.")
                return

            self.send_json_response(200, book)
            return

        self.send_error_json(404, "Rota não encontrada.")

    # ---------- POST ----------

    def do_POST(self):
        if self.path != "/api/books":
            self.send_error_json(404, "Rota não encontrada.")
            return

        try:
            data = self.get_request_body()
        except json.JSONDecodeError:
            self.send_error_json(400, "JSON inválido.")
            return

        error_message = livros.validate_book_data(data)
        if error_message is not None:
            self.send_error_json(400, error_message)
            return

        new_book = {
            "id": livros.next_id,
            "title": data["title"],
            "author": data["author"],
            "year": data["year"],
            "available": data["available"],
        }
        livros.books.append(new_book)
        livros.next_id += 1

        self.send_json_response(201, new_book)

    # ---------- PUT ----------

    def do_PUT(self):
        if not self.path.startswith("/api/books/"):
            self.send_error_json(404, "Rota não encontrada.")
            return

        id_text = self.path.replace("/api/books/", "")
        if not id_text.isdigit():
            self.send_error_json(400, "Id inválido, deve ser um número.")
            return

        book_id = int(id_text)
        book = livros.find_book(book_id)

        if book is None:
            self.send_error_json(404, "Livro não encontrado.")
            return

        try:
            data = self.get_request_body()
        except json.JSONDecodeError:
            self.send_error_json(400, "JSON inválido.")
            return

        error_message = livros.validate_book_data(data)
        if error_message is not None:
            self.send_error_json(400, error_message)
            return

        book["title"] = data["title"]
        book["author"] = data["author"]
        book["year"] = data["year"]
        book["available"] = data["available"]

        self.send_json_response(200, book)

    # ---------- DELETE ----------

    def do_DELETE(self):
        if not self.path.startswith("/api/books/"):
            self.send_error_json(404, "Rota não encontrada.")
            return

        id_text = self.path.replace("/api/books/", "")
        if not id_text.isdigit():
            self.send_error_json(400, "Id inválido, deve ser um número.")
            return

        book_id = int(id_text)
        book = livros.find_book(book_id)

        if book is None:
            self.send_error_json(404, "Livro não encontrado.")
            return

        livros.books.remove(book)
        self.send_empty_response(204)