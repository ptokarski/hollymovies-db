#!/usr/bin/env python3

from sqlite3 import connect

DB_FILENAME = 'db.sqlite3'


def main():
    with connect(DB_FILENAME) as connection:
        cursor = connection.cursor()
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
        cursor.execute("INSERT INTO genre VALUES (1, 'Drama')")
        cursor.execute(
            "INSERT INTO movie VALUES ("
            "  1, 'The Shawshank Redemption', 1, 9, DATE('1994-01-01'), "
            "  'very good movie', DATETIME('now') "
            ")"
        )
        cursor.close()


if __name__ == "__main__":
    main()
