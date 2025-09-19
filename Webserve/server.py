import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class MyHandle(SimpleHTTPRequestHandler):
    filmes = []

    def _serve_html_page(self, filename):
        try:
            page_path = os.path.join(os.getcwd(), filename)
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, f"{filename} não encontrado")

    def do_GET(self):
        if self.path == "/cadastroFilme":
            self._serve_html_page("cadastroFilme.html")
        elif self.path == "/listarFilme":
            filmes_html = ""
            for filme in self.filmes:
                filmes_html += f"<li>{filme['titulo']} - {filme['genero']} - {filme['atores']} - {filme['diretor']} - {filme['produtora']} ({filme['ano']}) - {filme['sinopse']}  </li>\n"
            
            content = f"""
            <!DOCTYPE html>
            <html lang="pt-br">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Listar Filmes</title>
                <link rel="stylesheet" href="styles.css">  <!-- Certifique-se de que este arquivo existe -->
            </head>
            <body class="listar-page">
                <div class="list-container">
                    <h1>Filmes Cadastrados</h1>
                    <ul>
                        {filmes_html}
                    </ul>
                </div>
            </body>
            </html>
            """
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/cadastroFilme":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            titulo = form_data.get("titulo", [""])[0]
            atores = form_data.get("atores", [""])[0]
            diretor = form_data.get("diretor", [""])[0]
            ano = form_data.get("ano", [""])[0]
            genero = form_data.get("genero", [""])[0]
            produtora = form_data.get("produtora", [""])[0]
            sinopse = form_data.get("sinopse", [""])[0]

            self.filmes.append({
                "titulo": titulo,
                "atores": atores,
                "diretor": diretor,
                "ano": ano,
                "genero": genero,
                "produtora": produtora,
                "sinopse": sinopse
            })

            # Redireciona para listarFilme
            self.send_response(303)
            self.send_header('Location', '/listarFilme')
            self.end_headers()
        else:
            self.send_error(404, "Rota não encontrada")

def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Servidor rodando em http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    main()
