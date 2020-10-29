import abc
from typing import List

from Movie_Web_App.domainmodel.Model import Movie, Actor, Director, Genre, User, Review

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, target_movie: Movie) -> Movie:
        """ Returns Movie with title from the repository.

        If there is no Movie with the given title, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_list(self) -> list:
        """Returns all movies in the database."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_popularity(self):
        """ Returns a list of Movies with there popularity(times being clicked)."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_id(self, movie_id: int):
        """ Returns a Movie by its movie_id"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie_popularity(self, movie: Movie):
        """ Add popularity of a Movie into the database"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_full_name: str) -> Actor:
        """ Returns Actor with full name from the repository.

        If there is no Actor with the given full name, this method returns None.
                """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor_full_name: str):
        """ Adds an actor to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_full_name: str) -> Director:
        """ Returns director with full name from the repository.

        If there is no director with the given full name, this method returns None."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a director to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a review to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, genre_name: str) -> Genre:
        """Returns genre with genre name from the repository.

        If there is no genre with the given genre name, this method returns None"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self, movie: Movie) -> list:
        """ Returns review with review text from the repository.

        If there is no review with the given review text, this method returns None"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with an Movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Comment not correctly attached to an Movie')
