

class Game:

    def __init__(self, winner, loser, winner_points, loser_points, date):
        self.winner = winner
        self.loser = loser
        self.winner_points = winner_points
        self.loser_points = loser_points
        self.date = date

    def file_out(self):
        return f'{self.date}\n{self.winner}\n{self.winner_points}\n{self.loser}\n{self.loser_points}'

    def __repr__(self):
        return f'{self.date}, Winner:{self.winner}({self.winner_points}) Loser:{self.loser}({self.loser_points})'
