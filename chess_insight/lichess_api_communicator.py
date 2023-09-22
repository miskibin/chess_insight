from chess_insight.api_communicator import ApiCommunicator
from typing import Generator
import berserk
from easy_logs import get_logger
import os
from rich.status import Status

logger = get_logger()


class LichessApiCommunicator(ApiCommunicator):
    HOST = "lichess.org"
    CLIENT = berserk.Client()

    def get_pgns(self, username: str, count: int, time_class: str) -> list[str]:
        stat = Status(f"Downloading {count} games from {self.HOST}")
        stat.start()
        games = self.CLIENT.games.export_by_player(
            username, max=count, perf_type=time_class, as_pgn=True, clocks=True
        )
        stat.stop()
        list_of_games = list(games)
        if len(list_of_games) < count:
            logger.warning(
                f"User {username} played only {len(list_of_games)} games on {self.HOST}."
            )
        return list_of_games


if __name__ == "__main__":
    lichess = LichessApiCommunicator()

    from pathlib import Path

    tests_path = Path(__file__).parent.parent / "tests" / "test_data"
    games = lichess.games_generator("pro100wdupe", 5, "rapid")
    for game in games:
        print(game.asdict())
    # for i, game in enumerate(games):
    #     with open(tests_path / f"pro100wdupe_lichess_{i}.pgn", "w") as f:
    #         f.write(game)

    # pprint(list(lichess.get_games("Pro100wdupe", 1, "rapid")))
    # valid = lichess.get_valid_username("michal")
    # pprint(valid)
