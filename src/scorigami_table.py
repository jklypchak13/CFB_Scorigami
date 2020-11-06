from typing import Dict, List, Tuple
from data_types import Game
import pprint


class TableEntry:
    def __init__(self, value="Empty", game=None):
        self.first_game = game
        self.value = value

    def __repr__(self):
        return f'Value: {self.value}, Game: {self.first_game}'

    def __lt__(self, other):
        return self.first_game.winner_points < other.first_game.winner_points


class ScorigamiTable:

    def __init__(self, all_games: Dict[int, List[Game]]):
        self.unique_scores: Dict[Tuple[int, int], TableEntry] = {}
        for year, games in all_games.items():
            self.add_games(games)

    def add_games(self, games: List[Game]):
        for game in games:
            key = (game.winner_points, game.loser_points)

            if key in self.unique_scores.keys():
                # This score has occurred
                continue

            # Unique Score
            entry = TableEntry(value='Filled', game=game)
            self.unique_scores[key] = entry

    def get_value(self, winner_score, loser_score):
        return self.get_entry(winner_score, loser_score).value

    def get_game(self, winner_score, loser_score):
        return self.get_entry(winner_score, loser_score).game

    def get_entry(self, winner_score, loser_score):
        key = (winner_score, loser_score)
        value = "Empty" if winner_score >= loser_score else "Impossible"
        default = TableEntry(value)
        result = self.unique_scores.setdefault(key, default)
        return result

    def max_score(self):
        return max(self.unique_scores.keys())[0]
