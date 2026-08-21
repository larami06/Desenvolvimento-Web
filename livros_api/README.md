# Desafio Prático — Construindo uma API REST para um Catálogo de Livros

**Alunos:** Ana Carla Del Puppo, Danielle, Gabriel Terres, Hikaro, Lara, Pedro Henrique Daniel e Vinícius

**Turma:** CC5N

## Pensando como um Projetista de APIs

### 1. Por que o endereço /api/books/1 representa um recurso diferente de /api/books?
O endereço `/api/books` representa a coleção inteira (a lista com todos os livros). Já o endereço `/api/books/1` representa um item específico dentro dessa coleção, que é o livro de número ID 1

### 2. Por que o método GET é utilizado para consultar livros?
Porque o método GET serve apenas para ler/buscar informações do servidor sem alterar nada. Ele é um método seguro que não cria, não modifica e nem apaga dados.

### 3. Por que o método POST é utilizado para criar um novo livro?
Porque o POST é o método HTTP padrão para enviar novos dados ao servidor para que um novo recurso seja processado e criado.

### 4. Qual é a diferença entre 400 Bad Request e 404 Not Found?
*   **400 Bad Request:** O erro está na forma como o cliente enviou a requisição. Exemplo: mandar um ID com letras em vez de números ou enviar um JSON faltando campos obrigatórios.
*   **404 Not Found:** A requisição foi feita no formato correto, mas o endereço ou o recurso não existe no servidor. Exemplo: tentar buscar o livro com ID 999 que não está cadastrado.

### 5. Por que uma exclusão realizada com sucesso pode retornar 204 No Content?
Porque o número 204 indica que a ação deu certo, mas o termo No Content ("Sem Conteúdo") significa que não sobrou nenhum dado para devolver no corpo da resposta, já que o item acabou de ser apagado.

### 6. O que aconteceria com os livros cadastrados se o servidor fosse encerrado?
Todos os livros novos criados enquanto o servidor rodava seriam apagados. Ao ligar o servidor de novo, ele voltaria apenas com a lista inicial configurada no código.

### 7. Quais limitações existem em uma aplicação que mantém seus dados exclusivamente em memória?
* Falta de persistência: Se a aplicação fechar, reiniciar ou cair, todos os dados cadastrados são perdidos. 
* Limite de tamanho: A quantidade de dados fica limitada à memória RAM disponível no computador.  
* Sem compartilhamento: Outros servidores ou sistemas externos não conseguem acessar esses dados de forma centralizada de fora da memória daquela aplicação. 


# Modelagem da API

## 1. Recursos (Entidades)
O recurso é definido pela classe do domínio, pela lista em memória e pela função de busca que gerenciam os livros:

* **A classe `Livro`:** Define o modelo e o comportamento do recurso no sistema (contendo atributos e os métodos `atualizar` e `para_dicionario`).
* **A Lista de Livros (`livros.livros`):** Representa a coleção global dos recursos mantida em memória.
* **A função `encontrar_livro(livro_id)`:** Responsável por localizar e retornar um recurso individual com base no seu identificador.

---

## 2. Representação dos Dados
A representação dos dados ocorre através do mapeamento do objeto Python para JSON e da validação da estrutura enviada pelo cliente:

* **A classe `Livro` e o método `para_dicionario()`:** Mapeia a estrutura interna do objeto com os campos `id`, `titulo`, `autor`, `ano` e `disponivel` para um dicionário Python pronto para ser serializado em JSON.
* **A função `validar_dados_livro(dados)`:** Garante que o corpo enviado na requisição siga estritamente os tipos de dados aceitos e que todos os campos obrigatórios estejam presentes.
* **Uso da biblioteca `json` (`json.dumps` e `json.loads`):** No handler, a conversão é realizada no método `obter_corpo_requisicao()` (desserialização) e no método `enviar_resposta_json()` (serialização para UTF-8).

---

## 3. Mapeamento de Rotas (Endpoints)
O mapeamento das rotas está estruturado na classe `LivrosHandler` (herdada de `BaseHTTPRequestHandler`), utilizando os métodos de ciclo de vida HTTP padrão:

* **`do_GET(self)`:** Mapeia as rotas `/api/livros` (listagem de todos os livros com status `200 OK`) e `/api/livros/{id}` (consulta de um livro específico).
* **`do_POST(self)`:** Mapeia a rota `/api/livros` para criação de novos registros, retornando o objeto criado e status `201 Created`.
* **`do_PUT(self)`:** Mapeia a rota `/api/livros/{id}` para atualização completa dos dados do livro, retornando status `200 OK`.
* **`do_DELETE(self)`:** Mapeia a rota `/api/livros/{id}` para remoção do recurso, retornando uma resposta sem corpo com status `204 No Content`.
* **Roteamento:** É feito manualmente através de condicionais como `if self.path == "/api/livros"` e `if self.path.startswith("/api/livros/")`.

---

## 4. Tratamento de Erros
O tratamento de erros e respostas atípicas é centralizado no handler através de métodos auxiliares e checagens condicionais:

* **Método `enviar_erro_json(codigo_status, mensagem)`:** Padroniza a resposta de erro enviando um JSON com o formato `{"erro": "mensagem"}` e o respectivo código HTTP.
* **Captura de Exceções (`try...except json.JSONDecodeError`):** Intercepta JSONs malformados ou inválidos nas requisições POST e PUT, respondendo com status `400 Bad Request`.
* **Validação de ID (`obter_id_da_url`):** Utiliza `id_texto.isdigit()` para garantir que o parâmetro de URL seja numérico, retornando `400 Bad Request` em caso negativo.
* **Recurso Inexistente (`if livro is None`):** Valida a existência do registro antes de operar sobre ele, retornando `404 Not Found` caso não seja localizado.
* **Rota Inexistente:** Caso o caminho acessado não corresponda a nenhuma rota esperada dentro de `do_GET`, `do_POST`, `do_PUT` ou `do_DELETE`, a API responde com status `404 Not Found`.