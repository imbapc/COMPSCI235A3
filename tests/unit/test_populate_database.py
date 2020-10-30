from SQLAlchemy import select, inspect

from Movie_Web_App.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['directors', 'movies', 'reviews', 'actors', 'genres', 'users']

def test_database_populate_select_all_actors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_actors_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_actors_table]])
        result = connection.execute(select_statement)

        all_actors_names = []
        for row in result:
            all_actors_names.append(row['name'])

        assert all_actors_names == ['New Zealand', 'Health', 'World', 'Politics', 'Travel', 'Entertainment', 'Business', 'Sport', 'Lifestyle', 'Opinion']


def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == ['thorke', 'fmercury', 'mjackson']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_comments_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_comments_table]])
        result = connection.execute(select_statement)

        all_comments = []
        for row in result:
            all_comments.append((row['id'], row['user_id'], row['article_id'], row['comment']))

        assert all_comments == [(1, 2, 1, 'Oh no, COVID-19 has hit New Zealand'),
                                (2, 1, 1, 'Yeah Freddie, bad news'),
                                (3, 3, 1, "I hope it's not as bad here as Italy!")]

def test_database_populate_select_all_movies(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_movies_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_movies_table]])
        result = connection.execute(select_statement)

        all_movies = []
        for row in result:
            all_movies.append((row['title'], row['year']))

        nr_articles = len(all_movies)

        assert all_movies[0] == ('Guardians of the Galaxy', 2014)
        assert all_movies[nr_articles//2] == (89, 'Covid 19 coronavirus: Queen to make speech urging Britain to rise to the unprecedented challenges of pandemic')
        assert all_movies[nr_articles-1] == (177, 'Covid 19 coronavirus: Kiwi mum on the heartbreak of losing her baby in lockdown')


