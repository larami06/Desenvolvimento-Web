"""
server.py

Sobe o HTTPServer, utilizando a lib padrão do Python e delega o tratamento das requisições para BooksRequest em handler.py

Se nenhuma porta for informada, o servidor sobe na porta 8000
"""

import sys
from http.server import HTTPServer
from handler import BooksRequestHandler

def main():
    # defindo a porta padrão
    port = 8000 

    # verifica se há algum numero extra na porta digitada
    if len(sys.argv) > 1:
        try:
            # transforma o argumento em inteiro e usa como porta            
            port = int(sys.argv[1])

        except ValueError:
            # caso o argumento seja inválido, ele segue com a porta padrão
            print(f"Porta inválida: '{sys.argv[1]}'. Usando a porta padrão 8000.")
            port = 8000

    server_address = ("", port) # "" significa aceitar requisições de qualquer endereço IP
    httpd = HTTPServer(server_address, BooksRequestHandler) # pede ao http acessar o endereço e utilizar o livro

    print(f"API de catálogo de livros rodando em http://localhost:{port}")
    print(f"EndPoints disponíveis:")
    print(f" GET /api/books")
    print(f" GET /api/books/{id}")
    print(f" POST /api/books")
    print(f" PUT /api/books/{id}")
    print(f" DELETE /api/books/{id}")
    print("\nPressione Ctrl+C para encerrar o servidor.\n")

    # encerrar servidor
    try:
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        httpd.server_close()

if __name__ == "__main__":
    main()