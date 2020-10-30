from Movie_Web_App.domainmodel.Model import User, Movie, Director, Review, Actor, Genre
import Movie_Web_App.utilities.services as services


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = len(in_memory_repo.get_movie_list())

    # Check that the query returned 6 Articles.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("ABC", 2020)
    movie.id = 1001
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie_by_id(1001) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie_by_id(1)

    # Check that the Movie has the expected title.
    assert movie.title == "Guardians of the Galaxy"

    # Check that the Movie is reviewed as expected.
    review_one = [review for review in movie.reviews if review.review_text == 'This is a good movie'][
        0]
    review_two = [review for review in movie.reviews if review.review_text == 'It is funny'][0]

    assert review_one.user.username == 'fmercury'
    assert review_two.user.username == "thorke"


def test_repository_does_not_retrieve_a_non_existent_article(in_memory_repo):
    movie = in_memory_repo.get_movie_by_id(1002)
    assert movie is None


def test_repository_can_add_actor(in_memory_repo):
    actor = Actor("ABC DEF")
    in_memory_repo.add_actor(actor)

    assert in_memory_repo.get_actor('ABC DEF') is actor


def test_repository_can_retrieve_actor(in_memory_repo):
    actor = in_memory_repo.get_actor("Chris Pratt")
    assert actor == Actor("Chris Pratt")


def test_repository_can_add_director(in_memory_repo):
    director = Director("XYZ QWE")
    in_memory_repo.add_director(director)

    assert in_memory_repo.get_director('XYZ QWE') is director


def test_repository_can_retrieve_director(in_memory_repo):
    director = in_memory_repo.get_director("James Gunn")
    assert director == Director("James Gunn")


def test_repository_can_add_genres(in_memory_repo):
    genre = Genre("mnb")
    in_memory_repo.add_genre(genre)

    assert in_memory_repo.get_genre("mnb") is genre


def test_repository_can_retrieve_genres(in_memory_repo):
    genre = in_memory_repo.get_genre("Action")
    assert genre == Genre("Action")


def test_repository_can_add_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie_by_id(2)
    review = Review(movie, 'this is a nice movie', 8, user)

    services.add_review(in_memory_repo, review.review_text, review.movie, review.rating, review.user)

    assert review in in_memory_repo.get_review(movie)


def test_repository_can_retrieve_review(in_memory_repo):
    movie = in_memory_repo.get_movie_by_id(1)
    result_list = in_memory_repo.get_review(movie)
    assert len(result_list) == 3
