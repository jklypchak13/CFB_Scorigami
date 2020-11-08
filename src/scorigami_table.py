from typing import Dict, List, Tuple
from data_types import Game
import pprint


class TableEntry:
    """Represents an entry in the scorigami table
    """

    def __init__(self, value='Empty', game=None):
        self.first_game: Game = game
        self.value: str = value

    def __repr__(self):
        return f'Value: {self.value}, Game: {self.first_game}'

    def __lt__(self, other):
        return self.first_game.winner_points < other.first_game.winner_points

    def __eq__(self, other):
        return self.first_game == other.first_game and self.value == other.value


class ScorigamiTable:
    """the whole scorigami table, tracking scores that have occureced
    """

    def __init__(self, all_games: Dict[int, List[Game]]):
        self.unique_scores: Dict[Tuple[int, int], TableEntry] = {}
        for year, games in all_games.items():
            self.add_games(games)

    def add_games(self, games: List[Game]):
        """add the given games to the scorigami table, checking if older/newer games exist

        Args:
            games (List[Game]): the games to add
        """
        for game in games:
            key = (game.winner_points, game.loser_points)

            if key in self.unique_scores.keys():
                # This score has occurred, See which game sooner
                previous = self.unique_scores[key]
                if previous.first_game < game:
                    continue

            # Unique Score
            entry = TableEntry(value='Filled', game=game)
            self.unique_scores[key] = entry

    def get_value(self, winner_score: int, loser_score: int) -> str:
        """get the string value of the table entry for the given scoreline

        Args:
            winner_score (int): the winner's score
            loser_score (int): the loser's score

        Returns:
            str: the value of the specified table entry
        """
        return self.get_entry(winner_score, loser_score).value

    def get_game(self, winner_score: int, loser_score: int) -> Game:
        """get the Game of the table entry for the given scoreline

        Args:
            winner_score (int): the winner's score
            loser_score (int): the loser's score

        Returns:
            str: the Game for the specified table entry
        """
        return self.get_entry(winner_score, loser_score).first_game

    def get_entry(self, winner_score: int, loser_score: int) -> TableEntry:
        """get the TableEntry for the given score line

        Args:
            winner_score (int): the winner's score
            loser_score (int): the loser's score

        Returns:
            TableEntry: [description]
        """
        EMPTY_ENTRY = TableEntry()
        IMPOSSIBLE_ENTRY = TableEntry('Impossible')

        key = (winner_score, loser_score)
        result = EMPTY_ENTRY if winner_score >= loser_score else IMPOSSIBLE_ENTRY

        if key in self.unique_scores:
            result = self.unique_scores[key]
        return result

    def max_score(self) -> int:
        """get the highest score to occur

        Returns:
            int: the highest score
        """
        return max(self.unique_scores.keys())[0]

    def __len__(self):
        return len(self.unique_scores.keys())
