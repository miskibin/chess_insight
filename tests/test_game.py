import pytest
from pathlib import Path
import glob
from chess_insight.game import Game


test_data_path = Path(__file__).parent / "test_data"


class TestGame:
    @pytest.mark.parametrize("pgn_path", glob.glob(str(test_data_path / "*.pgn")))
    def test_game(self, pgn_path):
        usr = self._get_usr(pgn_path)
        with open(pgn_path, "r") as f:
            game = Game(f.read(), usr)
        parsed_game = game.asdict()
        assert None not in parsed_game.values()

    def _get_usr(self, pgn_path: str):
        return Path(pgn_path).stem.split("_")[0]
