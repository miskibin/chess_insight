from chess_insight.chess_com_api_communicator import ChessComApiCommunicator
from chess_insight.lichess_api_communicator import LichessApiCommunicator
from chess_insight.game import Game
import pandas as pd
from easy_logs import get_logger

logger = get_logger()


def export_games_to_csv(games: list, file_name: str = "games.csv"):
    json_data = [game.flatten() for game in games]
    df = pd.DataFrame(json_data)
    df.to_csv(file_name, index=False)
    logger.info(f"Saved {len(games)} games to {file_name}")
