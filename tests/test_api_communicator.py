import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from chess_insight.api_communicator import ApiCommunicator


class MockApiCommunicator(ApiCommunicator):
    def get_pgns(self):
        pass


class TestApiCommunicator:
    @patch("chess_insight.api_communicator.get_logger")
    def test_init(self, mock_logger):
        mock_logger.return_value.warning = MagicMock()
        api_communicator = MockApiCommunicator("non_existent_path")
        assert api_communicator.stockfish is None

    def test_split_pgns(self):
        api_communicator = MockApiCommunicator()
        result = api_communicator.split_pgns("pgn1\n\n\npgn2\n\n\n")
        assert result == ["pgn1", "pgn2"]

    @patch("chess_insight.api_communicator.Game")
    @patch.object(MockApiCommunicator, "get_pgns")
    def test_games_generator(self, mock_get_pgns, mock_game):
        api_communicator = MockApiCommunicator()
        mock_get_pgns.return_value = ["pgn1", "pgn2"]
        mock_game.return_value = "game"
        result = list(api_communicator.games_generator("username", 2, "time_class"))
        assert result == ["game", "game"]
