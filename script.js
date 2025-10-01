const lis = document.querySelector('#lista-filmes'); // ond vai listar os filmes

// carregar api
function carregarFilmes() {
  fetch('/filmes') 
    .then(res => res.json())
    .then(data => {
      if (!lis) return; 
      lis.innerHTML = ""; 
      data.forEach(filme => {
        lis.innerHTML += `
          <li>
            <strong>${filme.nomeFilme}</strong> (${filme.ano})<br>
            <em>${filme.genero} - Diretor: ${filme.diretor}</em><br>
            <button class="btnEditar" onclick="editarFilme(${filme.id})">Editar</button>
            <form method="POST" action="/deletarFilme" style="display:inline;">
              <input type="hidden" name="id" value="${filme.id}">
              <button type="submit" class="btnDelete">Excluir</button>
            </form>
          </li>
        `;
      });
    });
}

// função que redireciona para a página de edição
function editarFilme(id) {
  window.location.href = "/editarFilme?id=" + id;
}

carregarFilmes(); 


const params = new URLSearchParams(window.location.search);
const filmeId = params.get("id"); 

fetch("/filmes")
  .then(res => res.json())
  .then(data => {
    const filme = data.find(f => f.id == filmeId); // buscar o filme pelo id
    if (filme) { 
      document.getElementById("id").value = filme.id;
      document.getElementById("nomeFilme").value = filme.nomeFilme;
      document.getElementById("atores").value = filme.atores;
      document.getElementById("diretor").value = filme.diretor;
      document.getElementById("ano").value = filme.ano;
      document.getElementById("genero").value = filme.genero;
      document.getElementById("produtora").value = filme.produtora;
      document.getElementById("sinopse").value = filme.sinopse;
    }
  });
