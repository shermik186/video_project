from fastapi import FastAPI, Query,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crud import load_genres, search_movies,delete_film

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5000"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/genres")
def get_all_genres():
    return load_genres()

@app.get("/movies")
def get_films(genres:list[str]|None = Query(default = None), title: str|None = None,offset:int= 0,limit:int = 50):
    return search_movies(genres,title,offset,limit)

@app.delete("/movies")
def delete_movie(relative_path:str):
    if not delete_film(relative_path):
        raise HTTPException(status_code=404, detail="Film nenalezen")
    return {"deleted": relative_path}





