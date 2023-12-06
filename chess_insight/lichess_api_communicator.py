from chess_insight.api_communicator import ApiCommunicator
from typing import Generator
import berserk
from easy_logs import get_logger
import os

logger = get_logger()


class LichessApiCommunicator(ApiCommunicator):
    HOST = "lichess.org"
    CLIENT = berserk.Client()

    def get_pgns(self, username: str, count: int, time_class: str) -> list[str]:
        games = self.CLIENT.games.export_by_player(
            username, max=count, perf_type=time_class, as_pgn=True, clocks=True
        )

        try:
            list_of_games = list(games)
        except berserk.exceptions.ResponseError as err:
            logger.error(f"Failed to get games from {self.HOST}: {err}")
            if err.status_code == 404:
                logger.error(f"User {username} doesn't exist on {self.HOST}.")
                raise ValueError(f"User {username} doesn't exist on {self.HOST}.")
            raise err
        if len(list_of_games) < count:
            logger.warning(
                f"User {username} played only {len(list_of_games)} games on {self.HOST}."
            )
        return list_of_games


if __name__ == "__main__":
    lichess = LichessApiCommunicator()

    from pathlib import Path

    tests_path = Path(__file__).parent.parent / "tests" / "test_data"
    username = "drnykterstein"
    games = lichess.get_pgns(username, 5, "blitz")
    for i, game in enumerate(games):
        with open(tests_path / f"{username}_lichess_{i}.pgn", "w") as f:
            f.write(game)

    # pprint(list(lichess.get_games("Pro100wdupe", 1, "rapid")))
