import csv
import os
from abc import ABC
from datetime import date, datetime
from typing import List
from bisect import bisect, bisect_left, insort_left
from werkzeug.security import generate_password_hash
from collections import OrderedDict

from Movie_Web_App.adapters.repository import AbstractRepository, RepositoryException
from Movie_Web_App.datafilereaders.MovieFileCSVReader import MovieFileCSVReader

from Movie_Web_App.domainmodel.Model import Movie, Actor, Director, Genre, User, Review
from Movie_Web_App.utilities import services


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = list()
        self._users = list()
        self._genres = list()
        self._directors = list()
        self._reviews = list()
        self._actors = list()
        self._movie_popularity = OrderedDict()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username.lower()), None)

    def add_actor(self, actor_full_name: str):
        self._actors.append(actor_full_name)

    def get_actor(self, actor_full_name: str) -> Actor:
        return next((actor for actor in self._actors if actor.actor_full_name == actor_full_name), None)

    def add_director(self, director: Director):
        self._directors.append(director)

    def get_director(self, director_full_name: str) -> Director:
        return next((director for director in self._directors if director.director_full_name == director_full_name),
                    None)

    def add_movie(self, movie: Movie):
        self._movies.append(movie)
        self._movie_popularity[movie] = 0

    def get_movie(self, target_movie: Movie) -> Movie:
        return next((movie for movie in self._movies if movie == target_movie), None)

    def get_movie_by_time(self) -> list:
        return self._movies

    def get_movie_by_id(self, movie_id: int):
        return next((movie for movie in self._movies if movie.id == movie_id), None)

    def get_movie_by_popularity(self) -> list:
        return [k for k in self._movie_popularity]

    def add_movie_popularity(self, movie: Movie):
        self._movie_popularity[movie] += 1
        self._movie_popularity = OrderedDict(sorted(self._movie_popularity.items(), key=lambda item: item[1],
                                                    reverse=True))

    def get_movie_list(self) -> list:
        return self._movies

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def get_genre(self, genre_name: str) -> Genre:
        return next((genre for genre in self._genres if genre.genre_name == genre_name), None)

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_review(self, movie: Movie) -> list:
        result_list = list()
        for review in self._reviews:
            if review.movie == movie:
                result_list.append(review)
        return result_list


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            data_row[1],
            generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        review = Review(repo.get_movie_by_id(int(data_row[1])), data_row[2], data_row[3], users[data_row[4]])
        review._timestamp = data_row[5]
        services.add_review(repo, review.review_text, review.movie, review.rating, review.user)


def populate(data_path: str, repo: MemoryRepository):
    file_data = MovieFileCSVReader(data_path)
    file_data.read_csv_file()
    for movie in file_data.dataset_of_movies:
        repo.add_movie(movie)
    for actor in file_data.dataset_of_actors:
        repo.add_actor(actor)
    for director in file_data.dataset_of_directors:
        repo.add_director(director)
    for genre in file_data.dataset_of_genres:
        repo.add_genre(genre)

    users = load_users(data_path, repo)
    load_comments(data_path, repo, users)
