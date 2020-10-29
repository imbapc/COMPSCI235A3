from datetime import date

import pytest

from Movie_Web_App.domainmodel.Model import Movie, User, Director, Actor, Genre, Review


@pytest.fixture()
def movie():
    movie = Movie("Project X", 2012)
    movie.id = 1
    movie.director = Director("Mike John")
    movie.runtime_minutes = 120
    movie.description = "abcdefg"
    return movie


@pytest.fixture()
def actor():
    return Actor("Mike Smith")


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def review():
    return Review(Movie("Project X", 2012), "A nice Movie", 7 ,User('dbowie', '1234567890'))


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie>'

    for review in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie, actor):
    assert movie.id == 1
    assert movie.title == 'Project X'
    assert movie.year == 2012
    assert movie.runtime_minutes == 120
    assert movie.description == "abcdefg"
    movie.actors.append(actor)
    assert actor in movie.actors
    assert len(movie.reviews) == 0

    assert repr(movie) == '<Movie Project X, 2012>'


def test_movie_less_than_operator():
    movie_1 = Movie("Project X", 2012)

    movie_2 = Movie("ABC", 2018)

    movie_3 = Movie("Project X", 2019)

    assert movie_2 < movie_1 < movie_3


def test_get_picture(movie):
    picture = movie.picture

    assert picture == "https://m.media-amazon.com/images/M/MV5BMTc1MTk0Njg4OF5BMl5BanBnXkFtZTcwODc0ODkyNw@@._V1_SX300.jpg"


def test_actor(actor):
    assert actor.actor_full_name == "Mike Smith"
    assert repr(actor) == '<Actor Mike Smith>'

    for movie in actor.act_movie:
        # actors should have an empty list of act_movie after construction.
        assert False


def test_review(review, movie, user):
    assert review.user == user
    assert review.movie == movie
    assert review.review_text == "A nice Movie"
    assert review.rating == 7