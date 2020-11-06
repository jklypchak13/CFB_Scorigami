import jinja2
import os
import json
from data_types import Game
OUTPUT_DIR: str = f'docs{os.sep}'
INPUT_DIR: str = './src/templates'


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


def write_cache(game_dict):

    for year, games in game_dict.items():
        output_file = f'data/cache_{year}.json'
        updated_games = [game.to_json() for game in games]
        with open(output_file, 'w') as fp:
            json.dump(updated_games, fp)


def read_cache():
    years = []
    for root, dirs, files in os.walk('data'):
        for file in files:
            if 'cache' in file:
                # extract year
                year = file[6:-5]
                years.append(int(year))
    return years


def write_cache(game_dict):

    for year, games in game_dict.items():
        output_file = f'data/cache_{year}.json'
        updated_games = [game.to_json() for game in games]
        with open(output_file, 'w') as fp:
            json.dump(updated_games, fp)


def read_cache():
    all_games = {}
    for root, dirs, files in os.walk('data'):
        for file in files:
            if 'cache' in file:
                # extract year
                year = int(file[6:-5])
                games = []
                with open(root + os.sep + file, 'r') as fp:
                    games = json.load(fp)
                    games = [Game.from_json(game) for game in games]
                all_games[year] = games
    return all_games


def check_directories():
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isdir('docs'):
        os.mkdir('docs')
