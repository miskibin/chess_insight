import io

import chess.pgn
from typing import Literal
from enum import IntEnum, Enum
from pathlib import Path
import os
import json


class Color(IntEnum):
    WHITE = 1
    BLACK = 0


class GamePhase(Enum):
    OPENING = "opening"
    MIDDLE_GAME = "middle_game"
    END_GAME = "end_game"


class Mistakes(IntEnum):
    INACCURACY = 50
    MISTAKE = 120
    BLUNDER = 200


class ResultReason(IntEnum):
    INSSUFICIENT_MATERIAL = 4
    REPETITION = 3
    RESIGN = 2
    TIMEOUT = 1
    MATE = 0


class Result(Enum):
    WHITE = "1-0"
    BLACK = "0-1"
    DRAW = "1/2-1/2"
    ON_GOING = "*"


def get_pgn(pgn: str) -> chess.pgn.Game:
    """extracts a pgn file."""
    pgn = io.StringIO(pgn)
    game = chess.pgn.read_game(pgn)
    return game


def get_time_class(
    pgn: chess.pgn.Game,
) -> Literal["bullet", "blitz", "rapid", "classical"]:
    time_control = pgn.headers["TimeControl"]
    time_control = time_control.split("/")[-1]  # daily time control
    if time_control.count("+") > 1:
        raise ValueError(f'Invalid time control: {pgn.headers["TimeControl"]}')
    time = int(time_control.split("+")[0])
    if time < 180:
        return "bullet"
    if time < 600:
        return "blitz"
    if time < 1800:
        return "rapid"
    return "classical"


def load_eco() -> list[str]:
    with open(
        os.path.join(Path(__file__).parent / "data" / Path("openings.json")),
        encoding="utf-8",
    ) as f:
        eco = json.load(f)
    return eco
