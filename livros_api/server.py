from http.server import BaseHTTPRequestHandler
import json
import livros

class LivrosHandler(BaseHTTPRequestHandler):

    def enviar_resposta_json(self, codigo_status, dados):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")

        self.send_response(codigo_status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def enviar_resposta_vazia(self, codigo_status):
        self.send_response(codigo_status)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def enviar_erro_json(self, codigo_status, mensagem):
        self.enviar_resposta_json(codigo_status, {"erro": mensagem})

    def obter_corpo_requisicao(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        dados_brutos = self.rfile.read(tamanho)
        return json.loads(dados_brutos)

    def obter_id_da_url(self):
        id_texto = self.path.replace("/api/livros/", "")

        if not id_texto.isdigit():
            self.enviar_erro_json(400, "Id inválido, deve ser um número.")
            return None

        return int(id_texto)

    # ---------- GET ----------

    def do_GET(self):
        if self.path == "/api/livros":
            dados = [
                livro.para_dicionario()
                for livro in livros.livros
            ]

            self.enviar_resposta_json(200, dados)
            return

        if self.path.startswith("/api/livros/"):
            livro_id = self.obter_id_da_url()

            if livro_id is None:
                return

            livro = livros.encontrar_livro(livro_id)

            if livro is None:
                self.enviar_erro_json(404, "Livro não encontrado.")
                return

            self.enviar_resposta_json(200, livro.para_dicionario())
            return

        self.enviar_erro_json(404, "Rota não encontrada.")

    # ---------- POST ----------

    def do_POST(self):
        if self.path != "/api/livros":
            self.enviar_erro_json(404, "Rota não encontrada.")
            return

        try:
            dados = self.obter_corpo_requisicao()
        except json.JSONDecodeError:
            self.enviar_erro_json(400, "JSON malformado.")
            return

        mensagem_erro = livros.validar_dados_livro(dados)

        if mensagem_erro is not None:
            self.enviar_erro_json(400, mensagem_erro)
            return

        novo_livro = livros.Livro(
            livros.proximo_id,
            dados["titulo"],
            dados["autor"],
            dados["ano"],
            dados["disponivel"]
        )

        livros.livros.append(novo_livro)
        livros.proximo_id += 1

        self.enviar_resposta_json(201, novo_livro.para_dicionario())

    # ---------- PUT ----------

    def do_PUT(self):
        if not self.path.startswith("/api/livros/"):
            self.enviar_erro_json(404, "Rota não encontrada.")
            return

        livro_id = self.obter_id_da_url()

        if livro_id is None:
            return

        livro = livros.encontrar_livro(livro_id)

        if livro is None:
            self.enviar_erro_json(404, "Livro não encontrado.")
            return

        try:
            dados = self.obter_corpo_requisicao()
        except json.JSONDecodeError:
            self.enviar_erro_json(400, "JSON inválido.")
            return

        mensagem_erro = livros.validar_dados_livro(dados)

        if mensagem_erro is not None:
            self.enviar_erro_json(400, mensagem_erro)
            return

        livro.atualizar(dados)

        self.enviar_resposta_json(200, livro.para_dicionario())

    # ---------- DELETE ----------

    def do_DELETE(self):
        if not self.path.startswith("/api/livros/"):
            self.enviar_erro_json(404, "Rota não encontrada.")
            return

        livro_id = self.obter_id_da_url()

        if livro_id is None:
            return

        livro = livros.encontrar_livro(livro_id)

        if livro is None:
            self.enviar_erro_json(404, "Livro não encontrado.")
            return

        livros.livros.remove(livro)
        self.enviar_resposta_vazia(204)
