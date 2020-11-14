import os
from os import read
import sqlite3
from sqlite3 import Error
import datetime
from sqlite3.dbapi2 import Cursor
from scraper import get_games
from scraper.scrape import parse_date_string
from scorigami_table import ScorigamiTable
from file_manger import read_cache
from typing import Tuple
from model.game import Game
DB_FILE = 'data/game_db.sqlite3'


def create_database():
    """freshly create the database, and the used databases
    """
    connection = None
    try:
        connection = sqlite3.connect(DB_FILE)
    except Error as e:
        print(e)

    create_game_table: str = '''CREATE TABLE IF NOT EXISTS Games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        winning_team TEXT NOT NULL,
        losing_team TEXT NOT NULL,
        game_date DATE NOT NULL
    )'''

    create_scoreline_table: str = '''CREATE TABLE IF NOT EXISTS Scorelines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        winning_score INTEGER NOT NULL,
        losing_score INTEGER NOT NULL,
        first_game_id INTEGER NOT NULL,
        recent_game_id INTEGER NOT NULL,
        FOREIGN KEY (first_game_id) REFERENCES Games (id),
        FOREIGN KEY (recent_game_id) REFERENCES Games (id)
    )'''
    connection.execute(create_game_table)
    connection.execute(create_scoreline_table)
    connection.commit()
    connection.close()


def seed_db():
    """fill the data base with the up to date data
    """
    games, years = read_cache('data/scorgiami_cache.json')
    table = ScorigamiTable(games)
    conn = sqlite3.connect(DB_FILE)
    cursor: sqlite3.Cursor = conn.cursor()

    for key, entry in table.unique_scores.items():
        first_game: Game = entry.first_game
        last_game: Game = entry.last_game

        # Insert the First Game with the scoreline
        cursor.execute(insert_game(first_game))
        first_index = cursor.lastrowid
        last_index = cursor.lastrowid

        # If the two games in the table are different, insert the second one
        if first_game != last_game:
            cursor.execute(insert_game(last_game))
            last_index = cursor.lastrowid

        # Insert the score line
        cursor.execute(insert_scoreline(
            key, first_index, last_index))

        conn.commit()
    cursor.close()


def insert_game(game: Game) -> str:
    """generate the SQL statement for inserting a Game

    Args:
        id (int): the id of the given game
        game (Game): the game to insert

    Returns:
        str: the SQL statement to insert the given game
    """
    date: datetime.date = game.date
    game_date: str = f'"{date.year}-{date.month}-{date.day}"'
    game_insert: str = f'''
        INSERT INTO GAMES (winning_team, losing_team, game_date) VALUES (
         "{game.winner}", "{game.loser}", {game_date}
        )
        '''
    return game_insert


def insert_scoreline(scoreline: Tuple[int, int], first_id: int, last_id: int) -> str:
    """generate the SQL statement for inserting a scoreline

    Args:
        id (int): the ID of the scoreline
        scoreline (Tuple[int, int]): the winning and losing score
        first_id (int): the id of the first game to have this scoreline
        last_id (int): the id of the most recent game to have this scoreline

    Returns:
        str: the finalized SQL query
    """
    return f'''
        INSERT INTO SCORELINES (winning_score, losing_score, first_game_id, recent_game_id) VALUES (
            {scoreline[0]}, {scoreline[1]}, {first_id}, {last_id}
        )
    '''


if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        create_database()
    seed_db()
