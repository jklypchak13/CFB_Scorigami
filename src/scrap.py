from urllib.request import urlopen
from bs4 import BeautifulSoup
from game import Game
import urllib.error
import bs4


def get_year_data(year):
    url = f'https://www.sports-reference.com/cfb/years/{year}-schedule.html'
    try:
        page = urlopen(url)
    except(urllib.error.HTTPError):
        print("error")
        return None

    page = page.read()
    soup = BeautifulSoup(page, 'html.parser')

    def get_element(row, attr):
        result = []
        val = row.find_all(attrs={'data-stat': attr})
        if len(val) > 0:
            if len(val[0].contents) > 0:
                val = val[0].contents[0]
            else:
                return None
            if type(val) == bs4.element.Tag:
                temp = val.contents[0]
                val = temp
            else:
                if val.next_sibling is not None:
                    val = val.next_sibling
                    val = val.contents[0]
            return val
        else:
            return None

    thing = soup.find_all('tbody')[0]
    table_body = thing.find_all
    games = []
    for row in thing.find_all('tr'):
        winner_points = get_element(row, 'game_')
        winner_points = get_element(row, 'winner_points')
        loser_points = get_element(row, 'loser_points')
        winner = get_element(row, 'winner_school_name')
        loser = get_element(row, 'loser_school_name')
        date = get_element(row, 'date_game')
        if date != 'Date' and winner_points is not None:
            games.append(
                Game(winner, loser, winner_points, loser_points, date))
    return games


scorigami = [[0 for i in range(300)] for i in range(300)]


def mark_game(game, scorigami):
    scorigami[int(game.winner_points)][int(game.loser_points)] += 1


for i in range(2019, 2020):

    data = get_year_data(str(i))
    if data is not None:
        output_file = open(f'data/games_{i}', "w")
        for game in data:
            output_file.write(game.file_out() + "\n")
            mark_game(game, scorigami)
    else:
        print(f'Error: {i}')
