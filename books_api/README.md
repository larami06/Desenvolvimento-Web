# Desafio Prático — Construindo uma API REST para um Catálogo de Livros

**Alunos:** Ana Carla Del Puppo, Danielle, Gabriel Terres, Hikaro, Lara, Pedro Henrique Daniel e Vinícius

**Turma:** CC5N

## Pensando como um Projetista de APIs

### Por que o endereço /api/books/1 representa um recurso diferente de /api/books?
`/api/books` representa a coleção inteira de livros. `/api/books/1` representa um recurso individual específico dentro dessa coleção.

### Por que o método GET é utilizado para consultar livros?
O método GET é seguro e idempotente, servindo estritamente para leitura de dados sem alterar o estado do servidor.

### Por que o método POST é utilizado para criar um novo livro?
O POST é utilizado para submeter dados que resultarão no processamento e criação de um novo recurso no servidor.

### Qual é a diferença entre 400 Bad Request e 404 Not Found?
*   **400 Bad Request:** Indica que a requisição está malformada ou com dados/sintaxe inválidos (ex: ID contendo letras).
*   **404 Not Found:** Indica que a requisição está bem formatada, mas o recurso ou rota não foi encontrado no servidor.

### Por que uma exclusão realizada com sucesso pode retornar 204 No Content?
Porque o recurso foi removido com sucesso e não há mais nenhum dado/corpo para retornar ao cliente.

### O que aconteceria com os livros cadastrados se o servidor fosse encerrado?
Seriam perdidos, pois estão armazenados apenas na memória RAM (variável em memória).

### Quais limitações existem em uma aplicação que mantém seus dados exclusivamente em memória?
Falta de persistência (dados somem ao desligar/reiniciar), consumo limitado pela memória RAM do sistema e incapacidade de compartilhar dados entre múltiplas instâncias do servidor.

## Modelagem da API

### 1. Recursos (Entidades)
No código, o recurso é definido pelas estruturas em memória e variáveis que guardam e identificam os livros:
*   **A Lista de Livros (books):** Representa a coleção de recursos.
*   **A função `find_book(book_id)`:** Representa a busca por um recurso individual no sistema.

### 2. Representação dos Dados
No código, isso aparece na validação dos campos do dicionário e na conversão em JSON:
*   **Dicionários em Python:** A estrutura das chaves `id`, `title`, `author`, `year` e `available` reflete a representação JSON exigida pelo trabalho.
*   **A função `validate_book_data(data)`:** Garante que o corpo enviado pelo cliente siga estritamente os tipos de dados e os campos obrigatórios da representação.
*   **`json.dumps(data)` e `json.loads(raw_data)`:** Realizam a transformação entre a representação textual JSON (trafegada no HTTP) e o objeto em memória do Python.

### 3. Mapeamento de Rotas (Endpoints)
O mapeamento de rotas está organizado nas funções da classe `BooksHandler` que começam com `do_` (os métodos HTTP padrão da biblioteca `http.server`):
*   **`do_GET(self)`:** Mapeia as URIs `/api/books` (listar) e `/api/books/{id}` (consultar).
*   **`do_POST(self)`:** Mapeia a URI `/api/books` para criação.
*   **`do_PUT(self)`:** Mapeia a URI `/api/books/{id}` para atualização.
*   **`do_DELETE(self)`:** Mapeia a URI `/api/books/{id}` para remoção.
*   **Roteamento:** A verificação `if self.path == "/api/books"` ou `if self.path.startswith("/api/books/")` faz o papel do roteamento da aplicação.

### 4. Tratamento de Erros
No seu código, o tratamento de erros é feito através dos blocos condicionais de validação e dos métodos auxiliares de resposta HTTP:
*   **Método `send_error_json(status_code, message)`:** Centraliza o envio dos códigos de erro com uma mensagem descritiva.
*   **Captura de Exceções (`try...except json.JSONDecodeError`):** Trata requisições com corpo malformado enviando o status `400 Bad Request`.
*   **Validação de ID (`if not id_text.isdigit()`):** Trata IDs inválidos retornando `400 Bad Request`.
*   **Busca no banco (`if book is None`):** Trata recursos inexistentes retornando `404 Not Found`.
