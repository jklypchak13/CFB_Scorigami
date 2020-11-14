from scorigami_table import ScorigamiTable, TableEntry
from model.game import Game
import sqlite3
from datetime import date as Date


def read_database(db_file: str) -> ScorigamiTable:
    conn = sqlite3.connect(db_file)

    result = conn.execute(
        '''
        SELECT *
        FROM Scorelines as s, Games as g, Games as h
        WHERE s.first_game_id = g.id and s.recent_game_id = h.id
        '''
    )

    table = ScorigamiTable([])
    for item in result:
        scoreline_id = item[0]
        winner_score = item[1]
        loser_score = item[2]
        first_game_id = item[3]
        recent_game_id = item[4]
        game_id_1 = item[5]
        w_team_1 = item[6]
        l_team_1 = item[7]
        g_date_1 = item[8]
        game_id_2 = item[9]
        w_team_2 = item[10]
        l_team_2 = item[11]
        g_date_2 = item[12]

        key = (winner_score, loser_score)
        first_game = Game(game_id_1, w_team_1, l_team_1,
                          winner_score, loser_score, g_date_1)
        recent_game = Game(game_id_2, w_team_2, l_team_2,
                           winner_score, loser_score, g_date_2)
        entry: TableEntry = TableEntry(value='Filled')
        entry.first_game = first_game
        entry.last_game = recent_game
        entry.first_game_id = game_id_1
        entry.last_game_id = game_id_2

        table.unique_scores[key] = entry

    print(len(table.unique_scores))


if __name__ == "__main__":
    read_database('data/game_db.sqlite3')
