from game import Game


class GameReader:

    def __init__(self, file_name):
        self.input = open(file_name, "r")

    def next_game(self):
        date = self.input.readline()[0:-1]
        winner = self.input.readline()[0:-1]
        winner_points = self.input.readline()[0:-1]
        loser = self.input.readline()[0:-1]
        loser_points = self.input.readline()[0:-1]
        if date == '':
            return None
        return Game(winner, loser, winner_points, loser_points, date)

    def close(self):
        self.input.close()
