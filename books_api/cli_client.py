import json
import sys
import urllib.error
import urllib.request

BASE_URL = "http://localhost:8000/api"


def request_api(method: str, path: str, data: dict = None):
    """Realiza a requisição HTTP para o servidor da API."""
    url = f"{BASE_URL}{path}"
    headers = {}
    body_bytes = None

    if data is not None:
        body_bytes = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    req = urllib.request.Request(
        url, data=body_bytes, headers=headers, method=method
    )

    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            response_body = response.read().decode("utf-8")
            location = response.headers.get("Location")

            print(f"\n✅ Status: {status}")
            if location:
                print(f"📌 Header Location: {location}")

            if response_body:
                parsed = json.loads(response_body)
                print("\n📄 Resposta do Servidor:")
                print(json.dumps(parsed, indent=2, ensure_ascii=False))
            else:
                print("\n📄 Resposta: Sem corpo de conteúdo (204 No Content).")

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"\n❌ Status de Erro: {e.code}")
        if error_body:
            try:
                parsed = json.loads(error_body)
                print(
                    f"⚠️ Mensagem: {json.dumps(parsed, indent=2, ensure_ascii=False)}"
                )
            except Exception:
                print(f"⚠️ Mensagem: {error_body}")

    except urllib.error.URLError as e:
        print(
            f"\n🚫 Erro de Conexão: O servidor está rodando em {BASE_URL}? ({e.reason})"
        )


def menu_listar():
    print("\n--- 📚 LISTAR TODOS OS LIVROS ---")
    request_api("GET", "/books")


def menu_consultar():
    print("\n--- 🔍 CONSULTAR LIVRO POR ID ---")
    book_id = input("Digite o ID do livro: ").strip()
    request_api("GET", f"/books/{book_id}")


def menu_criar():
    print("\n--- ➕ CADASTRAR NOVO LIVRO ---")
    title = input("Título: ").strip()
    author = input("Autor: ").strip()

    try:
        year = int(input("Ano de publicação: ").strip())
    except ValueError:
        print("❌ O ano deve ser um número inteiro!")
        return

    available_input = (
        input("Está disponível? (s/n): ").strip().lower()
    )
    available = available_input in ["s", "sim", "true", "1"]

    payload = {
        "title": title,
        "author": author,
        "year": year,
        "available": available,
    }

    request_api("POST", "/books", payload)


def menu_atualizar():
    print("\n--- ✏️ ATUALIZAR LIVRO EXISTENTE ---")
    book_id = input("Digite o ID do livro que deseja atualizar: ").strip()

    print("Informe os NOVOS dados do livro:")
    title = input("Novo Título: ").strip()
    author = input("Novo Autor: ").strip()

    try:
        year = int(input("Novo Ano: ").strip())
    except ValueError:
        print("❌ O ano deve ser um número inteiro!")
        return

    available_input = (
        input("Está disponível? (s/n): ").strip().lower()
    )
    available = available_input in ["s", "sim", "true", "1"]

    payload = {
        "title": title,
        "author": author,
        "year": year,
        "available": available,
    }

    request_api("PUT", f"/books/{book_id}", payload)


def menu_remover():
    print("\n--- 🗑️ REMOVER LIVRO ---")
    book_id = input("Digite o ID do livro a ser removido: ").strip()
    request_api("DELETE", f"/books/{book_id}")


def main():
    while True:
        print("\n" + "=" * 40)
        print("     📖 CATÁLOGO DE LIVROS - CLIENTE CLI")
        print("=" * 40)
        print("1. Listar todos os livros (GET /api/books)")
        print("2. Consultar livro por ID (GET /api/books/{id})")
        print("3. Criar novo livro (POST /api/books)")
        print("4. Atualizar livro (PUT /api/books/{id})")
        print("5. Remover livro (DELETE /api/books/{id})")
        print("0. Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_listar()
        elif opcao == "2":
            menu_consultar()
        elif opcao == "3":
            menu_criar()
        elif opcao == "4":
            menu_atualizar()
        elif opcao == "5":
            menu_remover()
        elif opcao == "0":
            print("\nEncerrando o cliente... Até logo!")
            sys.exit(0)
        else:
            print("\n❌ Opção inválida! Tente novamente.")

        input("\nPressione [ENTER] para voltar ao menu...")


if __name__ == "__main__":
    main()