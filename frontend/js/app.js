const API_URL = "http://127.0.0.1:8000/pontos-coleta/";

const listaPontos = document.getElementById("listaPontos");
const buscaNome = document.getElementById("buscaNome");
const buscaBairro = document.getElementById("buscaBairro");
const botaoBuscar = document.getElementById("botaoBuscar");
const modalDetalhes = document.getElementById("modalDetalhes");
const conteudoDetalhes = document.getElementById("conteudoDetalhes");
const fecharModal = document.getElementById("fecharModal");

async function carregarPontos() {
    try {
        listaPontos.innerHTML = `
            <p class="mensagem-inicial">
                Carregando pontos de coleta...
            </p>
        `;

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Erro ao buscar os pontos");
        }

        const pontos = await response.json();

        mostrarPontos(pontos);

    } catch (error) {
        console.error(error);

        listaPontos.innerHTML = `
            <p class="mensagem-inicial">
                Não foi possível carregar os pontos de coleta.
            </p>
        `;
    }
}


function mostrarPontos(pontos) {

    if (pontos.length === 0) {
        listaPontos.innerHTML = `
            <p class="mensagem-inicial">
                Nenhum ponto de coleta encontrado.
            </p>
        `;

        return;
    }

    listaPontos.innerHTML = "";

    pontos.forEach((ponto) => {

        const card = document.createElement("div");

        card.classList.add("card-ponto");

        card.innerHTML = `
            <h3>${ponto.nome}</h3>

            <p>
                <strong>📍 Endereço:</strong>
                ${ponto.endereco}
            </p>

            <p>
                <strong>🏘️ Bairro:</strong>
                ${ponto.bairro}
            </p>

            <p>
                <strong>🕒 Horário:</strong>
                ${ponto.horario || "Não informado"}
            </p>

            <button onclick="verDetalhes(${ponto.id})">
                Ver detalhes
            </button>
        `;

        listaPontos.appendChild(card);
    });
}


async function buscarPontos() {

    const nome = buscaNome.value.trim();
    const bairro = buscaBairro.value.trim();

    const params = new URLSearchParams();

    if (nome) {
        params.append("nome", nome);
    }

    if (bairro) {
        params.append("bairro", bairro);
    }

    const url = params.toString()
        ? `${API_URL}?${params.toString()}`
        : API_URL;

    try {

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Erro ao buscar pontos");
        }

        const pontos = await response.json();

        mostrarPontos(pontos);

    } catch (error) {

        console.error(error);

        listaPontos.innerHTML = `
            <p class="mensagem-inicial">
                Ocorreu um erro durante a busca.
            </p>
        `;
    }
}


botaoBuscar.addEventListener("click", buscarPontos);


async function verDetalhes(id) {

    try {
        const response = await fetch(
            `${API_URL}${id}/detalhes`
        );

        if (!response.ok) {
            throw new Error("Erro ao buscar detalhes");
        }

        const ponto = await response.json();

        const materiais = ponto.materiais.length > 0
            ? ponto.materiais.map(material => `
                <li>${material.nome}</li>
            `).join("")
            : "<li>Nenhum material informado.</li>";

        conteudoDetalhes.innerHTML = `
            <h2 class="detalhes-titulo">
                ${ponto.nome}
            </h2>

            <p class="detalhe-item">
                <strong>📍 Endereço:</strong>
                ${ponto.endereco}
            </p>

            <p class="detalhe-item">
                <strong>🏘️ Bairro:</strong>
                ${ponto.bairro}
            </p>

            <p class="detalhe-item">
                <strong>🕒 Horário:</strong>
                ${ponto.horario || "Não informado"}
            </p>

            <div class="detalhe-item">
                <strong>♻️ Materiais aceitos:</strong>

                <ul class="materiais-lista">
                    ${materiais}
                </ul>
            </div>
        `;

        modalDetalhes.classList.add("ativo");

    } catch (error) {

        console.error(error);

        alert("Não foi possível carregar os detalhes.");
    }
}

fecharModal.addEventListener("click", () => {
    modalDetalhes.classList.remove("ativo");
});


modalDetalhes.addEventListener("click", (event) => {

    if (event.target === modalDetalhes) {
        modalDetalhes.classList.remove("ativo");
    }

});

carregarPontos();