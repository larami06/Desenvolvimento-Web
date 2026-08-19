"""
storage.py
Os dados são mantidos inteiramente em memória, em um dicionário indexado pelo id do livro, 
ou seja, todo catálogo é perdido quando o servidor é encerrado.
"""

from itertools import count
from typing import Optional

class BookNotFoundError(Exception):
    """Levantada quando um id não corresponde a nenhum livro existente."""
    pass

class BookStorage:
    """Armazena livros em memória e gera ids automaticamente."""

    def __init__(self):
        self._books = {}  # dicionário para armazenar livros, indexado pelo id
        self._id_counter = count(1)  # contador para gerar ids únicos
        self._seed()

    def _seed(self):
        """Popula o catálogo com alguns livros iniciais, só para facilitar os testes."""
        seed_books = [
            {
                "title": "Dom Casmurro",
                "author": "Machado de Assis",
                "year": 1899,
                "available": True,
            },
            {
                "title": "O Cortiço",
                "author": "Aluísio Azevedo",
                "year": 1890,
                "available": True,
            },
        ]
        for book in seed_books:
            self.create(book)

    def list_all(self) -> list:
        """Retorna todos os livros como uma lista, orndenado por id."""
        return [self._books[book_id] for book_id in sorted(self._books)]

    def get(self, book_id: int) -> dict:
        """Retorna o livro com o id informado ou levanta BookNotFoundError."""
        book = self._books.get(book_id)
        if book is None:
            raise BookNotFoundError(book_id)
        return book

    def exists(self, book_id: int) -> bool:
        return book_id in self._books

    def create(self, data: dict) -> dict:
        """Cria um novo livro, atribuindo automaticamente id único"""
        new_id = next(self._id_counter)
        book = {
            "id": new_id,
            "title": data["title"],
            "author": data["author"],
            "year": data["year"],
            "available": data["available"],
        }
        self._books[new_id] = book
        return book

    def update(self, book_id: int, data: dict) -> dict:
        """Substitui os dados do livro existente (PUT = substituição completa)"""
        if not self.exists(book_id):
            raise BookNotFoundError(book_id)
        book = {
            "id": book_id,
            "title": data["title"],
            "author": data["author"],
            "year": data["year"],
            "available": data["available"],
        }
        self._books[book_id] = book
        return book

    def delete(self, book_id: int) -> None:
        """Remove o livro com o id informado ou levanta BookNotFoundError."""
        if not self.exists(book_id):
            raise BookNotFoundError(book_id)
        del self._books[book_id]