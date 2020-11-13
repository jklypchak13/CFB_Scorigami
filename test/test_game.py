import pytest
from . import context
from data_types import Game
from datetime import date as Date


@pytest.fixture
def sample_game():
    game = Game("Ohio State", "Michigan", 100, 0, Date(2020, 11, 5))
    return game


def test_to_json(sample_game):
    expected = {
        "winner": "Ohio State",
        "loser": "Michigan",
        "winner_points": 100,
        "loser_points": 0,
        "date": "2020-11-05"
    }
    assert sample_game.to_json() == expected


def test_from_json(sample_game):
    data = {
        "winner": "Ohio State",
        "loser": "Michigan",
        "winner_points": 100,
        "loser_points": 0,
        "date": "2020-11-05"
    }
    assert Game.from_json(data) == sample_game


def test_repr(sample_game):
    expected = '2020-11-05, Winner:Ohio State(100) Loser:Michigan(0)'
    assert sample_game.__repr__() == expected


def test_equal_true(sample_game):
    other_game = Game("Ohio State", "Michigan", 100, 0, Date(2020, 11, 5))
    assert sample_game == other_game


def test_equal_false(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, Date(2020, 10, 30))
    assert sample_game != other_game


def test_lt_true(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, Date(2020, 11, 30))
    assert sample_game < other_game


def test_lt_false(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, Date(2020, 9, 30))
    assert not sample_game < other_game


def test_gt_true(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, Date(2020, 11, 30))
    assert not sample_game > other_game


def test_tt_false(sample_game):
    other_game = Game("Rutgers", "Michigan", 99, 0, Date(2020, 9, 30))
    assert sample_game > other_game
