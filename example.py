from chess_insight import (
    ChessComApiCommunicator,
    LichessApiCommunicator,
    export_games_to_csv,
)


c1 = LichessApiCommunicator(depth=1)
c2 = ChessComApiCommunicator(depth=1)


games = list(c1.games_generator("pro100wdupe", 10, "blitz"))
games += list(c2.games_generator("Barabasz60", 10, "blitz"))


export_games_to_csv(games)
