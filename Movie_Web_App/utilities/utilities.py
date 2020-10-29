from flask import Blueprint, request, render_template, redirect, url_for, session

import Movie_Web_App.adapters.repository as repo
import Movie_Web_App.utilities.services as services

# Configure Blueprint.
from Movie_Web_App.domainmodel.Model import Movie, Actor, Director

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_movie(title: str, year: int) -> Movie:
    return services.get_movie(repo.repo_instance, title, year)


def find_movie(data: str, category: str) -> Movie:
    target_list = services.get_movie_list(repo.repo_instance)
    result = list()
    if category == "Movie":
        for movie in target_list:
            if movie.title == data:
                result.append(movie)

    if category == "Actor":
        for movie in target_list:
            if data in movie.actors:
                result.append(movie)

    if category == "Genres":
        for movie in target_list:
            if data in movie.genres:
                result.append(movie)

    if category == "Director":
        for movie in target_list:
            if data == movie.director:
                result.append(movie)
    return result


def get_popular_movies():
    return services.get_popular_movies(repo.repo_instance)


def get_recent_movies():
    return services.get_recent_movies(repo.repo_instance)


def get_actor(actor_full_name: str) -> Actor:
    return services.get_actor(repo.repo_instance, actor_full_name)


def get_director(director_full_name: str) -> Director:
    return services.get_director(repo.repo_instance, director_full_name)


def add_popularity(movie: Movie):
    return services.add_popularity(repo.repo_instance, movie)


def get_random_movie(quantity: int):
    return services.get_random_movie(repo.repo_instance, quantity)


def get_reviews(movie_id: int):
    return services.get_reviews(repo.repo_instance, movie_id)


def get_user(username: str):
    return services.get_user(repo.repo_instance, username)
