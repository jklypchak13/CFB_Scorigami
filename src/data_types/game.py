from typing import Dict
from datetime import date as Date


class Game:
    """represents a single game in the history of CFB
    """

    def __init__(self, winner: str, loser: str, winner_points: int, loser_points: int, date: Date):
        self.winner: str = winner
        self.loser: str = loser
        self.winner_points: int = int(winner_points)
        self.loser_points: int = int(loser_points)
        self.date: Date = date

    def __repr__(self):
        return f'{self.date}, Winner:{self.winner}({self.winner_points}) Loser:{self.loser}({self.loser_points})'

    def __eq__(self, other):
        type_equal = type(self) == type(other)
        teams_equal = self.winner == other.winner and self.loser == other.loser
        scores_equal = self.winner_points == other.winner_points and self.loser_points == other.loser_points
        date_equal = self.date == other.date
        return type_equal and teams_equal and scores_equal and date_equal

    def __lt__(self, other):
        """compare by date
        """
        return self.date < other.date

    def __gt__(self, other):
        """compare by date
        """
        return self.date > other.date

    def to_json(self) -> Dict[str, any]:
        """return the json represention of this

        Returns:
            Dict[str, any]: this object
        """
        result = self.__dict__
        result['date'] = str(self.date)
        return result

    @staticmethod
    def from_json(json_data: Dict[str, any]):
        """Construct a Game from a json object

        Args:
            json_data (Dict[str): the object to be constructed

        Returns:
            Game: the dictionary as a game
        """
        new_game = Game(None, None, 0, 0, None)
        new_game.__dict__.update(json_data)
        new_game.date = Date.fromisoformat(new_game.date)
        return new_game
