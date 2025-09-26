const lis = document.querySelector('#lista-filmes');

fetch('/filmes')
  .then(res => res.json())
  .then(data => {
    lis.innerHTML = "";
    data.forEach(filme => {
      lis.innerHTML += `
        <li>
          <strong>Nome: </strong> ${filme.nomeFilme}<br>
          <strong>Atores: </strong> ${filme.atores}<br>
          <strong>Diretor: </strong> ${filme.diretor}<br>
          <strong>Ano: </strong> ${filme.ano}<br>
          <strong>Gênero: </strong> ${filme.genero}<br>
          <strong>Produtora: </strong> ${filme.produtora}<br>
          <strong>Sinopse: </strong> ${filme.sinopse}<br>
        </li>
      `;
    });
  });
