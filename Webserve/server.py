import os
from http.server import SimpleHTTPRequestHandler, HTTPServer


# manipulas requisição
class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # abrir o arquivo
            f = open(os.path.join(path, 'index.html'), 'r')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)
# manipular o get
    def do_GET(self):
        
        if self.path == "/login":
            try:
                login_path = os.path.join(os.getcwd(), "login.html")
                with open(login_path, 'r') as login:
                    content = login.read()
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "login.html Not Found")

# Caso a requisição seja para a página de cadastro de filme
        elif self.path == "/cadastroFilme":
            try:
                cadastro_path = os.path.join(os.getcwd(), "cadastroFilme.html")
                with open(cadastro_path, 'r') as cadastro:
                    content = cadastro.read()
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "cadastroFilme.html Not Found")

# Caso a requisição seja para a página de listar filmes
        elif self.path == "/listarFilme":
            try:
                listar_path = os.path.join(os.getcwd(), "listarFilme.html")
                with open(listar_path, 'r') as listar:
                    content = listar.read()
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "listarFilme.html Not Found")

        else:
            super().do_GET()

# Inicia o Servidor
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running in http://localhost:8000")
    httpd.serve_forever()

main()
