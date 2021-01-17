#!/usr/bin/env python3

from sqlite3 import connect
from sys import stdout

DB_FILENAME = 'db.sqlite3'


def main():
    with connect(DB_FILENAME) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT 'Hello, world!'")
        result, = cursor.fetchone()
        stdout.write(f'{result}\n')
        cursor.close()


if __name__ == "__main__":
    main()
