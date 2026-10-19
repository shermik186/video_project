const state = {
    currentPage: 0,
    limit : 50,
    total : 0,
    genres : [],
    pendingDelete:null,
    
}

function createDiv(film,seznam){
    const card = document.createElement("div")
    card.className = "movie-card"

    const title = document.createElement("h3");
    title.textContent = film.title;
    
    const genres = document.createElement("p");
    genres.textContent = film.genres.join(", ");

    const filename = document.createElement("p");
    filename.textContent = film.filename;

    const path = document.createElement("p");
    path.textContent = film.relative_path;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent="DELETE";
    deleteBtn.className="delete-btn";
    deleteBtn.addEventListener("click",()=>{
        state.pendingDelete = film.relative_path;
        document.getElementById("confirmFilmTitle").textContent=film.title;
        document.getElementById("confirmDialog").showModal()
    })



    card.append(title,genres,filename,path,deleteBtn)

    seznam.appendChild(card)
}
async function fetchData(){
    try{
        const moviesNames = document.getElementById("moviesNames").value;
        const params = new URLSearchParams();

        params.append("limit", state.limit)
        params.append("offset", state.currentPage * state.limit)

        if(moviesNames){
            params.append("title", moviesNames);
        }
        state.genres.forEach((genre)=>{
            params.append("genres",genre)
        })
        
        let url = `http://localhost:8000/movies?${params}`;

        const response = await fetch(url);

        if(!response.ok){
            throw new Error("Could not fetch resource")
        }

        const data = await response.json();
        
        state.total = data.total;   
        renderPagination();
        return data.movies;
    }
    catch(error){
        console.log(error);
    }
}

function WriteFilmsOnSite(apiResponse,seznam){
    apiResponse.forEach((film) => createDiv(film, seznam));
}

async function getData(){
    showMessage("");
    const seznam = document.getElementById("movie-list");
    const films = await fetchData();
    console.log(films)

    if (!films){
        showMessage("Nepodařilo se načíst data");
        return;
    }
    seznam.innerHTML="";
    if(films.length == 0){
        showMessage("Žádné filmy splňující podmínky vyhledávaní nebyly nalezeny");
        return;

    }
    WriteFilmsOnSite(films,seznam)
}
function nextFilms(){
    state.currentPage = state.currentPage + 1;
    getData();
}
function previousFilms(){
    state.currentPage = state.currentPage - 1;
    getData();
}

function searchButtonQuery(){
    state.currentPage = 0;
    getData();
}

function getPageNumbers(current, total) {
    // málo stránek: vrať všechny bez teček
    if (total <= 7) {
        return Array.from({ length: total }, (_, i) => i + 1);
    }

    // okno kolem aktuální stránky
    let start = current - 1;
    let end = current + 1;
    if (current === 1) end = 3;            // na začátku ukaž 1 2 3
    if (current === total) start = total - 2; // na konci ukaž poslední tři

    // sesbírej čísla, která se mají zobrazit (Set odstraní duplicity)
    const pages = new Set([1, total - 1, total]);
    for (let i = start; i <= end; i++) {
        if (i >= 1 && i <= total) pages.add(i);
    }

    const sorted = [...pages].sort((a, b) => a - b);

    // vlož "..." tam, kde chybí čísla
    const result = [];
    for (let i = 0; i < sorted.length; i++) {
        if (i > 0) {
            const gap = sorted[i] - sorted[i - 1];
            if (gap === 2) result.push(sorted[i] - 1); // chybí jediné číslo, napiš ho
            else if (gap > 2) result.push("...");
        }
        result.push(sorted[i]);
    }
    return result;
}
function renderPagination() {
    const totalPages = Math.ceil(state.total / state.limit);
    const pages = getPageNumbers(state.currentPage + 1, totalPages); // spočítá se jednou

    document.querySelectorAll(".page-numbers").forEach((container) => {
        container.replaceChildren();
        if (totalPages <= 1) return;

        for (const page of pages) {
            if (page === "...") {
                const dots = document.createElement("span");
                dots.textContent = "...";
                container.appendChild(dots);
            } else {
                const btn = document.createElement("button");
                btn.textContent = page;
                if (page === state.currentPage + 1) btn.classList.add("active");
                btn.addEventListener("click", () => {
                    state.currentPage = page - 1;
                    getData();
                });
                container.appendChild(btn);
            }
        }
    });

    document.querySelectorAll(".prev-btn").forEach((btn) => {
        btn.disabled = totalPages <= 1 || state.currentPage === 0;
    });
    document.querySelectorAll(".next-btn").forEach((btn) => {
        btn.disabled = totalPages <= 1 || state.currentPage >= totalPages - 1;
    });
}   
async function fetchGenres(){
    try{
        let url = "http://localhost:8000/genres";
        const response = await fetch(url);
        const genres = await response.json();
        console.log(genres);
        return genres;
    }
    catch(error)
    {
        console.log(error);
    }
}
function createCheckBox(genre) {
    const form = document.getElementById("genres");

    const label = document.createElement("label");

    const box = document.createElement("input");
    box.type = "checkbox";
    box.value = genre;

    label.append(box, " " + genre);

    form.appendChild(label);
}
function WriteGenresOnSite(genres){
    genres.forEach((genre)=> createCheckBox(genre));
}
async function getGenres(){
    const genres = await fetchGenres();
    console.log(genres);
    if (!genres){
        return;
    }
    WriteGenresOnSite(genres);

}

function queryGenres(){
    state.currentPage =0;
    state.genres = [];
    const genres = document.querySelectorAll("#genres input:checked");
    genres.forEach((genre)=>{
        state.genres.push(genre.value)
    })
    getData();

}
function showMessage(text){
    message = document.getElementById("showMessage");
    message.textContent = text;
}
async function deleteMovie(relativePath){
 
    const params = new URLSearchParams();
    params.append("relative_path", relativePath);

    try {
        const response = await fetch(`http://localhost:8000/movies?${params}`, {
            method: "DELETE",
        });

        if (response.ok || response.status === 404) {
            const lastPage = Math.max(0, Math.ceil((state.total - 1) / state.limit) - 1);
            state.currentPage = Math.min(state.currentPage, lastPage);
            await getData();
            if (!response.ok) {
                showMessage("Film už neexistoval, seznam byl obnoven");
            }
            return;
        }
        showMessage("Film se nepodařilo smazat");
    } catch (error) {
        console.log(error);
        showMessage("Film se nepodařilo smazat");
    }
}


document.getElementById("searchBtn").addEventListener("click",searchButtonQuery)
document.querySelectorAll(".next-btn").forEach((btn) => btn.addEventListener("click", nextFilms));
document.querySelectorAll(".prev-btn").forEach((btn) => btn.addEventListener("click", previousFilms));
document.getElementById("genres").addEventListener("change", queryGenres)
document.getElementById("confirmYes").addEventListener("click",()=>{
    console.log("ano", state.pendingDelete)
    deleteMovie(state.pendingDelete);
    state.pendingDelete = null;
    document.getElementById("confirmDialog").close()
})
document.getElementById("confirmNo").addEventListener("click",()=>{
    state.pendingDelete = null;
    document.getElementById("confirmDialog").close()
})

getGenres();
getData();

