from datetime import date

import pytest

from Movie_Web_App.authentication.services import AuthenticationException
from Movie_Web_App.domainmodel.Model import Review, Director, Movie
from Movie_Web_App.utilities import services
from Movie_Web_App.utilities.utilities import utilities_blueprint
from Movie_Web_App.authentication import services as auth_services


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_comment(in_memory_repo):
    movie_id = 3
    review_text = 'This is a good movie to see with your friends'
    username = 'fmercury'
    print(in_memory_repo.get_movie_by_id(movie_id))
    # Call the service layer to add the comment.
    review = Review(in_memory_repo.get_movie_by_id(movie_id), review_text, 7, in_memory_repo.get_user(username))
    services.add_review(in_memory_repo, review_text, in_memory_repo.get_movie_by_id(movie_id), 7, in_memory_repo.get_user(username))

    # Retrieve the comments for the article from the repository.
    review_as_list = services.get_reviews(in_memory_repo, movie_id)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (review_element for review_element in review_as_list if review_element == review),
        None) is not None


def test_cannot_add_comment_for_non_existent_movie(in_memory_repo):
    movie_id = 1001
    review_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(services.NonExistentMovieException):
        services.add_review(in_memory_repo, review_text, in_memory_repo.get_movie_by_id(movie_id), 7, in_memory_repo.get_user(username))


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(services.UnknownUserException):
        services.add_review(in_memory_repo, review_text, in_memory_repo.get_movie_by_id(movie_id), 7, in_memory_repo.get_user(username))


def test_can_get_movie_by_id(in_memory_repo):
    movie_id = 1

    movie = services.get_movie_by_id(movie_id, in_memory_repo)

    assert movie.title == "Guardians of the Galaxy"
    assert movie.id == movie_id
    assert movie.year == 2014
    assert movie.runtime_minutes == 121
    assert movie.director == Director("James Gunn")


def test_can_get_movie(in_memory_repo):
    movie = Movie("Guardians of the Galaxy", 2014)
    result_movie = services.get_movie(in_memory_repo, movie.title, movie.year)

    assert result_movie.id == 1
    assert result_movie.title == "Guardians of the Galaxy"
    assert result_movie.year == 2014
    assert result_movie.director == Director("James Gunn")
    assert result_movie.runtime_minutes == 121


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 1002

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(services.NonExistentMovieException):
        services.get_movie_by_id(movie_id, in_memory_repo)


def test_get_review_for_movie(in_memory_repo):
    review_as_list = services.get_reviews(in_memory_repo, 1)

    # Check that 3 comments were returned for movie with id 1.
    assert len(review_as_list) == 3


def test_get_comments_for_non_existent_article(in_memory_repo):
    with pytest.raises(services.NonExistentMovieException):
        review_as_list = services.get_reviews(in_memory_repo, 1002)


def test_get_comments_for_article_without_comments(in_memory_repo):
    reviews_as_list = services.get_reviews(in_memory_repo, 5)
    assert len(reviews_as_list) == 0

