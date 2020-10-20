from game_reader import GameReader


class YearReader:

    def __init__(self, year):
        self.data = []

        reader = GameReader(f"data/games_{year}")

        current_value = reader.next_game()
        while current_value is not None:
            self.data.append(current_value)

            current_value = reader.next_game()
        reader.close()

    def get_values(self):
        return self.data
