import pytest
from . import context
from data_types import Game
from data_types.game import parse_date_string
import datetime


@pytest.fixture
def sample_game():
    game = Game("Ohio State", "Michigan", 100, 0, "Nov 5, 2020")
    return game


def test_parse_date_string():
    expected = datetime.date.fromisoformat('2020-10-31')
    result = parse_date_string('Oct 31, 2020')
    assert expected == result


def test_to_json(sample_game):
    expected = {
        "winner": "Ohio State",
        "loser": "Michigan",
        "winner_points": 100,
        "loser_points": 0,
        "date": "Nov 5, 2020"
    }
    assert sample_game.to_json() == expected


def test_from_json(sample_game):
    data = {
        "winner": "Ohio State",
        "loser": "Michigan",
        "winner_points": 100,
        "loser_points": 0,
        "date": "Nov 5, 2020"
    }
    assert Game.from_json(data) == sample_game


def test_repr(sample_game):
    expected = 'Nov 5, 2020, Winner:Ohio State(100) Loser:Michigan(0)'
    assert sample_game.__repr__() == expected


def test_equal_true(sample_game):
    other_game = Game("Ohio State", "Michigan", 100, 0, "Oct 31, 2020")
    assert sample_game == other_game


def test_equal_false(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, "Oct 30, 2020")
    assert sample_game != other_game


def test_lt_true(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, "Nov 30, 2020")
    assert sample_game < other_game


def test_lt_false(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, "Sep 30, 2020")
    assert not sample_game < other_game


def test_gt_true(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, "Nov 30, 2020")
    assert not sample_game > other_game


def test_tt_false(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, "Sep 30, 2020")
    assert sample_game > other_game
