#!/usr/bin/env python3

import sys
from contextlib import contextmanager
from datetime import datetime
from sqlite3 import connect
from sys import argv, stdout

DB_FILENAME = 'db.sqlite3'


@contextmanager
def disposable_cursor(connection):
    try:
        cursor = connection.cursor()
        yield cursor
    finally:
        cursor.close()


def initialize_data_structures(cursor):
    cursor.execute(
        'CREATE TABLE genre ('
        '  id INTEGER NOT NULL, '
        '  name VARCHAR NOT NULL, '
        '  PRIMARY KEY (id)'
        ')'
    )
    cursor.execute(
        'CREATE TABLE movie ('
        '  id INTEGER NOT NULL, '
        '  title VARCHAR(128) NOT NULL, '
        '  genre_id INTEGER NOT NULL, '
        '  rating INTEGER NOT NULL, '
        '  released DATE NOT NULL, '
        '  description VARCHAR, '
        '  created DATETIME, '
        '  PRIMARY KEY (id), '
        '  FOREIGN KEY(genre_id) REFERENCES genre (id)'
        ')'
    )


def load_data(cursor):
    table = input('What table you would like to add entry to? ')
    if table == 'genre':
        name = input('Get genre name: ')
        cursor.execute(f"INSERT INTO genre (name) VALUES ('{name}')")
        stdout.write(f'Id of added genre is {cursor.lastrowid}.\n')
        return
    if table == 'movie':
        title = input('Get movie title: ')
        genre_id = input('Get movie genre id: ')
        rating = input('Get movie rating: ')
        released = input('Get movie release date: ')
        description = input('Get movie description: ')
        cursor.execute(
            f"INSERT INTO movie ("
            f"  title, genre_id, rating, released, description, created"
            f") "
            f"VALUES ("
            f"  '{title}', {genre_id}, {rating}, '{released}', "
            f"  '{description}', DATETIME('now') "
            f")"
        )
        stdout.write(f'Id of added movie is {cursor.lastrowid}.\n')
        return
    sys.exit('Invalid choice.')


def dump_data(cursor):
    table = input('What table you would like to dump? ')
    if table == 'genre':
        cursor.execute('SELECT id, name FROM genre')
        genres = cursor.fetchall()
        for genre_id, genre_name in genres:
            stdout.write(f'Genre {genre_id} is {genre_name}.\n')
        return
    if table == 'movie':
        cursor.execute(
            'SELECT title, genre.name, released '
            'FROM movie '
            'JOIN genre ON movie.genre_id = genre.id'
        )
        movies = cursor.fetchall()
        for title, genre, released in movies:
            release_year = datetime.strptime(released, '%Y-%m-%d').year
            stdout.write(
                f'"{title}" is a {genre.lower()} released in {release_year}.\n'
            )
        return
    sys.exit('Invalid choice.')


def parse_args():
    '''Gets function to call based on provided argvs.'''
    if len(argv) < 2:
        sys.exit('No subcommand provided.')
    if argv[1] == 'init':
        return initialize_data_structures
    if argv[1] == 'loaddata':
        return load_data
    if argv[1] == 'dumpdata':
        return dump_data
    sys.exit('Invalid subcommand provided.')


def main():
    with connect(DB_FILENAME) as connection, \
            disposable_cursor(connection) as cursor:
        function_to_call = parse_args()
        function_to_call(cursor)


if __name__ == "__main__":
    main()
