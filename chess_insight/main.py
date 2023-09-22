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


class HostSpecific(BaseModel):
    username: str = Field(
        help="Provide username (leave blank to skip)",
        default="pro100wdupe",
    )
    games_to_download: NonNegativeInt = Field(
        help="Provide number of games to download ", default=10
    )

    class Config:
        # This is what you need!
        validate_assignment = True


class GenericQueries(BaseModel):
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


def input_model_data(console, model: BaseModel) -> BaseModel:
    for name, query in model.model_json_schema()["properties"].items():
        while True:
            answer = console.input(f"{query['help']} default [{query['default']}]: ")
            if name == "username" and answer == "":
                return None
            if answer == "":
                break
            try:
                model.__setattr__(name, answer)
                break
            except ValidationError as e:
                console.print(e.errors()[0]["msg"])
                console.print("Try again!")
    return model


def main():
    console = Console()
    md = Markdown(WELCOME_MESSAGE)
    console.print(md)
    console.print("General questions:")
    general: GenericQueries = input_model_data(console, GenericQueries())
    console.print("lichess.org specific:")
    lichess: HostSpecific = input_model_data(console, HostSpecific())
    console.print("chess.com specific:")
    chess: HostSpecific = input_model_data(console, HostSpecific())
    console.print(general, lichess, chess)
    console.print("Downloading games...")
    if lichess:
        games = list(
            LichessApiCommunicator(general.engine_depth).games_generator(
                lichess.username,
                lichess.games_to_download,
                general.time_control,
            )
        )
    if chess:
        games += list(
            ChessComApiCommunicator(general.engine_depth).games_generator(
                chess.username,
                chess.games_to_download,
                general.time_control,
            )
        )
    console.print("Games downloaded!")
    if general.file_format == "csv":
        export_games_to_csv(games, f"{general.file_name}.csv")
    else:
        export_games_to_json(games, f"{general.file_name}.json")


if __name__ == "__main__":
    main()
