#!/usr/bin/env bash
# test_requests.sh
# Testes obrigatórios com curl para a API de livros

# Desativa a conversão de rotas do Git Bash no Windows
export MSYS_NO_PATHCONV=1

BASE="http://localhost:8000/api"

run(){
    local description="$1"
    local method="$2"
    local url="$3"
    local data="$4"

    echo "----------------------------------------"
    echo "TESTE: $description"
    echo "$method $url"
    
    if [ -n "$data" ]; then
        echo "Body enviado: $data"
        # --data-raw garante que os caracteres e aspas do JSON cheguem intactos ao servidor
        curl -s -w "\nStatus: %{http_code}\n" \
             -X "$method" "$url" \
             -H "Content-Type: application/json; charset=utf-8" \
             --data-raw "$data"
    else
        curl -s -w "\nStatus: %{http_code}\n" \
             -X "$method" "$url" 
    fi
    echo
}

# ---- Operações obrigatórias (casos de sucesso) ----

run "Listar todos os livros" GET "$BASE/books"

run "Consultar livro existente" GET "$BASE/books/1"

run "Criar novo livro" POST "$BASE/books" '{"title": "Grande Sertao: Veredas", "author": "Guimaraes Rosa", "year": 1956, "available": true}'

run "Atualizar livro existente" PUT "$BASE/books/1" '{"title": "Dom Casmurro", "author": "Machado de Assis", "year": 1899, "available": false}'

run "Remover livro existente" DELETE "$BASE/books/2"

# ---- Casos de erro ----

run "Consultar livro inexistente (404)" GET "$BASE/books/999"

run "Consultar livro identificador inválido (400)" GET "$BASE/books/abc"

run "Criar livro com JSON malformado (400)" POST "$BASE/books" '{"title": "Livro quebrado",'

run "Criar livro com campo obrigatório ausente (400)" POST "$BASE/books" '{"title": "Sem autor", "year": 2020, "available": true}'

run "Criar livro com tipo de dado incompativel (400)" POST "$BASE/books" '{"title": "Ano errado", "author": "Author X", "year": "mil novecentos", "available": true}'

run "Atualizar livro inexistente (404)" PUT "$BASE/books/999" '{"title": "X", "author": "Y", "year": 2000, "available": true}'

run "Remover livro inexistente (404)" DELETE "$BASE/books/999"  

run "Acessar rota inexistente (404)" DELETE "$BASE/rota/inexistente"

echo "----------------------------------------"
echo "Testes concluídos."