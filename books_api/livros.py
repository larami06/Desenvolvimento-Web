# --------------------------------------------------------------------
# "Banco de dados" em memória
# --------------------------------------------------------------------

# Recurso no código + Representação dos Dados
books = [
    {"id": 1, "title": "Dom Casmurro", "author": "Machado de Assis", "year": 1899, "available": True},
    {"id": 2, "title": "O Cortico", "author": "Aluisio Azevedo", "year": 1890, "available": True},
]

# Contador simples para gerar o próximo id.
next_id = 3


def find_book(book_id):
    """Procura um livro pelo id na lista. Retorna None se não achar."""
    for book in books:
        if book["id"] == book_id:
            return book
    return None

# Representação dos Dados
def validate_book_data(data):
    """Confere se os dados de um livro são válidos.

    Retorna uma mensagem de erro (string) se algo estiver errado,
    ou None se os dados estiverem ok. Usada tanto no POST quanto no PUT,
    para não repetir a mesma validação duas vezes.
    """
    # O corpo precisa ser um objeto JSON (dicionário), não uma lista,
    # um número, um texto solto, etc.
    if not isinstance(data, dict):
        return "O corpo da requisição deve ser um objeto JSON."

    required_fields = ["title", "author", "year", "available"]
    for field in required_fields:
        if field not in data:
            return f"Campo obrigatório faltando: {field}"

    if not isinstance(data["title"], str):
        return "O campo 'title' deve ser texto."
    if not isinstance(data["author"], str):
        return "O campo 'author' deve ser texto."

    # Cuidado: em Python, bool é considerado um "tipo de int".
    # Por isso True/False é checado antes, para não ser aceito como year.
    if isinstance(data["year"], bool) or not isinstance(data["year"], int):
        return "O campo 'year' deve ser um número inteiro."

    if not isinstance(data["available"], bool):
        return "O campo 'available' deve ser true ou false."

    return None

