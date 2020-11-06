from year_reader import YearReader


def get_table():
    scorigami = [[0 for i in range(300)] for i in range(300)]

    def mark_game(game, scorigami):
        scorigami[int(game.winner_points)][int(game.loser_points)] += 1

    for i in range(1869, 2020):
        if i != 1871:
            print(i)
            data = YearReader(i).get_values()
            for game in data:
                mark_game(game, scorigami)
    return scorigami


scorigami = get_table()
