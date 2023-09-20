from chess_insight import (
    ChessComApiCommunicator,
    LichessApiCommunicator,
    export_games_to_csv,
)


c1 = LichessApiCommunicator(depth=1)
c2 = ChessComApiCommunicator(depth=1)


games = c1.games_generator("your lichess username", 10, "blitz")
games += c2.games_generator("your chess com username", 10, "blitz")


export_games_to_csv(list(games))
