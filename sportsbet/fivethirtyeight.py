from bs4 import BeautifulSoup, SoupStrainer
import requests

FIVETHIRTYEIGHT_GAME_PROJECTIONS_URL = (
    "https://projects.fivethirtyeight.com/2021-nba-predictions/games/"
)


def upcoming_games_projections():
    response = requests.get(FIVETHIRTYEIGHT_GAME_PROJECTIONS_URL)
    response.raise_for_status()
    return _parse_upcoming_games(response.text)


def _parse_upcoming_games(game_projections_text):
    print("game projections text")
    strainer = SoupStrainer("div", id="games")
    soup = BeautifulSoup(game_projections_text, "lxml", parse_only=strainer)
    for day in soup.find("div", id="upcoming-days").find_all("section", class_="day"):
        print("=== {} ===".format(day.find("h3").get_text()))
        for game in day.find("div").find_all("table"):
            for team in game.find("tbody").find_all("tr", class_="team"):
                team_short = team.find("td", class_="team").get("class")[-1]
                team_name = team.find("td", class_="team").get_text()
                team_spread = team.find("td", class_="spread").get_text()
                team_win_prob = team.find("td", class_="chance").get_text()
                print("{} ({}) {} {}".format(team_name, team_short, team_win_prob, team_spread))
            print()
