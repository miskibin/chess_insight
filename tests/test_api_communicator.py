import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from chess_insight.api_communicator import ApiCommunicator
from chess_insight.lichess_api_communicator import LichessApiCommunicator
from chess_insight.chess_com_api_communicator import ChessComApiCommunicator


class MockApiCommunicator(ApiCommunicator):
    def get_pgns(self):
        pass


class ConcreteApiCommunicator(ApiCommunicator):
    def get_pgns(self, username, months, time_class):
        return super().get_pgns(username, months, time_class)


class TestApiCommunicator:
    @patch("chess_insight.api_communicator.get_logger")
    def test_FR1_init(self, mock_logger):
        mock_logger.return_value.warning = MagicMock()
        api_communicator = MockApiCommunicator("non_existent_path")
        assert api_communicator.stockfish is None

    def test_FR1_split_pgns(self):
        api_communicator = MockApiCommunicator()
        result = api_communicator.split_pgns("pgn1\n\n\npgn2\n\n\n")
        assert result == ["pgn1", "pgn2"]

    @patch("chess_insight.api_communicator.Game")
    @patch.object(MockApiCommunicator, "get_pgns")
    def test_FR1_games_generator(self, mock_get_pgns, mock_game):
        api_communicator = MockApiCommunicator()
        mock_get_pgns.return_value = ["pgn1", "pgn2"]
        mock_game.return_value = "game"
        result = list(api_communicator.games_generator("username", 2, "time_class"))
        assert result == ["game", "game"]

    @patch("chessdotcom.get_player_games_by_month_pgn")
    @patch("chessdotcom.get_player_profile")
    @patch("chess_insight.chess_com_api_communicator.get_time_class")
    @patch("chess_insight.chess_com_api_communicator.get_pgn")
    def test_FR1_get_pgns_chess_com(
        self,
        mock_get_pgn,
        mock_get_time_class,
        mock_get_player_profile,
        mock_get_player_games_by_month_pgn,
    ):
        mock_get_player_profile.return_value.json = {
            "player": {"joined": 946684800}
        }  # 2000-01-01
        mock_get_player_games_by_month_pgn.return_value.json = {
            "pgn": {"pgn": "pgn1\n\n\npgn2\n\n\n"}
        }
        mock_get_time_class.return_value = "blitz"
        mock_get_pgn.return_value.headers = {}
        api_communicator = ChessComApiCommunicator()
        result = api_communicator.get_pgns("username", 2, "blitz")
        assert result == ["pgn1", "pgn2"]

    # Add similar test for lichess.org API
    @patch.object(LichessApiCommunicator, "CLIENT")
    def test_FR1_get_pgns_lichess(self, mock_client):
        mock_export_by_player = MagicMock()
        mock_export_by_player.return_value = ["pgn1", "pgn2"]
        mock_client.games.export_by_player = mock_export_by_player
        lichess_api_communicator = LichessApiCommunicator()
        result = lichess_api_communicator.get_pgns("username", 2, "time_class")
        assert result == ["pgn1", "pgn2"]

    @patch.object(ConcreteApiCommunicator, "get_pgns")
    def test_FR2_get_pgns_filtering(self, mock_get_pgns):
        mock_get_pgns.return_value = ["pgn1", "pgn2"]
        api_communicator = ConcreteApiCommunicator()
        result = api_communicator.get_pgns("username", 2, "time_class")
        mock_get_pgns.assert_called_once_with("username", 2, "time_class")
        assert result == ["pgn1", "pgn2"]
