carregarPokemons();
let pokemonsNaTela = [];

document.getElementById("filtroTipo")
    .addEventListener("change", filtrarPorTipo);

document.getElementById("btnBuscar")
    .addEventListener("click", buscarPokemon);

document.getElementById("btnVoltar")
    .addEventListener("click", carregarPokemons);

document.getElementById("inputBusca")
    .addEventListener("keypress", function (e) {
        if (e.key === "Enter") buscarPokemon();
    });

function mostrarLoader(mostrar) {
    document.getElementById("loader").style.display = mostrar ? "block" : "none";
}

function carregarPokemons() {
    mostrarLoader(true);

    fetch("http://127.0.0.1:5000/poke/pokemons")
        .then(res => res.json())
        .then(pokemons => {
            pokemonsNaTela = pokemons;
            renderizarLista(pokemonsNaTela);
            document.getElementById("btnVoltar").style.display = "none";
        })
        .finally(() => mostrarLoader(false));
}

function buscarPokemon() {
    console.log("BUSCAR FOI CHAMADO");
    const nome = document.getElementById("inputBusca").value.trim().toLowerCase();
    if (!nome) return;

    mostrarLoader(true);

    fetch("http://127.0.0.1:5000/poke/buscar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pokemon: nome })
    })
        .then(res => {
            if (!res.ok) throw new Error();
            return res.json();
        })
        .then(pokemon => {

            const jaExiste = pokemonsNaTela.find(p => p.id === pokemon.id);

            if (!jaExiste) {
                pokemonsNaTela.unshift(pokemon);
                renderizarLista(pokemonsNaTela);
            }

        })
        .catch(() => {
            alert("Pokémon não encontrado!");
        })
        .finally(() => mostrarLoader(false));
}

function filtrarPorTipo() {

    const tipo = document.getElementById("filtroTipo").value;
    if (!tipo) return;

    mostrarLoader(true);

    fetch("http://127.0.0.1:5000/poke/tipo", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ tipo: tipo })
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(lista => {

        const container = document.getElementById("listaFiltro");
        container.innerHTML = "";

        lista.forEach(pokemon => {

            const card = document.createElement("div");
            card.classList.add("cartao-pokemon");
            card.classList.add(`tipo-${pokemon.tipos[0]}`);

            card.innerHTML = `
                <h3>${pokemon.nome}</h3>
                <img src="${pokemon.imagem}" width="100">
            `;

            card.style.cursor = "pointer";

            card.addEventListener("click", () => {

                const jaExiste = pokemonsNaTela.find(p => p.id === pokemon.id);

                if (!jaExiste) {
                    pokemonsNaTela.unshift(pokemon);
                    renderizarLista(pokemonsNaTela);
                }

                document.getElementById("modalFiltro")
                    .classList.add("hidden");
            });

            container.appendChild(card);
        });

        document.getElementById("modalFiltro")
            .classList.remove("hidden");

        document.getElementById("filtroTipo").value = "";

    })
    .catch(() => {
        alert("Tipo não encontrado");
    })
    .finally(() => {
        mostrarLoader(false);
    });
}



function renderizarLista(pokemons) {
    const container = document.getElementById("cartoes");
    container.innerHTML = "";

    pokemons.forEach(pokemon => {
        const card = criarCard(pokemon);
        container.appendChild(card);
    });
}

function criarCard(pokemon) {
    const div = document.createElement("div");
    div.classList.add("cartao-pokemon");
    div.classList.add(`tipo-${pokemon.tipos[0]}`);

    div.innerHTML = `
        <div class="cartao-topo">
            <div class="detalhes">
                <h2>${pokemon.nome}</h2>
                <span>#${String(pokemon.id).padStart(3, "0")}</span>
            </div>

            <img src="${pokemon.imagem}" alt="${pokemon.nome}">
            <span class="tipo">${pokemon.tipos.join(", ")}</span>

            <button class="btn-remover">Remover</button>
        </div>
    `;

    div.addEventListener("click", (e) => {
        if (!e.target.classList.contains("btn-remover")) {
            abrirModal(pokemon);
        }
    });

    div.querySelector(".btn-remover")
        .addEventListener("click", () => removerPokemon(pokemon.id));

    return div;
}

function removerPokemon(id) {
    pokemonsNaTela = pokemonsNaTela.filter(p => p.id !== id);
    renderizarLista(pokemonsNaTela);
}

function abrirModal(pokemon) {
    const modal = document.getElementById("modal");
    const modalContent = document.querySelector(".modal-content");
    const body = document.getElementById("modalBody");

    modalContent.className = "modal-content";

    modalContent.classList.add(`tipo-${pokemon.tipos[0]}`);

    body.innerHTML = `
        <h2>${pokemon.nome}</h2>
        <img src="${pokemon.imagem}" width="150">
        <p>HP: ${pokemon.stats.hp}</p>
        <p>Ataque: ${pokemon.stats.attack}</p>
        <p>Defesa: ${pokemon.stats.defense}</p>
        <p>Velocidade: ${pokemon.stats.speed}</p>
        <p>Altura: ${pokemon.altura}</p>
        <p>Peso: ${pokemon.peso}</p>
    `;

    modal.classList.remove("hidden");
}

document.getElementById("fecharModal")
    .addEventListener("click", () => {
        document.getElementById("modal").classList.add("hidden");
    });

document.getElementById("fecharFiltro")
.addEventListener("click", () => {
    document.getElementById("modalFiltro")
        .classList.add("hidden");
});
