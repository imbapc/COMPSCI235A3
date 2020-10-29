from flask import Blueprint, render_template, url_for, request, session
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from better_profanity import profanity
import Movie_Web_App.utilities.utilities as utilities
import Movie_Web_App.adapters.repository as repo
from wtforms import StringField, TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError

from Movie_Web_App.utilities import services
from Movie_Web_App.authentication.authentication import login_required

movie_blueprint = Blueprint(
    'movie_bp', __name__)


@movie_blueprint.route('/<string:title>/<int:year>', methods=["GET", "POST"])
def movie(title, year):
    target_movie = utilities.get_movie(title, year)
    utilities.add_popularity(target_movie)
    review_list = utilities.get_reviews(target_movie.id)
    add_review_url = url_for('movie_bp.review_on_movie', movie_id=target_movie.id)
    return render_template('movie/movie.html', content_movie=target_movie, random_movies=utilities.get_random_movie(3),
                           review_list=review_list, add_review_url=add_review_url)


@movie_blueprint.route('/actor/<string:actor_full_name>', methods=["GET", "POST"])
def actor(actor_full_name):
    target_actor = utilities.get_actor(actor_full_name)
    return render_template('movie/actor.html', actor=target_actor, random_movies=utilities.get_random_movie(3))


@movie_blueprint.route('/director/<string:director_full_name>', methods=["GET", "POST"])
def director(director_full_name):
    target_director = utilities.get_director(director_full_name)
    return render_template('movie/director.html', director=target_director, random_movies=utilities.get_random_movie(3))


@movie_blueprint.route('/find', methods=["GET", "POST"])
def search():
    form = SearchForm(request.form)
    if form.validate():
        search_data = form.search.data
        category = request.form.get('category')
        result = utilities.find_movie(search_data, category)
        return render_template('result.html', result=result, random_movies=utilities.get_random_movie(3),)
    return render_template('searchbar.html', form=form, random_movies=utilities.get_random_movie(3),
                           )


@movie_blueprint.route('/review', methods=["GET", "POST"])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']
    user = utilities.get_user(username)

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the article id, representing the reviewed movie, from the form.
        movie_id = int(form.movie_id.data)

        # Retrieve the article in dict form.
        movie_result = services.get_movie_by_id(movie_id, repo.repo_instance)

        # Use the service layer to store the new review.
        services.add_review(repo.repo_instance, form.review.data, movie_result, form.rating.data, user)


        # Cause the web browser to display the page of all movies that have the same date as the reviewed movie,
        # and display all reviews, including the new review.
        return redirect(url_for('movie_bp.movie', title=movie_result.title, year=movie_result.year))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie_id'))

        # Store the article id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being reviewed from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    content_movie = services.get_movie_by_id(movie_id, repo.repo_instance)
    return render_template('movie/review.html', content_movie=content_movie,
                           random_movies=utilities.get_random_movie(3),
                           handler_url=url_for('movie_bp.review_on_movie'),
                           form=form)


class SearchForm(FlaskForm):
    search = StringField('search')
    submit = SubmitField('Find')


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=10, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = IntegerField("Rating")
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')
