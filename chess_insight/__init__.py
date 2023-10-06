from chess_insight.chess_com_api_communicator import ChessComApiCommunicator
from chess_insight.lichess_api_communicator import LichessApiCommunicator
from chess_insight.game import Game
import pandas as pd
from easy_logs import get_logger
from pathlib import Path

logger = get_logger()


def get_communicator(host: str, engine_depth: int = None, engine_path: Path = None):
    HOSTS = {
        "chess.com": ChessComApiCommunicator(engine_path, depth=engine_depth),
        "lichess.org": LichessApiCommunicator(engine_path, depth=engine_depth),
    }
    return HOSTS[host]


def export_games_to_csv(games: list, file_name: str = "games.csv") -> pd.DataFrame:
    logger.debug(f"Saving {len(games)} games to {file_name}")
    json_data = [game.flatten() for game in games]
    df = pd.DataFrame(json_data)
    df.to_csv(file_name, index=False)
    logger.info(f"Saved {len(games)} games to {file_name}")
    return df


def export_games_to_json(games: list, file_name: str = "games.json"):
    logger.info(f"Saving {len(games)} games to {file_name}")
    json_data = [game.asdict() for game in games]
    df = pd.DataFrame(json_data)
    df.to_json(file_name, index=False)
    logger.info(f"Saved {len(games)} games to {file_name}")
