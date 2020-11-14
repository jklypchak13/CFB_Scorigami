import jinja2
import os
import json
from model.game import Game
from typing import List
OUTPUT_DIR: str = f'docs{os.sep}'
INPUT_DIR: str = './src/templates'
CACHE_FILE = 'data/scorgiami_cache.json'


def get_template(file_name: str) -> jinja2.Template:
    """get the specified template from the file system

    Args:
        file_name (str): the name of the file in the template directory

    Returns:
        jinja2.Template: The requested template
    """

    template_loader = jinja2.FileSystemLoader(searchpath=INPUT_DIR)
    templateEnv = jinja2.Environment(loader=template_loader)
    template = templateEnv.get_template(file_name)
    return template


def write_file(output: str, file_name: str):
    """write the specified string to a file

    Args:
        output (str): the string to write to file
        file_name (str): the name of the file (without the output directory)
    """
    with open(OUTPUT_DIR + file_name, "w") as fp:
        fp.write(output)


def write_cache(file_name: str, games: List[Game], years: List[int]):
    json_games = [game.to_json() for game in games]

    cache = {
        "years": years,
        "games": json_games
    }
    with open(file_name, 'w') as fp:
        json.dump(cache, fp)


def read_cache(file_name):
    games = []
    years = []

    cache = {}
    if os.path.exists(file_name):
        with open(file_name, 'r') as fp:
            cache = json.load(fp)
            games = [Game.from_json(game) for game in cache['games']]
            years = cache['years']

    return games, years


def check_directories():
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isdir('docs'):
        os.mkdir('docs')
