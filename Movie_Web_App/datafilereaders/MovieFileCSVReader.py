import csv
import os

from Movie_Web_App.domainmodel.Model import Director, Genre, Actor, Movie


class MovieFileCSVReader:
    def __init__(self, filename: str):
        if isinstance(filename, str):
            self._filename = os.path.join(filename, 'Data1000Movies.csv')
        else:
            self._filename = ""
        self._dataset_of_movies = []
        self._dataset_of_actors = []
        self._dataset_of_directors = []
        self._dataset_of_genres = []

    def read_csv_file(self):
        with open(self._filename, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            index = 2
            for row in reader:
                title = row["Title"]
                release_year = int(row["Year"])
                movie1 = Movie(title, release_year)
                self._dataset_of_movies.append(movie1)
                movie1.description = row["Description"]
                movie1.runtime_minutes = int(row["Runtime (Minutes)"])
                movie1.id = int(row["Rank"])
                director_name = row["Director"]
                director = Director(director_name)
                if director not in self._dataset_of_directors:
                    self._dataset_of_directors.append(director)
                    movie1.director = director
                else:
                    n = self._dataset_of_directors.index(director)
                    movie1.director = self._dataset_of_directors[n]
                director.movie_list.append(movie1)
                actor_name_list = row["Actors"].split(",")
                index1 = 1
                for name in actor_name_list:
                    actor = Actor(name.strip())
                    if actor not in self._dataset_of_actors:
                        self._dataset_of_actors.append(actor)
                        movie1.actors.append(actor)
                        actor.act_movie.append(movie1)
                    else:
                        n = self._dataset_of_actors.index(actor)
                        movie1.actors.append(self._dataset_of_actors[n])
                        self._dataset_of_actors[n].act_movie.append(movie1)
                    index1 += 1
                for actor in movie1.actors:
                    for colleague in movie1.actors:
                        if actor != colleague:
                            actor.add_actor_colleague(colleague)

                genre_list = row["Genre"].split(",")
                for type in genre_list:
                    genre = Genre(type.strip())
                    movie1.genres.append(genre)
                    if genre not in self._dataset_of_genres:
                        self._dataset_of_genres.append(genre)
                movie1.rating = row["Votes"]
                movie1.metascore = row["Metascore"]
                index += 1

    @property
    def dataset_of_movies(self):
        return self._dataset_of_movies

    @property
    def dataset_of_directors(self):
        return self._dataset_of_directors

    @property
    def dataset_of_actors(self):
        return self._dataset_of_actors

    @property
    def dataset_of_genres(self):
        return self._dataset_of_genres
