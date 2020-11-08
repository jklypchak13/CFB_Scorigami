import pytest
from . import context
from scorigami_table import ScorigamiTable, TableEntry
from data_types import Game

EMPTY_ENTRY = TableEntry()
IMPOSSIBLE_ENTRY = TableEntry('Impossible')


@pytest.fixture
def sample_games():
    samples = [
        Game('Ohio State', 'Michigan', 100, 0, 'Nov 3, 2020'),
        Game('Penn State', 'Rutgers', 100, 0, 'Nov 3, 2020'),
        Game('Clemson', 'Alabama', 23, 20, 'Nov 3, 2020'),
        Game('Ohio State', 'Michigan State', 17, 7, 'Nov 3, 2020'),
    ]
    return samples


@pytest.fixture
def populated_table():
    samples = [
        Game('Ohio State', 'Michigan', 100, 0, 'Nov 3, 2020'),
        Game('Penn State', 'Rutgers', 100, 0, 'Nov 2, 2020'),
        Game('Clemson', 'Alabama', 23, 20, 'Nov 3, 2020'),
        Game('Ohio State', 'Michigan State', 17, 7, 'Nov 3, 2020'),
    ]
    return ScorigamiTable({2020: samples})


def test_constructor(sample_games):
    table = ScorigamiTable({2020: sample_games})
    assert len(table) == 3


def test_add_games_empty():
    table = ScorigamiTable({})
    table.add_games([])

    assert len(table) == 0


def test_add_games_nonempty(sample_games):
    table = ScorigamiTable({})

    table.add_games(sample_games)

    assert len(table) == 3


def test_add_games_has_value(sample_games):
    table = ScorigamiTable({})

    table.add_games(sample_games)

    assert table.get_value(100, 0) == 'Filled'


def test_get_entry_impossible(populated_table):
    assert populated_table.get_entry(0, 2) == IMPOSSIBLE_ENTRY


def test_get_entry_empty(populated_table):
    assert populated_table.get_entry(10, 0) == EMPTY_ENTRY


def test_get_entry_filled(populated_table):
    result = populated_table.get_entry(100, 0)
    expected = TableEntry('Filled', Game(
        'Penn State', 'Rutgers', 100, 0, 'Nov 2, 2020'))
    assert result == expected


def test_get_game_impossible(populated_table):
    assert populated_table.get_game(0, 2) is None


def test_get_game_empty(populated_table):
    assert populated_table.get_game(10, 0) is None


def test_get_game_filled(populated_table):
    result = populated_table.get_game(100, 0)
    expected = Game(
        'Penn State', 'Rutgers', 100, 0, 'Nov 2, 2020')
    assert result == expected


def test_get_value_impossible(populated_table):
    assert populated_table.get_game(0, 2) is None


def test_get_value_empty(populated_table):
    assert populated_table.get_game(10, 0) is None


def test_get_value_filled(populated_table):
    result = populated_table.get_value(100, 0)
    expected = 'Filled'
    assert result == expected


def test_get_max_score(populated_table):
    assert populated_table.max_score() == 100
