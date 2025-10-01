import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json

class MyHandle(SimpleHTTPRequestHandler):
    # checa login do usuário
    def accont_user(self, login, password):
        loga = "fer@gmail.com"
        senha = 1234
        return "Usuário Logado" if login == loga and senha == password else "Usuário não existe"

    #  GET
    def do_GET(self):
       
        rotas = {
            "/": "index.html",
            "/login": "login.html",
            "/cadastroFilme": "cadastroFilme.html",
            "/listarFilme": "listarFilme.html",
            "/editarFilme": "editarFilme.html"
        }

        #abrir rota no html se existir
        if self.path.split("?")[0] in rotas:
            try:
                with open(rotas[self.path.split("?")[0]], "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "Arquivo não encontrado.")
            return

        # rota de API para filmes com json
        elif self.path.startswith("/filmes"):
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

    # trata requisições POST
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(body)

        # login
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

        # cadastro de filme
        elif self.path == "/cadastroFilme":
            arquivo = "filme.json"
            if os.path.exists(arquivo):
                try:
                    with open(arquivo, "r", encoding="utf-8") as f:
                        filmes = json.load(f)
                except json.JSONDecodeError:
                    filmes = []
            else:
                filmes = []

            # pega dados do form
            filme = {
                "id": len(filmes) + 1,
                "nomeFilme": form_data.get("nomeFilme", [""])[0],
                "atores": form_data.get("atores", [""])[0],
                "diretor": form_data.get("diretor", [""])[0],
                "ano": form_data.get("ano", [""])[0],
                "genero": form_data.get("genero", [""])[0],
                "produtora": form_data.get("produtora", [""])[0],
                "sinopse": form_data.get("sinopse", [""])[0],
            }

            filmes.append(filme)

            # salva no JSON
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump(filmes, f, ensure_ascii=False, indent=4)

            # redireciona pra lista
            self.send_response(303)
            self.send_header("Location", "/listarFilme")
            self.end_headers()

        # editar filme
        elif self.path == "/editarFilme":
            filme_id = int(form_data.get("id", [0])[0])
            arquivo = "filme.json"
            if os.path.exists(arquivo):
                with open(arquivo, "r", encoding="utf-8") as f:
                    filmes = json.load(f)
            else:
                filmes = []

            # atualiza campos
            for filme in filmes:
                if filme["id"] == filme_id:
                    filme["nomeFilme"] = form_data.get("nomeFilme", [filme["nomeFilme"]])[0]
                    filme["atores"] = form_data.get("atores", [filme["atores"]])[0]
                    filme["diretor"] = form_data.get("diretor", [filme["diretor"]])[0]
                    filme["ano"] = form_data.get("ano", [filme["ano"]])[0]
                    filme["genero"] = form_data.get("genero", [filme["genero"]])[0]
                    filme["produtora"] = form_data.get("produtora", [filme["produtora"]])[0]
                    filme["sinopse"] = form_data.get("sinopse", [filme["sinopse"]])[0]
                    break

            # salva alterações
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump(filmes, f, ensure_ascii=False, indent=4)

            # redireciona pra lista
            self.send_response(303)
            self.send_header("Location", "/listarFilme")
            self.end_headers()

        # deletar filme
        elif self.path == "/deletarFilme":
            filme_id = int(form_data.get("id", [0])[0])
            arquivo = "filme.json"
            if os.path.exists(arquivo):
                with open(arquivo, "r", encoding="utf-8") as f:
                    filmes = json.load(f)
            else:
                filmes = []

            filmes = [f for f in filmes if f["id"] != filme_id]

            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump(filmes, f, ensure_ascii=False, indent=4)

            # redireciona pra lista
            self.send_response(303)
            self.send_header("Location", "/listarFilme")
            self.end_headers()

        else:
            self.send_error(404, "Rota POST não encontrada")

# inicia o servidor
def main():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Servidor rodando em http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
