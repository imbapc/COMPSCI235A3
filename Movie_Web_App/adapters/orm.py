from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from Movie_Web_App.domainmodel import Model

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
    Column('movie_id', ForeignKey('movies.id')),
    Column('review', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('user_id', ForeignKey('users.id')),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('year', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('popularity', Integer, default=0),
    Column('director', ForeignKey('directors.name'))
)


def map_model_to_tables():
    mapper(Model.User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_reviews': relationship(Model.Review, backref='_user')
    })
    mapper(Model.Review, reviews, properties={
        '_review': reviews.c.review,
        '_timestamp': reviews.c.timestamp,
        '_rating': reviews.c.rating
    })
    movie_mapper = mapper(Model.Movie, movies, properties={
        '_id': movies.c.id,
        '_year': movies.c.year,
        '_title': movies.c.title,
        '_director': movies.c.director,
        '_Reviews': relationship(Model.Review, backref='_reviews')})

    actor_mapper = mapper(Model.Actor, actors, properties={
        '_name': actors.c.name
    })

    mapper(Model.Director, directors, properties={
        '_name': directors.c.name
    })
