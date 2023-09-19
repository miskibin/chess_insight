from easy_logs import get_logger
from chess_insight.semi_dataclass import SemiDataclass
from chess_insight.utils import Color, GamePhase, Mistakes
import chess.pgn
from collections import defaultdict
from statistics import mean

logger = get_logger()


class Player(SemiDataclass):
    def __init__(
        self,
        pgn: chess.pgn.Game,
        board: chess.Board,
        color: Color,
        game_phases: tuple,
        evaluations: list,
    ) -> None:
        self._pgn = pgn
        self._board = board
        self._color = color
        self._phases = game_phases
        self._evaluations = (
            evaluations  # [{'evaluation': float, 'time': float},] only for given color
        )

    @property
    def elo(self) -> int:
        """
        elo of player at the time of game.
        """
        prop_name = {
            Color.WHITE: "WhiteElo",
            Color.BLACK: "BlackElo",
        }
        return int(self._pgn.headers[prop_name[self._color]])

    @property
    def avg_move_time(self) -> dict:
        """
        list with average move time for each phase.
        """
        if len(self._evaluations) < 3:
            return {}
        idx = 0 if self._color == Color.WHITE else 1
        times = [item["time"] for item in self._evaluations]
        return {
            GamePhase.OPENING: mean(times[idx : self._phases[GamePhase.OPENING] : 2]),
            GamePhase.MIDDLE_GAME: mean(
                times[idx : self._phases[GamePhase.MIDDLE_GAME] : 2]
            ),
            GamePhase.END_GAME: mean(times[idx : self._phases[GamePhase.END_GAME] : 2]),
        }

    @property
    def accuracy(self) -> dict:
        """
        dict with number of mistakes for each phase.
        """
        idx = 0 if self._color == Color.WHITE else 1
        mul = 1 if self._color == Color.WHITE else -1
        mist = [item["evaluation"] for item in self._evaluations]
        last_eval = last_idx = 0  # we need to track last eval from phase before
        data = defaultdict(dict)
        for phase in GamePhase:  # intEnum
            evals = [last_eval] + mist[
                last_idx : self._phases[phase]
            ]  # get all moves from given phase
            last_idx = self._phases[phase]
            for mistake_type in Mistakes:
                data[phase][mistake_type] = sum(
                    (mul * mistake_type.value < evals[i - 1] - evals[i])
                    for i in range(idx, len(evals) // 2, 2)
                )
        return data
