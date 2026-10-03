from fastapi import FastAPI

from crud import load_genres, get_all_movies

app = FastAPI()


@app.get("/genres")
def get_all_genres():
    return load_genres()

@app.get("/movies")
def get_films(genres:list = None):
    if not genres:
        return get_all_movies()

