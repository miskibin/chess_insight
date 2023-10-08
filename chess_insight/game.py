import chess.pgn
from easy_logs import get_logger
from chess_insight.utils import (
    load_eco,
    Color,
    GamePhase,
    Result,
    ResultReason,
    get_pgn,
    get_time_class,
)
from typing import Literal, Annotated
from stockfish import Stockfish
from datetime import datetime
from chess_insight.semi_dataclass import SemiDataclass
from chess_insight.player import Player
from functools import cached_property
from urllib.parse import urlparse
import io


logger = get_logger()


class Game(SemiDataclass):
    _ECO = load_eco()

    _PIECE_ENDGAME_VALUES = {
        "p": 1,
        "P": 1,
        "n": 3,
        "N": 3,
        "q": 8,
        "Q": 8,
        "r": 4,
        "R": 4,
        "b": 3,
        "B": 3,
        "k": 0,
        "K": 0,
    }

    host: Annotated[str, "Server where game was played."]

    username: Annotated[str, "Username of player."]

    time_class: Annotated[
        Literal["bullet", "blitz", "rapid", "classical"], "Time class of game."
    ]

    opening: Annotated[str | None, "Opening name in ECO format."]

    player: Annotated[Player, "Dict containing player data. Determined by `username`."]

    opponent: Annotated[Player, "Dict containing opponent data."]

    url: Annotated[str, "Url to game."]

    def __init__(self, pgn_string: str, usr: str, stockfish: Stockfish = None) -> None:
        self._pgn = get_pgn(pgn_string)
        self._board = chess.pgn.read_game(
            io.StringIO(pgn_string), Visitor=chess.pgn.BoardBuilder
        )
        self.username = usr
        self.time_class = get_time_class(self._pgn)
        self._evaluations = self._get_evaluations(stockfish)
        self.opening, self._opening_end = self._set_opening()
        self.player = Player(
            self._pgn,
            self._board,
            self.player_color,
            self.phases,
            evaluations=self._evaluations,
        )

        self.opponent = Player(
            self._pgn,
            self._board,
            not self.player_color,
            self.phases,
            evaluations=self._evaluations,
        )

    def _get_evaluations(self, stockfish: Stockfish | None) -> list:
        evaluations = []
        total, add_time = map(float, self.time_control.split("+"))
        white_time = black_time = total
        evaluation = 0
        if stockfish:
            stockfish.set_position()
        for move in self._pgn.mainline():
            if stockfish:
                stockfish.make_moves_from_current_position([move.uci()])
                evaluation = stockfish.get_evaluation()
                if evaluation["type"] == "mate":
                    evaluation = evaluation["value"] * 1000
                else:
                    evaluation = evaluation["value"]
            if abs(evaluation) > 1000:
                evaluation = (evaluation / abs(evaluation)) * 1000  # normalize
            if move.turn() == Color.WHITE.value:  # time is added after white move
                time = round((white_time - move.clock()) + add_time, 2)
                white_time = move.clock()
            else:
                time = round((black_time - move.clock()) + add_time, 2)
                black_time = move.clock()
            evaluations.append({"evaluation": evaluation, "time": time})
        return evaluations

    @property
    def host(self) -> str:
        """
        Server where game was played.
        """
        site = urlparse(self._pgn.headers.get("Site"))
        if not site.hostname:
            site = urlparse(self._pgn.headers.get("Link"))
        if not site.hostname:
            raise ValueError(f"Invalid url: {self._pgn.headers.get('Site')}")
        return site.hostname.lower().split("www.")[-1]

    @property
    def url(self) -> str:
        """
        Url to game.
        """
        match self.host:
            case "lichess.org":
                return self._pgn.headers.get("Site")
            case "chess.com":
                return self._pgn.headers.get("Link")
            case _:
                raise ValueError(f"Unknown host: {self.host}")

    @property
    def player_color(self) -> Color:
        """
        Player color in game.
        """
        if self.username.lower() in self._pgn.headers["White"].lower():
            return Color.WHITE
        if self.username.lower() in self._pgn.headers["Black"].lower():
            return Color.BLACK
        raise ValueError(f"Pgn: {self._pgn} \nUsername: {self.username}")

    @property
    def time_control(self) -> str:
        """
        time control in format "time+increment" in seconds.
        e.g. "600+0" or "180+2"
        """
        time_control = self._pgn.headers["TimeControl"].split("/")[-1]
        if "+" not in time_control:
            time_control = time_control + "+0"
        if time_control.count("+") != 1:
            raise ValueError("Invalid timeControl: " + self._pgn.headers["TimeControl"])
        return time_control

    @property
    def date(self) -> datetime:
        """
        Date and time of game in UTC.
        """
        date = self._pgn.headers["UTCDate"]
        time = self._pgn.headers["UTCTime"]
        date_time = datetime.strptime(date + " " + time, "%Y.%m.%d %H:%M:%S")
        return date_time

    @property
    def end_reason(self) -> str:
        """
        Reason of game end.
        """
        comment = self._pgn.end().comment.lower()
        if not comment or comment.startswith("[%clk") and comment.endswith("]"):
            comment = self._pgn.headers.get("Termination").lower()
        reason = None
        if "resigns" in comment or "abandoned" in comment:
            reason = ResultReason.RESIGN
        elif (
            "wins on time" in comment
            or "won on time" in comment
            or "time forfeit" in comment
        ):
            reason = ResultReason.TIMEOUT
        elif "checkmate" in comment:
            reason = ResultReason.MATE
        else:
            logger.debug(f"Unknown result reason: {comment}")
        return reason

    @property
    def result(self) -> Result:
        """
        Result of game. Black, White or Draw.
        """
        res = Result(self._pgn.headers["Result"])

        return res

    def _set_opening(self) -> tuple[str | None, int]:
        """
        Opening name in ECO format.
        Improtant: This method has side effect!!! It sets `self._opening_end`
        """
        board = self._board.copy()
        for _ in range(len(board.move_stack) - len(self._ECO)):
            board.pop()
        for i in range(len(board.move_stack) - 1, -1, -1):
            for opening in self._ECO[i]:
                if opening["fen"] in board.fen():
                    return opening["name"], len(board.move_stack)
            board.pop()
        logger.warning(f"There is no opening in game played {self.date}")
        self._opening_end = 0
        return None, 0

    @property
    def opening_short(self) -> str:
        """
        Short opening name in ECO format.
        e.g. "Sicilian Defense: Alapin Variation" -> "Sicilian Defense"
        """
        return self.opening.split(":")[0]

    @cached_property
    def phases(self) -> dict:
        """
        Phases in half moves
        https://en.wikipedia.org/wiki/Chess_endgame#The_start_of_the_endgame
        """
        game = self._board.copy()
        if self._opening_end == -1:
            raise ValueError("You have to call `self.opening` first")
        board = chess.Board()
        middle_game_end = len(game.move_stack)
        for index, move in enumerate(game.move_stack):
            board.push(move)
            points = sum(
                self._PIECE_ENDGAME_VALUES[str(i)] for i in board.piece_map().values()
            )
            if points < 27:  # if more it is endgame
                middle_game_end = max(index, self._opening_end)
                break
        return {
            GamePhase.OPENING: self._opening_end,
            GamePhase.MIDDLE_GAME: middle_game_end,
            GamePhase.END_GAME: (len(game.move_stack)),
        }


if __name__ == "__main__":
    with open("tests/test_data/barabasz60_chess_com_0.pgn") as f:
        pgn = f.read()
    game = Game(pgn, "barabasz60", Stockfish("stockfish.exe", depth=4))
    from rich import inspect, print

    print(game.render_docs())
    print(game.player.render_docs())
    print(game.asdict())
