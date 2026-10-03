from models import Movie, Genre, movie_genres
from schemas import MoviesInput, MovieInput
from database import engine
from genres import GENRES


from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import delete, select
import logging
import asyncio

logger = logging.getLogger(__name__)
handler = logging.FileHandler("video.log", mode="a", encoding="utf-8")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def add_movie(session, movie: MovieInput):
    genres_list = []
    for genre in movie.genres:
        result = session.query(Genre).filter_by(name=genre).first()
        if result is not None:
            genres_list.append(result)
        else:
            logger.error(f"Genre {genre} does not exist")

    new_movie = Movie(
        title=movie.title,
        relative_path=movie.relative_path,
        filename=movie.filename,
        genres=genres_list,
    )
    session.add(new_movie)
    try:
        session.commit()
        logger.info(f"Movie{movie.title} was successfully added")
    except IntegrityError:
        logger.error(f"Movie already exists:{movie.title}")
        session.rollback()


def add_movies(movies: MoviesInput):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        for movie in movies.items:
            add_movie(session, movie)


def fill_genres():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        for genre in GENRES:
            exists = session.query(Genre).filter_by(name=genre).first()
            if not exists:
                new_genre = Genre(name=genre)
                session.add(new_genre)
        session.commit()


def load_genres():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        genres = session.query(Genre).all()
        names = [genre.name for genre in genres]
        return names


def create_set_of_relative_pathes():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        arr = session.query(Movie.relative_path).all()
    return {row[0] for row in arr}


def delete_database():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.execute(delete(movie_genres))
        session.execute(delete(Movie))
        session.commit()
    return True


def get_all_movies():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        movies = session.query(Movie).options(selectinload(Movie.genres)).all()
    movies = unpack_movies(movies)
    return movies


def get_genres_ids(genres_names):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        genres = []
        for genre in genres_names:
            genres.append(session.query(Genre).filter_by(name=genre).first().id)
    return genres


def search_movies(genres_name: list | None = None, title: str | None = None):
    if genres_name is None:
        genres_name = []

    Session = sessionmaker(bind=engine)
    with Session() as session:

        genres = get_genres_ids(genres_name)

        stmt = select(Movie).options(
            selectinload(Movie.genres),
        )

        for genre_id in genres:
            stmt = stmt.where(Movie.genres.any(Genre.id == genre_id))

        if title:
            stmt = stmt.where(Movie.title.ilike(f"%{title}%"))

        movies = session.scalars(stmt).all()
        movies = unpack_movies(movies)
        return movies


def unpack_movies(movies):
    output = []
    for movie in movies:
        output.append(
            {
                "id": movie.id,
                "title": movie.title,
                "relative_path": movie.relative_path,
                "filename": movie.filename,
                "genres": [genre.name for genre in movie.genres],
            }
        )

    return output
