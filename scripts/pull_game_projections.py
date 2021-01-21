from sportsbet import fivethirtyeight

game_projections = fivethirtyeight.upcoming_games_projections()
for game in game_projections:
    game.print()
    print()
