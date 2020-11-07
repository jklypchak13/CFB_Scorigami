from file_manger import get_template, write_file, read_cache, write_cache, check_directories
from scraper import get_games
from scorigami_table import ScorigamiTable


def generate_index(score_table):
    max_score = score_table.max_score()
    template = get_template('index.html')
    write_file(template.render(table=score_table,
                               max_score=max_score), 'index.html')


if __name__ == "__main__":
    check_directories()
    cached_games = read_cache()
    all_games = get_games(cached_games)
    table = ScorigamiTable(all_games)
    generate_index(table)
    write_cache(all_games)
