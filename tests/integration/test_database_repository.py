from Movie_Web_App.adapters.database_repository import SqlAlchemyRepository
from Movie_Web_App.domainmodel.Model import User, Movie, Director, Review, Actor, Genre
import Movie_Web_App.utilities.services as services


def test_repository_can_add_a_user(session_factory):
    in_memory_repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(session_factory):
    in_memory_repo = SqlAlchemyRepository(session_factory)
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    in_memory_repo = SqlAlchemyRepository(session_factory)
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(session_factory):
    in_memory_repo = SqlAlchemyRepository(session_factory)
    number_of_movies = len(in_memory_repo.get_movie_list())

    # Check that the query returned 1000 Movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(session_factory):
    in_memory_repo = SqlAlchemyRepository(session_factory)
    movie = Movie("ABC", 2020)
    movie.title = "ABC"
    movie.id = 1001
    movie.director = Director("Bob Smith").director_full_name
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie_by_id(1001) is movie


def test_repository_can_retrieve_movie(session_factory):
    in_memory_repo = SqlAlchemyRepository(session_factory)
    movie = in_memory_repo.get_movie_by_id(1)
    print(movie)

    # Check that the Movie has the expected title.
    assert movie.title == "Guardians of the Galaxy"

def test_repository_does_not_retrieve_a_non_existent_article(session_factory):
    in_memory_repo = SqlAlchemyRepository(session_factory)
    movie = in_memory_repo.get_movie_by_id(1002)
    assert movie is None

