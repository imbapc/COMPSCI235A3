import re
import time
from datetime import date
import omdb


class Director:
    def __init__(self, director: str):
        if not re.search("^[a-zA-Z]+", str(director)):
            self._director = 'None'
        else:
            self._director = director
        self._movie_list = []

    @property
    def director_full_name(self) -> str:
        return self._director

    @director_full_name.setter
    def director_full_name(self, director: str):
        self._director = director

    @property
    def movie_list(self):
        return self._movie_list

    def __repr__(self):
        return f'<Director {self._director}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Director):
            return False
        return self._director == other._director

    def __lt__(self, other) -> bool:
        if not isinstance(other, Director):
            return False
        return self._director < other._director

    def __hash__(self):
        return hash(self._director)


class Genre:
    def __init__(self, genre: str):
        if genre == "":
            self._genre = "None"
        else:
            self._genre = genre

    @property
    def genre_name(self):
        return self._genre

    @genre_name.setter
    def genre_name(self, genre):
        self._genre = genre

    def __repr__(self):
        return f'<Genre {self._genre}>'

    def __eq__(self, other):
        return self._genre == other.genre_name

    def __lt__(self, other):
        return self._genre < other.genre_name

    def __hash__(self):
        return hash(self._genre)


class Actor:
    def __init__(self, name: str):
        if str(name) == "":
            self._actor_name = "None"
        else:
            self._actor_name = name
        self._act_movie = []
        self._colleague = []

    @property
    def actor_full_name(self):
        return self._actor_name

    @property
    def actor_colleague(self):
        return self._colleague

    @property
    def act_movie(self):
        return self._act_movie

    def __repr__(self) -> str:
        return f'<Actor {self._actor_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Actor):
            return False
        return self._actor_name == other._actor_name

    def __lt__(self, other) -> bool:
        if not isinstance(other, Actor):
            return False
        return self._actor_name < other._actor_name

    def __hash__(self):
        return hash(self._actor_name)

    def add_actor_colleague(self, colleague):
        self._colleague.append(colleague)

    def check_if_this_actor_worked_with(self, colleague) -> bool:
        return colleague in self._colleague


class Movie:
    
    def __init__(self, title, year):
        if title == "" or not isinstance(title, str):
            self._title = "None"
        elif year < 1900 or not isinstance(year, int):
            self._year = None
        else:
            self._title = title.strip()
            self._year = year
        self._director = None
        self._actors = []
        self._genres = []
        self._runtime_minutes = None
        self._description = ""
        self._rating = 0
        self._metascore = 0
        self._id = 0
        self._reviews = []

    def __repr__(self):
        return f'<Movie {self.title}, {self.year}>'

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        else:
            return self.title == other.title and self.year == other.year

    def __lt__(self, other):
        if not isinstance(other, Movie):
            return False
        elif self.title == other.title:
            return self._year < other.year
        else:
            return self.title < other.title

    def __hash__(self):
        return hash(self._title + str(self._year))

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, movie_rank):
        if isinstance(movie_rank, int):
            self._id = movie_rank

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, director: Director):
        if self._director == None and isinstance(director, Director):
            self._director = director

    @property
    def actors(self):
        return self._actors

    def add_actor(self, actor):
        if actor not in self._actors and str(actor) != "<Actor None>" and isinstance(actor, Actor):
            self._actors.append(actor)

    def remove_actor(self, actor):
        if actor in self._actors and str(actor) != "<Actor None>" and isinstance(actor, Actor) and not len(
                self._actors) == 0:
            self._actors.remove(actor)

    @property
    def genres(self):
        return self._genres

    def add_genre(self, genre):
        if genre not in self._genres and str(genre) != "<Genre None>" and isinstance(genre, Genre):
            self._genres.append(genre)

    def remove_genre(self, genre):
        if genre in self._genres and str(genre) != "<Genre None>" and isinstance(genre, Genre) and not len(
                self._genres) == 0:
            self._genres.remove(genre)

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, time):
        if (time < 0 or time == 0) and isinstance(time, int):
            raise ValueError("Runtime is invalid")
        else:
            self._runtime_minutes = time

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, des):
        if isinstance(des, str):
            self._description = des.strip()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str):
            self._title = title

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if isinstance(year, int):
            self._year = year

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        if isinstance(rating, float):
            self._rating = rating

    @property
    def metascore(self):
        return self._metascore

    @metascore.setter
    def metascore(self, score):
        if isinstance(score, int):
            self._metascore = score

    @property
    def picture(self):
        omdb.set_default('apikey', 'c69d8944')
        res = omdb.get(title=self._title, year=self._year)
        if "poster" in res.keys():
            return res["poster"]
        else:
            return None

    @property
    def reviews(self):
        return self._reviews


class User:
    def __init__(self, name: str, password: str):
        if not isinstance(name, str) or not isinstance(password, str):
            self._username = ""
            self._password = ""
        else:
            self._username = name.strip()
            self._password = password
        self._watched_movies = []
        self._review = []
        self._time_spent_watching_movies_minutes = 0
        self._watchlist = []

    def __repr__(self):
        return f'<User {self._username}>'

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        else:
            return self._username == other._username

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        else:
            return self._username < other._username

    def __hash__(self):
        return hash(self._username + self._password)

    def watch_movie(self, movie):
        if isinstance(movie, Movie):
            self._watched_movies.append(movie)
            self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if isinstance(review, Review) and review not in self._review:
            self._review.append(review)

    def create_watchlist(self, name=""):
        for watchlist in self._watchlist:
            if name == watchlist.name:
                return "Watchlist already exists"
        self._watchlist.append(Watchlist(name))
        Watchlist.owner = self

    def add_movie_to_watchlist(self, movie, watchlist):
        if isinstance(movie, Movie) and isinstance(watchlist, Watchlist) and watchlist.owner == self:
            watchlist.add_movie(movie)

    def save_watchlist(self, watchlist):
        if isinstance(watchlist, Watchlist) and not watchlist.privacy:
            self._watchlist.append(watchlist)

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._review

    @property
    def time_spent_watching_movies_minutes(self):
        if self._time_spent_watching_movies_minutes == 0:
            return None
        else:
            return self._time_spent_watching_movies_minutes

    @property
    def watchlist(self):
        return self._watchlist


class Watchlist:
    def __init__(self, name=""):
        self._watchlist = []
        self._name = name
        self._privacy = True
        self._owner = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, user):
        if isinstance(user, User) and self._owner is None:
            self._owner = user
            print(self.owner)

    @property
    def privacy(self):
        return self._privacy

    def add_movie(self, movie: Movie):
        if movie not in self._watchlist:
            self._watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self._watchlist:
            self._watchlist.remove(movie)

    def select_movie_to_watch(self, index):
        if index in range(0, self.size()):
            return self._watchlist[index]
        else:
            return None

    def size(self):
        return len(self._watchlist)

    def first_movie_in_watchlist(self):
        if self.size() == 0:
            return None
        else:
            return self._watchlist[0]

    def share_watchlist(self):
        self._privacy = False

    def stop_sharing(self):
        self._privacy = True

    def __repr__(self):
        return f'<Watchlist {self._name}: {self._watchlist}>'

    def __eq__(self, other):
        if not isinstance(other, Watchlist):
            return False
        else:
            return self._name == other._name

    def __lt__(self, other):
        if not isinstance(other, Watchlist):
            return False
        else:
            return self._name < other._name

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == self.size():
            raise StopIteration
        else:
            self._index += 1
            return self._watchlist[self._index - 1]


class Review:
    def __init__(self, movie: Movie, review: str, rating: int, user: User):
        if rating in range(1, 11) and isinstance(rating, int):
            self._rating = rating
        else:
            self._rating = None
        self._review = review
        self._movie = movie
        self._timestamp = time.time()
        self._user = user

    @property
    def movie(self):
        return self._movie

    @property
    def review_text(self):
        return self._review

    @property
    def rating(self):
        return self._rating

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def human_time(self):
        return date.fromtimestamp(self._timestamp)

    @property
    def user(self):
        return self._user

    @property
    def username(self):
        return str(self._user)

    def __repr__(self):
        return f'<Review {self.movie},{self.review_text}, {self.rating}, {self.user}>'

    def __eq__(self, other):
        return self._movie == other.movie and self._review == other.review_text and \
               self._rating == other.rating and self._user == other.user
