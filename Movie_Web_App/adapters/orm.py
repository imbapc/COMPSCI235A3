from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from Movie_Web_App.domainmodel import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)


directors = Table(
    'directors', metadata,
    Column('name', String(1024), primary_key=True)
)


actors = Table(
    'actors', metadata,
    Column('name', String(1024), primary_key=True)
)


genres = Table(
    'genres', metadata,
    Column('name', String(1024), primary_key=True)
)


reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movie', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('year', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('director', ForeignKey('directors.name'))
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Review, reviews, properties={
        '_review': reviews.c.review,
        '_timestamp': reviews.c.timestamp
    })
    movie_mapper = mapper(model.Movie, movies, properties={
        '_id':movies.c.id,
        '_year': movies.c.year,
        '_title': movies.c.title,
        '_director': movies.c.director,
        '_Reviews': relationship(model.Review, backref='_reviews')
    })
