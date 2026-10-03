from pydantic import BaseModel
from typing import List

class MovieInput(BaseModel):
    title : str
    relative_path : str
    filename : str
    genres : List[str]

class MoviesInput(BaseModel):
    items : List[MovieInput]