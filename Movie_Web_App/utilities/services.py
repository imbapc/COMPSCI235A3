import random

from Movie_Web_App.adapters.repository import AbstractRepository
from Movie_Web_App.domainmodel.Model import Movie, User, Review


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_movie(repo: AbstractRepository, title: str, year: int) -> Movie:
    return repo.get_movie(Movie(title, year))


def get_popular_movies(repo: AbstractRepository, number=5):
    return repo.get_movie_by_popularity()[0:number]


def get_recent_movies(repo: AbstractRepository, number=5):
    return repo.get_movie_by_time()[-1 - number:-1]


def get_movie_list(repo: AbstractRepository):
    return repo.get_movie_list()


def get_movie_by_id(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)
    if movie is None:
        raise NonExistentMovieException
    else:
        return movie


def get_actor(repo: AbstractRepository, actor_full_name: str):
    return repo.get_actor(actor_full_name)


def get_director(repo: AbstractRepository, director_full_name: str):
    return repo.get_director(director_full_name)


def add_review(repo: AbstractRepository, review_text: str, movie: Movie, rating: int, user: User):
    if movie is None:
        raise NonExistentMovieException
    if user is None:
        raise UnknownUserException
    review = Review(movie, review_text, rating, user)
    review.user.add_review(review)
    review.movie.reviews.append(review)
    repo.add_review(review)


def get_reviews(repo: AbstractRepository, movie_id: int):
    movie = repo.get_movie_by_id(movie_id)
    if movie is None:
        raise NonExistentMovieException
    else:
        return repo.get_review(movie)


def add_popularity(repo: AbstractRepository, movie: Movie):
    repo.add_movie_popularity(movie)


def get_random_movie(repo: AbstractRepository, quantity: int):
    movie_amount = len(repo.get_movie_list())
    if quantity >= movie_amount:
        quantity = movie_amount - 1

    random_ids = random.sample(range(1, movie_amount), quantity)
    movie_list = list()
    for id_number in random_ids:
        movie_list.append(repo.get_movie_list()[id_number])

    return movie_list


def get_user(repo: AbstractRepository, username: str):
    return repo.get_user(username)
