import csv
import os
from abc import ABC

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from Movie_Web_App.datafilereaders.MovieFileCSVReader import MovieFileCSVReader
from Movie_Web_App.domainmodel.Model import Director, Actor, User, Movie, Genre, Review
from Movie_Web_App.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, target_movie: Movie) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._id == target_movie.id).one()
        except NoResultFound:
            pass
        return movie


    def get_movie_by_id(self, movie_id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._id == movie_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_movies_by_id(self, id_list):
        movies = self._session_cm.session.query(Movie).filter(Movie._id.in_(id_list)).all()
        return movies

    def get_review(self, movie: Movie) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_comment(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_actor(self, actor_full_name: str):
        with self._session_cm as scm:
            scm.session.add(actor_full_name)
            scm.commit()

    def get_actor(self, actor_full_name: str) -> Actor:
        actor = None
        try:
            actor = self._session_cm.session.query(Actor).filtered_by(_name=actor_full_name).one()
        except NoResultFound:
            pass
        return actor

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_director(self, director_full_name: str) -> Director:
        director = None
        try:
            director = self._session_cm.session.query(Director).filtered_by(_name=director_full_name).one()
        except NoResultFound:
            pass
        return director

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genre(self, genre_name: str) -> Genre:
        genre = None
        try:
            genre = self._session_cm.session.query(Genre).filtered_by(_name=genre_name).one()
        except NoResultFound:
            pass
        return genre


def movie_record_generator(filename: str):
    file_data = MovieFileCSVReader(filename)
    return file_data.dataset_of_movies

def actor_record_generator(filename: str):
    file_data = MovieFileCSVReader(filename)
    return file_data.dataset_of_actors

def director_record_generator(filename: str):
    file_data = MovieFileCSVReader(filename)
    return file_data.dataset_of_directors

def genre_record_generator(filename: str):
    file_data = MovieFileCSVReader(filename)
    return file_data.dataset_of_genres


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    insert_movies = """
        INSERT INTO movies (
        id, year, title, director)
        VALUES (?, ?, ?, ?, )"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'Data1000Movies.csv')))

    insert_actors = """
        INSERT INTO actors(
        name)
        VALUES(?)"""
    cursor.executemany(insert_actors, actor_record_generator(data_path, 'Data1000Movies.csv'))

    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_reviews = """
        INSERT INTO comments (
        id, user_id, movie_id, review, timestamp)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_reviews, generic_generator(os.path.join(data_path, 'reviews.csv')))

    conn.commit()
    conn.close()
