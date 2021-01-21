class Game:
    def __init__(
        self,
        home_team,
        away_team,
        home_score=None,
        away_score=None,
        date=None,
        odds=None,
        projections=None,
    ):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.home_score = home_score
        self.away_score = away_score
        self.odds = odds
        self.projections = projections

    def print(self):
        if self.date:
            print(self.date.strftime("%d/%m/%Y"))
        print("{} @ {}".format(self.away_team, self.home_team))
        for projection in self.projections:
            print(
                "{}%   {}%".format(
                    int(projection.home_win_prob * 100),
                    int(projection.away_win_prob * 100),
                )
            )
            if projection.home_spread > 0.0:
                print("      -{}".format(projection.home_spread))
            elif projection.away_spread > 0.0:
                print("-{}".format(projection.away_spread))
            else:
                print("   PK")


class Projection:
    def __init__(
        self,
        source,
        home_win_prob=None,
        away_win_prob=None,
        home_spread=None,
        away_spread=None,
        over_under=None,
    ):
        self.source = source
        self.home_win_prob = home_win_prob
        self.away_win_prob = away_win_prob
        self.home_spread = home_spread
        self.away_spread = away_spread
        self.over_under = over_under


class Odds:
    def __init__(
        self,
        source,
        home_spread=None,
        away_spread=None,
        home_ml=None,
        away_ml=None,
        over=None,
        under=None,
    ):
        self.source = source
        self.home_spread = home_spread
        self.away_spread = away_spread
        self.home_ml = home_ml
        self.away_ml = away_ml
        self.over = over
        self.under = under
