from typing import Literal
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from chess_insight import (
    ChessComApiCommunicator,
    LichessApiCommunicator,
    export_games_to_csv,
    export_games_to_json,
)
from textual.app import App
from pydantic import BaseModel, Field, NonNegativeInt, ValidationError


class Queries(BaseModel):
    lichess_username: str = Field(
        help="Provide username for `lichess` (leave blank to skip lichess)",
        default="",
    )
    lichess_games_to_download: NonNegativeInt = Field(
        help="Provide number of games to download from `lichess`", default=10
    )
    chesscom_username: str = Field(
        help="Provide username for chess.com (leave blank to skip chess.com)",
        default="",
    )
    chesscom_games_to_download: NonNegativeInt = Field(
        help="Provide number of games to download from chess.com", default=10
    )
    time_control: Literal["bullet", "blitz", "rapid", "classical"] = Field(
        help="Provide time control (`bullet`, `blitz`, `rapid`, `classical`)",
        default="blitz",
    )
    file_format: Literal["json", "csv"] = Field(
        help="Provide file format for exported data (`csv`, `json`)", default="csv"
    )
    file_name: str = Field(help="Provide file name for exported data", default="games")
    engine_depth: NonNegativeInt = Field(
        help="Provide engine depth for analysis", default=10
    )

    class Config:
        # This is what you need!
        validate_assignment = True


WELCOME_MESSAGE = f"""
# **Welcome to chess-insight interactive mode!**

### Github page: `https://github.com/michalskibinski109/chess-insight`
### PyPI page: `https://pypi.org/project/chess-insight/`
### Author: `michalskibinski109@gmail.com`

# *Have fun!*
"""


def main():
    console = Console()
    md = Markdown(WELCOME_MESSAGE)
    console.print(md)
    queries = Queries()
    for name, query in Queries.model_json_schema()["properties"].items():
        while True:
            answer = console.input(f"{query['help']} default [{query['default']}]: ")
            try:
                queries.__setattr__(name, answer)
                break
            except ValidationError as e:
                console.print(e.errors()[0]["msg"])
                console.print("Try again!")
    console.print(queries)
    console.print("Downloading games...")
    games = list(
        LichessApiCommunicator(queries.engine_depth).games_generator(
            queries.lichess_username,
            queries.lichess_games_to_download,
            queries.time_control,
        )
    )
    games += list(
        ChessComApiCommunicator(queries.engine_depth).games_generator(
            queries.chesscom_username,
            queries.chesscom_games_to_download,
            queries.time_control,
        )
    )
    console.print("Games downloaded!")
    if queries.file_format == "csv":
        export_games_to_csv(games, f"{queries.file_name}.csv")
    else:
        export_games_to_json(games, f"{queries.file_name}.json")


if __name__ == "__main__":
    main()
