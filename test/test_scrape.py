import pytest
from . import context
import bs4
from data_types import Game
import scraper.scrape as scrape
import datetime


@pytest.fixture
def sample_rows():
    rows = scrape._get_year_data(1869)
    return rows


def get_fake_cache():
    return [i for i in range(1870, 2021)]

# Test Get Year Data


def test_get_year_data_length(sample_rows):
    # 2 Games in 1869, plus the table header
    assert len(sample_rows) == 3


def test_get_year_data_invalid():
    # No Games in 1868
    assert scrape._get_year_data(1868) == []


# Test Get Element

def test_get_element_non_existant(sample_rows):
    row = sample_rows[1]
    assert scrape._get_element(row, 'potato') is None


def test_get_element_scores(sample_rows: bs4.element.ResultSet):
    row = sample_rows[0]
    assert scrape._get_element(row, 'winner_points') == 6
    assert scrape._get_element(row, 'loser_points') == 4


def test_get_element_schools(sample_rows: bs4.element.ResultSet):
    row = sample_rows[0]
    assert scrape._get_element(row, 'winner_school_name') == 'Rutgers'
    assert scrape._get_element(row, 'loser_school_name') == 'Princeton'


def test_get_element_date(sample_rows: bs4.element.ResultSet):
    row = sample_rows[0]
    assert scrape._get_element(row, 'date_game') == 'Nov 6, 1869'


# Test Proccess Year Data
def test_process_year_data_length(sample_rows):
    games = scrape._process_year_data(sample_rows)
    assert len(games) == 2


def test_process_year_data_correct_game(sample_rows):
    games = scrape._process_year_data(sample_rows)

    expected = Game("Rutgers", "Princeton", 6, 4, "Nov 6, 1869")
    assert games[0] == expected


# Test Get Games

def test_get_games_ignore_current_year_true():
    current_year = datetime.datetime.now().year
    fake_cache = get_fake_cache()
    result, years = scrape.get_games(fake_cache)
    current_year = datetime.datetime.now().year
    expected_years = [i for i in range(1869, current_year + 1)]
    assert sorted(years) == sorted(expected_years)
    assert len(result[current_year]) > 0


def test_get_games_ignore_current_year_false():
    current_year = datetime.datetime.now().year
    fake_cache = get_fake_cache()
    result, years = scrape.get_games(fake_cache, ignore_current=True)
    current_year = datetime.datetime.now().year
    expected_years = [i for i in range(1869, current_year + 1)]
    assert sorted(years) == sorted(expected_years)
    assert len(result[current_year]) > 0


def test_get_games_1869_correct():
    fake_cache = get_fake_cache()
    result, years = scrape.get_games(fake_cache)

    expected = [
        Game("Rutgers", "Princeton", 6, 4, "Nov 6, 1869"),
        Game("Princeton", "Rutgers", 8, 0, "Nov 13, 1869")
    ]
    current_year = datetime.datetime.now().year
    expected_years = [i for i in range(1869, current_year + 1)]
    assert sorted(years) == sorted(expected_years)
    assert result[1869] == expected


def test_get_games_skip_cache():

    fake_cache = get_fake_cache()
    result, years = scrape.get_games(fake_cache)
    current_year = datetime.datetime.now().year
    expected_years = [i for i in range(1869, current_year + 1)]
    assert sorted(years) == sorted(expected_years)
    assert 1870 not in result.keys()
