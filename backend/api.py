from fastapi import FastAPI, Query

from crud import load_genres, search_movies

app = FastAPI()


@app.get("/genres")
def get_all_genres():
    return load_genres()

@app.get("/movies")
def get_films(genres:list[str]|None = Query(default = None), title: str|None = None):
    return search_movies(genres)




