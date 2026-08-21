class Livro:
    def __init__(self, id, titulo, autor, ano, disponivel):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = disponivel

    def atualizar(self, dados):
        self.titulo = dados["titulo"]
        self.autor = dados["autor"]
        self.ano = dados["ano"]
        self.disponivel = dados["disponivel"]

    def para_dicionario(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "disponivel": self.disponivel
        }


livros = [
    Livro(1, "Dom Casmurro", "Machado de Assis", 1899, True),
    Livro(2, "O Cortiço", "Aluísio Azevedo", 1890, True),
    Livro(3, "O Guarani", "José de Alencar", 1857, True)
]

proximo_id = 4

def encontrar_livro(livro_id):
    for livro in livros:
        if livro.id == livro_id:
            return livro

    return None

def validar_dados_livro(dados):
    if not isinstance(dados, dict):
        return "O corpo da requisição deve ser um objeto JSON."

    campos_obrigatorios = ["titulo", "autor", "ano", "disponivel"]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return f"Campo obrigatório faltando: {campo}"

    if not isinstance(dados["titulo"], str):
        return "O campo 'titulo' deve ser texto."

    if not isinstance(dados["autor"], str):
        return "O campo 'autor' deve ser texto."

    if isinstance(dados["ano"], bool) or not isinstance(dados["ano"], int):
        return "O campo 'ano' deve ser um número inteiro."

    if not isinstance(dados["disponivel"], bool):
        return "O campo 'disponivel' deve ser true ou false."

    return None