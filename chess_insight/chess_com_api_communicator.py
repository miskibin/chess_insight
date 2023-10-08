from chess_insight.api_communicator import ApiCommunicator
import chessdotcom
from chessdotcom.types import ChessDotComError
from easy_logs import get_logger
from datetime import datetime
from chess_insight.utils import get_time_class, get_pgn

logger = get_logger()


class ChessComApiCommunicator(ApiCommunicator):
    HOST = "chess.com"

    def _get_joined_year(self, usr: str) -> int:
        if not usr:
            logger.error("No username provided")
            return []
        try:
            user = chessdotcom.get_player_profile(usr).json
        except ChessDotComError as err:
            logger.error(f"Failed to get user {usr} from {self.HOST}: {err.text}")
            raise err
        joined = user["player"]["joined"]
        year = datetime.fromtimestamp(joined).year
        logger.debug(f"User {usr} joined in year: {year}")
        return year

    def get_pgns(self, username: str, count: int, time_class: str) -> list[str]:
        joined_year = self._get_joined_year(username)
        games = []
        for y in range(datetime.now().year, joined_year - 1, -1):
            month = int(datetime.now().month) if y == datetime.now().year else 12
            for m in range(month, 0, -1):
                logger.debug(f"Downloading games from {y}-{m}")
                games_list = chessdotcom.get_player_games_by_month_pgn(username, y, m)
                games_list = self.split_pgns(games_list.json["pgn"]["pgn"])
                for g in games_list:
                    if len(games) >= count:
                        return games
                    if get_time_class(get_pgn(g)) == time_class and not (
                        get_pgn(g).headers.get("variant")
                    ):
                        games.append(g)
        logger.warning(
            f"User {username} played only {len(games)} games on {self.HOST}."
        )
        return games


if __name__ == "__main__":
    lichess = ChessComApiCommunicator()
    from rich import print
    from pprint import pprint
    from pathlib import Path

    tests_path = Path(__file__).parent.parent / "tests" / "test_data"
    games = lichess.games_generator("barabasz60", 5, "blitz")
    list_of_games = list(games)
    # for i, game in enumerate(games):
    #     with open(tests_path / f"barabasz60_chess_com_{i}.pgn", "w") as f:
    #         f.write(game)
