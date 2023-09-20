from chess_insight import (
    ChessComApiCommunicator,
    LichessApiCommunicator,
    export_games_to_csv,
    Game,
)

Game("pgn_string", "usr", stockfish=None)

# c1 = LichessApiCommunicator(depth=10)
# c2 = ChessComApiCommunicator(depth=10)


# games = list(c1.games_generator("pro100wdupe", 20, "blitz"))
# games += list(c2.games_generator("Barabasz60", 10, "blitz"))


# export_games_to_csv(games)
