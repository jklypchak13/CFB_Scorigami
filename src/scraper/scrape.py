from urllib.request import urlopen
from bs4 import BeautifulSoup
from data_types.game import Game
import urllib.error
import bs4
from datetime import date as Date
from typing import Dict, List
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


def parse_date_string(date_string: str) -> Date:
    """parse the given string into a datetime object

    Args:
        date_string (str): the date in form MMM DD, YYYY

    Returns:
        Date: the date
    """

    components = date_string.replace(',', '').split(' ')
    day = '0' + components[1] if len(components[1]) < 2 else components[1]
    month = MONTH_TABLE[components[0]]
    year = components[2]
    new_str = f'{year}-{month}-{day}'

    return Date.fromisoformat(new_str)


def get_games(cached_years: List[int], ignore_current=True) -> Dict[int, List[Game]]:
    """get data for all CFB games that have been played, accounting for cached games

    Args:
        cached_years (List[int]): the years to skip
        ignore_current (bool, optional): to ignore current eyar in cache. Defaults to True.

    Returns:
        Dict[int, List[Game]]: all games tat have been played
    """
    starting_year: int = 1869  # first year of CFB
    ending_year: int = Date.today().year  # get up to date data

    all_games = {}

    if ignore_current and ending_year in cached_years:
        cached_years.remove(ending_year)

    all_years = cached_years
    # Loop through all Years
    for current_year in range(starting_year, ending_year + 1):
        # Check cache, except current year. Get up to date data
        if current_year in cached_years:
            print(f'Data for {current_year} found in cache')
            continue
        print(f'Currently Scraping Year {current_year}')
        table_rows = _get_year_data(current_year)
        all_games[current_year] = _process_year_data(table_rows)
        all_years.append(current_year)

    return all_games, all_years


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
            date = parse_date_string(date)
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

        try:
            val = int(val)
            return val
        except ValueError:
            return val
    else:
        return None
