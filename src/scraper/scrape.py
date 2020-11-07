from urllib.request import urlopen
from bs4 import BeautifulSoup
from data_types.game import Game
import urllib.error
import bs4
import datetime
from typing import Dict, List


def get_games(all_games: Dict[int, List[Game]]) -> Dict[int, List[Game]]:
    """get data for all CFB games that have been played, accounting for cached games

    Args:
        all_games (Dict[int, List[Game]]): the cached games

    Returns:
        Dict[int, List[Game]]: all games tat have been played
    """
    starting_year: int = 1869  # first year of CFB
    ending_year: int = datetime.datetime.now().year  # get up to date data
    cached_years: List[int] = all_games.keys()

    # Loop through all Years
    for current_year in range(starting_year, ending_year + 1):
        # Check cache, except current year. Get up to date data
        if current_year in cached_years and current_year != ending_year:
            print(f'Data for {current_year} found in cache')
            continue
        print(f'Currently Scraping Year {current_year}')
        table_rows = _get_year_data(current_year)
        all_games[current_year] = _process_year_data(table_rows)

    return all_games


def _get_year_data(year: int) -> List[BeautifulSoup]:
    """scrape the game data for the given year

    Args:
        year (int): the year to scrape

    Returns:
        List[Game]: the games that were played that year
    """
    url: str = f'https://www.sports-reference.com/cfb/years/{year}-schedule.html'
    try:
        page = urlopen(url)
    except(urllib.error.HTTPError):
        print(f'An Error has occurred while scraping games for {year}.')
        return []

    page = page.read()
    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find_all('tbody')[0]
    rows = table.find_all('tr')
    return rows


def _process_year_data(rows: List[BeautifulSoup]) -> List[Game]:
    """process the rows in the site's table, converting them into game objects

    Args:
        rows (List[BeautifulSoup]): the current years data

    Returns:
        List[Game]: the current years data as Game objects
    """
    games = []
    for row in rows:
        winner_points = _get_element(row, 'winner_points')
        loser_points = _get_element(row, 'loser_points')
        winner = _get_element(row, 'winner_school_name')
        loser = _get_element(row, 'loser_school_name')
        date = _get_element(row, 'date_game')
        if date != 'Date' and winner_points is not None:
            games.append(
                Game(winner, loser, winner_points, loser_points, date))
    return games


def _get_element(row: BeautifulSoup, attr: str) -> str:
    """extract the specified element from the given row

    Args:
        row (BeautifulSoup): the html representation of given row
        attr (str): the name of the attribute to extract

    Returns:
        str: the desired attribute
    """
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
