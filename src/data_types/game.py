from typing import Dict
import datetime

MONTH_TABLE = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}


def parse_date_string(date_string: str) -> datetime.date:
    """parse the given string into a datetime object

    Args:
        date_string (str): the date in form MMM DD, YYYY

    Returns:
        datetime.date: [description]
    """

    components = date_string.replace(',', '').split(' ')
    day = '0' + components[1] if len(components[1]) < 2 else components[1]
    month = MONTH_TABLE[components[0]]
    year = components[2]
    new_str = f'{year}-{month}-{day}'

    return datetime.date.fromisoformat(new_str)


class Game:
    """represents a single game in the history of CFB
    """

    def __init__(self, winner: str, loser: str, winner_points: int, loser_points: int, date: str):
        self.winner: str = winner
        self.loser: str = loser
        self.winner_points: int = int(winner_points)
        self.loser_points: int = int(loser_points)
        self.date: str = date

    def __repr__(self):
        return f'{self.date}, Winner:{self.winner}({self.winner_points}) Loser:{self.loser}({self.loser_points})'

    def __eq__(self, other):
        type_equal = type(self) == type(other)
        teams_equal = self.winner == other.winner and self.loser == other.loser
        scores_equal = self.winner_points == other.winner_points and self.loser_points == other.loser_points
        return type_equal and teams_equal and scores_equal

    def __lt__(self, other):
        """compare by date
        """
        return parse_date_string(self.date) < parse_date_string(other.date)

    def __gt__(self, other):
        """compare by date
        """
        return parse_date_string(self.date) > parse_date_string(other.date)

    def to_json(self) -> Dict[str, any]:
        """return the json represention of this

        Returns:
            Dict[str, any]: this object
        """
        return self.__dict__

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
        return new_game
