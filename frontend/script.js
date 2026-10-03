function createDiv(film,seznam){
    const card = document.createElement("div")
    card.className = "movie-card"
    card.textContent = film.nazev
    seznam.appendChild(card)
}


const films = [{nazev: "Troya", rok: 2004}, {nazev: "Big Short", rok: 2015}]
const seznam = document.getElementById("movie-list")
films.forEach((film) => createDiv(film,seznam))

