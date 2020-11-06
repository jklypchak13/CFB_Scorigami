import jinja2
from data_types import Game
from file_manger import get_template, write_file, read_cache, write_cache, check_directories
from scraper import get_games
from pprint import pprint
import json
import os


if __name__ == "__main__":
    check_directories()
    all_games = read_cache()
    games = get_games(all_games)
    write_cache(games)
