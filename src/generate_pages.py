from typing import ChainMap
from file_manger import get_template, write_file, read_cache, write_cache, check_directories
from scraper import get_games
from scorigami_table import ScorigamiTable

CACHE_FILE = 'data/scorgiami_cache.json'


def generate_index(score_table):
    max_score = score_table.max_score()
    template = get_template('index.html')
    write_file(template.render(table=score_table,
                               max_score=max_score), 'index.html')


if __name__ == "__main__":
    check_directories()
    cached_games, cached_years = read_cache(CACHE_FILE)
    new_games, all_years = get_games(cached_years)

    all_games = cached_games
    for year, games in new_games.items():
        all_games.extend(games)

    table = ScorigamiTable(all_games)
    generate_index(table)

    important_games = table.extract_games()
    write_cache(CACHE_FILE, important_games, all_years)
