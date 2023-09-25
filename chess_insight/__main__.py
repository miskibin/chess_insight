from typing import Literal
from rich.console import Console
from rich.markdown import Markdown
from chess_insight import (
    ChessComApiCommunicator,
    LichessApiCommunicator,
    export_games_to_csv,
    export_games_to_json,
)
from pydantic import BaseModel, Field, NonNegativeInt, ValidationError
from pathlib import Path

STOCKFISH_PATH = Path(__file__).parent.parent / "stockfish.exe"


class HostSpecific(BaseModel):
    username: str = Field(
        None,
        help="Provide username (leave blank to skip)",
    )
    games_to_download: NonNegativeInt = Field(
        help="Provide number of games to download ", default=10
    )

    def __hash__(self):  # make hashable BaseModel subclass
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
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
        validate_assignment = True


WELCOME_MESSAGE = f"""
# **Welcome to chess_insight interactive mode!**

### Github page: `https://github.com/michalskibinski109/chess_insight`
### PyPI page: `https://pypi.org/project/chess_insight/`
### Author: `michalskibinski109@gmail.com`

# *Have fun!*
"""


def input_model_data(console, model: BaseModel) -> BaseModel:
    for name, query in model.model_json_schema()["properties"].items():
        while True:
            answer = console.input(f"{query['help']} default `{query['default']}`: ")
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
    console.print("General questions:", style="bold green ", justify="center")
    general: GenericQueries = input_model_data(console, GenericQueries())
    console.print("lichess.org specific:", style="bold blue", justify="center")
    lichess: HostSpecific = input_model_data(console, HostSpecific())
    console.print("chess.com specific:", style="bold blue", justify="center")
    chess_com: HostSpecific = input_model_data(console, HostSpecific())
    console.print(general, lichess, chess_com)
    HOSTS = {
        chess_com: ChessComApiCommunicator(STOCKFISH_PATH, depth=general.engine_depth),
        lichess: LichessApiCommunicator(STOCKFISH_PATH, depth=general.engine_depth),
    }
    console.print("Downloading games...")
    games = []
    for config, communicator in HOSTS.items():
        if not config:
            continue
        games += list(
            communicator.games_generator(
                config.username,
                config.games_to_download,
                general.time_control,
            )
        )
    console.print("Games downloaded!")
    if general.file_format == "csv":
        df = export_games_to_csv(games, f"{general.file_name}.csv")
        console.print("Games exported to {general.file_name}.csv!")
        console.print(df.head())
    else:
        export_games_to_json(games, f"{general.file_name}.json")
        console.print("Games exported to {general.file_name}.json!")
        console.print(games[0].asdict())


if __name__ == "__main__":
    main()
