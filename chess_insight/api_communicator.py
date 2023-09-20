import json
import os
from abc import ABC
from logging import Logger
from pathlib import Path
from typing import Generator
from abc import abstractmethod
import requests
from stockfish import Stockfish
from easy_logs import get_logger
from chess_insight.game import Game
from rich.progress import track

logger = get_logger()


class ApiCommunicator(ABC):
    HOST: str = None

    def __init__(self, depth: int = 10) -> None:
        """
        Summary:
            Abstract class for API communication. It is used to get games from chess.com, lichess, etc.
            Each subclass should implement get_games method.
        Args:
            logger (Logger): logger to log to
            depth (int, optional): depth of stockfish engine. Defaults to 10.
        """
        try:
            self.stockfish = Stockfish("stockfish.exe", depth=depth)
        except (AttributeError, FileNotFoundError) as err:
            logger.error(
                f"Failed to load stockfish engine: Do you have it installed?  {err}"
            )
            self.stockfish = None

    def split_pgns(self, text_pgn: str) -> list[str]:
        """
        Summary:
            Splits pgn string into list of pgn strings.
        Args:
            text_pgn (str): pgn string to split
        Returns:
            list of pgn strings
        """
        pgns = text_pgn.split("\n\n\n")
        while pgns and len(pgns[-1]) == 0:
            pgns.pop()
        return pgns

    def games_generator(
        self, username: str, count: int, time_class: str
    ) -> Generator[Game, None, None]:
        """
        Args:
            username (str): username on given portal (lichess, chess.com, etc.) to get games from
            list_of_pgns (int): number of pgn strings to compute
        returns:
            generator of Game objects, each representing a game played on chess.com
        """
        list_of_pgns = self.get_pgns(username, count, time_class)
        logger.info(f"Collected {len(list_of_pgns)} games")
        progress = track(
            list_of_pgns,
            description=f"Analyzing games for {username}",
            total=len(list_of_pgns),
            transient=True,
        )
        for game in progress:
            game = Game(
                game,
                username,
                stockfish=self.stockfish,
            )
            yield game

    @abstractmethod
    def get_pgns(
        self, username: str, number_of_games: int, time_class: str
    ) -> Generator[Game, None, None]:
        """
        Args:
            username (str): username on given portal (lichess, chess.com, etc.) to get games from
            games (int): number of lastest games to get
            time_class (_type_): time class of games to get (blitz, rapid, bullet, daily)
        returns:
            generator of Game objects, each representing a game played on chess.com, licess, etc.
        """
