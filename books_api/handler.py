"""
handler.py
Todas as rotas, validação JSON e código de status.
Implementa a API Rest de catálogo de livros usando a lib padrão (http.server, json e re)

Modelagem:
Recurso        Coleção      Item
---------------------------------------------
Livro          /api/books   /api/books/{id}

Métodos:
GET /api/books -> retorna todos os livros
GET  /api/books/{id} -> consulta um livro específico, pelo id
POST /api/books -> cria um novo livro
PUT /api/books/{id} -> atualiza (substitui) um livro existente pelo id
DELETE /api/books/{id} -> -> remove um livro existente

Conforme devidamente solicitado no exercícío, qualquer outra combinação de método/rota é tratada como erro (400 ou 404)
"""

import json
import re
from http.server import BaseHTTPRequestHandler

from storage import BookNotFoundError, BookStorage

storage = BookStorage()  # instancia o armazenamento de livros

# /api/books ou api/books/ 
COLLECTION_PATH = re.compile(r"^/api/books/?$")

# /api/books/{qualquer coisa} (item - a validação do id acontece depois)
ITEM_PATH = re.compile(r"^/api/books/([^/]+)/?$")

REQUIRED_FIELDS = {
    "title": str,
    "author": str,
    "year": int,
    "available": bool,
}

class BooksRequestHandler(BaseHTTPRequestHandler):
    """Trata as requisições HTTP recebidas pelo servidor."""

    server_version = "BooksAPI/1.0"

# ----- Utilitários de resposta -----
    def send_json(self, status_code: int, payload=None, headers: dict = None):
        """
        Envia uma resposta JSON com o código de status informado
        Se 'payload' for None, nenhum corpo é enviado (usado para 204) 
        """ 

        body = b""
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        self.send_response(status_code)

        if headers:
            for key, value in headers.items():
                self.send_header(key, value)

        if body:
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
        else:
            self.send_header("Content-Length", "0")
            
        self.end_headers()

        if body:
            self.wfile.write(body)
            self.wfile.flush()  # Garante que os bytes saiam do buffer do socket

    def send_error_response(self, status_code: int, message: str):
        """
        Padroniza o formato de erro: {"error": "..."}
        """
        self.send_json(status_code, {"error":message})

    # ----- leitura e validação do corpo e da requisição -----
    def read_json_body(self):
        """ 
        Lê e decodifica o corpo da requisição como JSON.
        Retorna (dados, None) em caso de sucesso, ou (None, mensagem_erro) caso o corpo esteja ausente ou inválido
        """

        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None, "Corpo da requisição vazio; um JSON era esperado."

        raw_body = self.rfile.read(length)

        
        body_str = None
        for encoding in ("utf-8", "cp1252", "latin-1"):
            try:
                body_str = raw_body.decode(encoding)
                break
            except (UnicodeDecodeError, LookupError):
                continue

        if body_str is None:
            return None, "Erro de codificação nos caracteres do corpo."

        try:
            data = json.loads(raw_body)

        except json.JSONDecodeError:
            return None, "JSON malformado."

        if not isinstance(data, dict):
            return None, "O corpo da requisição deve ser um objeto JSON."
        
        return data, None

    def validate_book_payload(self, data:dict):
        """
        Confere se todos os campos obrigatórios estão presentes e com o tipo correto. 
        Retorna uma mensagem de erro, ou None se estiver ok
        """
        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            return f"Capos obrigatórios ausentes: {', '.join(missing)}."

        for field, expected_type in REQUIRED_FIELDS.items():
            value = data[field]
            if expected_type is bool:
                if not isinstance(value, bool):
                    return f"Campo '{field}' deve ser um valor booleano (true/false)."

            elif expected_type is int:
                if not isinstance(value, int):
                    return f"Campo '{field}' deve ser um número inteiro."
            
            elif expected_type is str:
                if not isinstance(value, str) or not value.strip():
                    return f"Campo '{field}' deve ser uma string."

        return None

    # ----- Resolução de rota / id -----
    def _resolve_book_id(self, raw_id: str):
        """
        Converte o segmento de id da URI para int
        Retorna (id, None) em caso de sucesso, ou (None, mensagem_erro) caso o formato do id for inválido.
        """
        if not raw_id.isdigit():
            return None, f"Identificador inválido: '{raw_id}'. Esperado um número inteiro."
        return int(raw_id), None

    # ----- Handlers por método HTTP -----
    def do_GET(self):
        if COLLECTION_PATH.match(self.path):
            self.send_json(200, storage.list_all())
            return

        match = ITEM_PATH.match(self.path)
        if match:
            book_id, error = self._resolve_book_id(match.group(1))
            if error:
                self.send_error_response(400, error)
                return
            try:
                book = storage.get(book_id)
            except BookNotFoundError:
                self.send_error_response(404, f"Livro com id {book_id} não encontrado.")
                return

            self.send_json(200, book)
            return
        self.send_error_response(404, f"Rota não encontrada: {self.path}")

    def do_POST(self):
        if not COLLECTION_PATH.match(self.path):
            self.send_error_response(404, f"Rota não encontrada: {self.path}")
            return

        data, error = self.read_json_body()
        if error:
            self.send_error_response(400, error)
            return

        validation_error = self.validate_book_payload(data)
        if validation_error:
            self.send_error_response(400, validation_error)
            return

        book = storage.create(data)

        extra_headers = {"Location": f"/api/books/{book['id']}"}
        self.send_json(201, book, headers=extra_headers)

    def do_PUT(self):
        match = ITEM_PATH.match(self.path)
        if not match:
            self.send_error_response(
                404, f"Rota não encontrada ou inválida para PUT: {self.path}"
            )
            return

        book_id, error = self._resolve_book_id(match.group(1))
        if error:
            self.send_error_response(400, error)
            return
        
        data, error = self.read_json_body()
        if error:
            self.send_error_response(400, error)
            return

        validation_error = self.validate_book_payload(data)
        if validation_error:
            self.send_error_response(400, validation_error)
            return

        try:
            book = storage.update(book_id, data)
        except BookNotFoundError:
            self.send_error_response(404, f"Livro com id {book_id} não encontrado.")
            return

        self.send_json(200, book)

    def do_DELETE(self):
        match = ITEM_PATH.match(self.path)
        if not match:
            self.send_error_response(
                404, f"Rota não encontrada ou inválida para DELETE: {self.path}"
            )
            return

        book_id, error = self._resolve_book_id(match.group(1))
        if error:
            self.send_error_response(400, error)
            return

        try:
            storage.delete(book_id)
        except BookNotFoundError:
            self.send_error_response(404, f"Livro com id {book_id} não encontrado.")
            return

        self.send_json(204)  # 204 No Content, sem corpo de resposta.

    # ----- Fallback para métodos não suportados -----
    def _method_not_allowed(self):
        self.send_error_response(405, f"Método {self.command} não permitido para a rota {self.path}")

    def do_PATCH(self):
        self._method_not_allowed()

    # ----- Logging mais legível no console -----
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}")
