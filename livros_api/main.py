from http.server import HTTPServer
from server import LivrosHandler

PORTA = 8000

servidor = HTTPServer(("localhost", PORTA), LivrosHandler)

print(f"Servidor rodando em http://localhost:{PORTA}")

try:
    servidor.serve_forever()

except KeyboardInterrupt:
    print("\nServidor encerrado.")

finally:
    servidor.server_close()