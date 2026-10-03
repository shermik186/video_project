from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Table, ForeignKey


Base = declarative_base()


movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    relative_path = Column(String, nullable=False,unique=True)
    filename = Column(String, nullable=False)

    genres = relationship("Genre", secondary=movie_genres,back_populates="films")

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    films = relationship("Movie",secondary=movie_genres, back_populates="genres")

