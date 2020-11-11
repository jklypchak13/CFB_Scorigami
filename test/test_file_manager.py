import pytest
from . import context
from file_manger import read_cache, write_cache
from data_types import Game


@pytest.fixture
def sample_games():

    games = [
        Game("Rutgers", "Princeton", 6, 4, "Nov 6, 1869"),
        Game("Princeton", "Rutgers", 8, 0, "Nov 13, 1869")
    ]
    return games


@pytest.fixture
def sample_years():
    years = [1869]
    return years


def test_read_cache(sample_games, sample_years):
    input_file = 'test/data/sample_cache.json'
    games, years = read_cache(input_file)
    assert games == sample_games
    assert years == sample_years


def test_write_cache(sample_games, sample_years):
    output_file = 'test/data/cache_output.json'
    input_file = 'test/data/sample_cache.json'
    write_cache(output_file, sample_games, sample_years)

    expected = ''
    with open(input_file, 'r') as fp:
        expected = fp.read()

    result = ''
    with open(output_file, 'r') as fp:
        result = fp.read()

    assert result == expected
