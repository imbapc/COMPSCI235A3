from flask import Blueprint, render_template

import Movie_Web_App.utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        popular_movies=utilities.get_popular_movies(),
        recent_movies=utilities.get_recent_movies(),
        random_movies=utilities.get_random_movie(3)
    )
