from bs4 import BeautifulSoup, SoupStrainer
import requests
from dateutil import parser
from .models import Game, Projection

FIVETHIRTYEIGHT_GAME_PROJECTIONS_URL = (
    "https://projects.fivethirtyeight.com/2021-nba-predictions/games/"
)


def upcoming_games_projections():
    response = requests.get(FIVETHIRTYEIGHT_GAME_PROJECTIONS_URL)
    response.raise_for_status()
    return _parse_upcoming_games(response.text)


def _parse_upcoming_games(game_projections_text):
    games = list()
    strainer = SoupStrainer("div", id="games")
    soup = BeautifulSoup(game_projections_text, "lxml", parse_only=strainer)
    for day_soup in soup.find("div", id="upcoming-days").find_all(
        "section", class_="day"
    ):
        date = parser.parse(day_soup.find("h3").get_text())
        for game_soup in day_soup.find("div").find_all("table"):
            away_team_soup, home_team_soup = game_soup.find("tbody").find_all(
                "tr", class_="team"
            )
            away_team = away_team_soup.find("td", class_="team").get("class")[-1]
            home_team = home_team_soup.find("td", class_="team").get("class")[-1]
            away_spread = away_team_soup.find("td", class_="spread").get_text()
            home_spread = home_team_soup.find("td", class_="spread").get_text()
            away_win_prob = away_team_soup.find("td", class_="chance").get_text()
            home_win_prob = home_team_soup.find("td", class_="chance").get_text()
            if home_spread.strip():
                home_spread = float(home_spread.strip())
                away_spread = home_spread * -1.0
            else:
                away_spread = float(away_spread.strip())
                home_spread = away_spread * -1.0
            home_win_prob = float(home_win_prob.strip(" %")) / 100.0
            away_win_prob = float(away_win_prob.strip(" %")) / 100.0
            projection = Projection(
                source="FiveThirtyEight",
                home_win_prob=home_win_prob,
                away_win_prob=away_win_prob,
                home_spread=home_spread,
                away_spread=away_spread,
            )
            game = Game(
                home_team=home_team,
                away_team=away_team,
                date=date,
                projections=[projection],
            )
            games.append(game)

    return games
