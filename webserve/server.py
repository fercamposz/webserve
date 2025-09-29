import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

class MyHandle(SimpleHTTPRequestHandler):
    def accont_user(self, login, password):
        loga = "fer@gmail.com"
        senha = 1234
        return "Usuário Logado" if login == loga and senha == password else "Usuário não existe"

    def do_GET(self):
        # Mapeamento de rotas para arquivos HTML
        rotas = {
            "/": "index.html",
            "/login": "login.html",
            "/cadastroFilme": "cadastroFilme.html",
            "/listarFilme": "listarFilme.html"
        }

        if self.path in rotas:
            try:
                with open(rotas[self.path], "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "Arquivo não encontrado.")
            return

        elif self.path == "/filmes":
            arquivo = "filme.json"
            if os.path.exists(arquivo):
                try:
                    with open(arquivo, "r", encoding="utf-8") as f:
                        filmes = json.load(f)
                except json.JSONDecodeError:
                    filmes = []
            else:
                filmes = []
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(filmes, ensure_ascii=False, indent=4).encode("utf-8"))
            return
      
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(body)

        if self.path == "/send_login":
            login = form_data.get("email", [""])[0]
            try:
                password = int(form_data.get("password", [""])[0])
            except (ValueError, TypeError):
                password = 0

            logou = self.accont_user(login, password)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(logou.encode("utf-8"))

        elif self.path == "/cadastroFilme":
            filme = {
                "nomeFilme": form_data.get("nomeFilme", [""])[0],
                "atores": form_data.get("atores", [""])[0],
                "diretor": form_data.get("diretor", [""])[0],
                "ano": form_data.get("ano", [""])[0],
                "genero": form_data.get("genero", [""])[0],
                "produtora": form_data.get("produtora", [""])[0],
                "sinopse": form_data.get("sinopse", [""])[0],
            }

            arquivo = "filme.json"
            if os.path.exists(arquivo):
                try:
                    with open(arquivo, "r", encoding="utf-8") as f:
                        filmes = json.load(f)
                except json.JSONDecodeError:
                    filmes = []
                filmes.append(filme)
            else:
                filmes = [filme]

            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump(filmes, f, ensure_ascii=False, indent=4)

            self.send_response(303)
            self.send_header("Location", "/listarFilme")
            self.end_headers()

        else:
            self.send_error(404, "Rota POST não encontrada")

def main():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Servidor rodando em http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    main()