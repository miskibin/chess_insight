import pytest
from unittest.mock import MagicMock
from chess_insight.player import Player
from chess_insight.utils import Color, GamePhase, Mistakes
import chess


class TestPlayer:
    def test_init(self):
        pgn = chess.pgn.Game()
        board = chess.Board()
        color = Color.WHITE
        game_phases = (1, 2, 3)
        evaluations = [{"evaluation": 1.0, "time": 2.0}]
        player = Player(pgn, board, color, game_phases, evaluations)
        assert player._pgn == pgn
        assert player._board == board
        assert player._color == color
        assert player._phases == game_phases
        assert player._evaluations == evaluations

    def test_elo(self):
        pgn = chess.pgn.Game()
        pgn.headers["WhiteElo"] = "2000"
        player = Player(
            pgn,
            chess.Board(),
            Color.WHITE,
            (1, 2, 3),
            [{"evaluation": 1.0, "time": 2.0}],
        )
        assert player.elo == 2000
