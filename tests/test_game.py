import pytest
from pathlib import Path
import glob
import pytest
from chess_insight.game import Game
from chess_insight.player import Player
from stockfish import Stockfish
from datetime import datetime
import os

from stockfish import Stockfish

test_data_path = Path(__file__).parent / "test_data"


class TestGame:
    def test_FR3_game_properties(self):
        pgn_string = Path(test_data_path / "drnykterstein_lichess_0.pgn").read_text()
        game = Game(pgn_string, "DrNykterstein")

        assert game.host == "lichess.org"
        assert game.username == "DrNykterstein"
        assert game.time_class == "blitz"
        assert game.opening == "Nimzo-Larsen Attack: Classical Variation"
        assert game.url == "https://lichess.org/kx7aGZB0"
        assert isinstance(game.player, Player)
        assert isinstance(game.opponent, Player)
        assert game.result.value == "1-0"
        assert game.player.elo == 3113
        assert game.opponent.elo == 2718
        assert game.date == datetime(2023, 7, 1, 21, 56, 43)

    @pytest.mark.parametrize(
        "pgn_path",
        glob.glob(str(test_data_path / "*.pgn")),
        ids=[
            os.path.basename(path) for path in glob.glob(str(test_data_path / "*.pgn"))
        ],
    )
    def test_FR3_game(self, pgn_path):
        usr = self._get_usr(pgn_path)
        with open(pgn_path, "r") as f:
            game = Game(f.read(), usr)
        parsed_game = game.asdict()
        assert None not in parsed_game.values()

    def _get_usr(self, pgn_path: str):
        return Path(pgn_path).stem.split("_")[0]

    def test_FR4_stockfish_integration(self):
        pgn_string = Path(test_data_path / "drnykterstein_lichess_0.pgn").read_text()
        username = "drnykterstein"
        depth = 1  # depth of the game analysis
        # Initialize the Stockfish engine with the specified depth
        stockfish = Stockfish(depth=depth)
        # Initialize the Game object with the Stockfish engine
        game = Game(pgn_string, username, stockfish)
        # Perform the game analysis
        evaluations = game._get_evaluations(stockfish)
        # Check if the game analysis is performed correctly
        assert evaluations is not None
        assert isinstance(evaluations, list)
        assert all(isinstance(evaluation, dict) for evaluation in evaluations)
