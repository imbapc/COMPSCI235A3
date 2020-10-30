import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from Movie_Web_App.domainmodel.Model import User, Movie, Review, Actor, Director, Genre


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_movie(empty_session, values):
    empty_session.execute(
        'INSERT INTO articles (id, year, title, director) VALUES (:id, :year, :title, :director)',
        {'id': values.id, 'year': values.year, 'title': values.title, 'director': values.director.director_full_name}
    )
    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def insert_actors(empty_session, values):
    empty_session.execute(
        'INSERT INTO actors VALUE(:name)', {'name': values[0]}
    )
    rows = list(empty_session.execute('SELECT name from actors'))
    names = rows[0]
    return names


def insert_director(empty_session, values):
    empty_session.execute(
        'INSERT INTO directors (name) VALUE(:name)', {'name': values[0]}
    )
    rows = list(empty_session.execute('SELECT name from directors'))
    names = rows[0]
    return names


def insert_genre(empty_session, values):
    empty_session.execute(
        'INSERT INTO genres (name) VALUE (: name)', {'name': values[0]}
    )


def insert_reviewed_movie(empty_session):
    article_key = insert_movie(empty_session, Movie("ABC", 2012))
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, movie_id, review, rating, timestamp) VALUES '
        '(:user_id, :movie_id, "Comment 1", "7", :timestamp_1),'
        '(:user_id, :movie_id, "Comment 2", "5", :timestamp_2)',
        {'user_id': user_key, 'movie_id': article_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from reviews').fetchone()
    return row[0]


def make_movie():
    movie = Movie("QWE", 2000)
    movie.id = 1
    movie.director = Director("Bob Adam")
    return movie


def make_user():
    user = User("Andrew", "111")
    return user


def make_actor():
    actor = Actor("News Tim")
    return actor


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("Andrew", "111")]


def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_movie(empty_session):
    expected_article = make_movie()
    movie_key = insert_movie(empty_session, make_movie())
    fetched_article = empty_session.query(Movie).one()

    assert expected_article == fetched_article
    assert movie_key == fetched_article.id


def test_loading_of_reviewed_movie(empty_session):
    insert_reviewed_movie(empty_session)

    rows = empty_session.query(Movie).all()
    movie = rows[0]

    assert len(movie.reviews) == 2

    for review in movie.reviews:
        assert review.movie is movie


def test_saving_of_movie(empty_session):
    movie = make_movie()
    empty_session.add(movie)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, year FROM movies'))
    assert rows == [('QWE', '2000')]


