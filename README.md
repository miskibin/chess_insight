[![PyPI version](https://badge.fury.io/py/chess-insight.svg)](https://badge.fury.io/py/chess-insight)


# Chess-insight

__Modern package for analyzing chess games.__
 
### Features:
1. Download games from `lichess.org` and `chess.com`
2. Analyze games using set of custom methods and `stockfish-16` engine.
3. Parses games to `Game` object which contains all information about game and players to python object and `json`.
4. Provides method for exporting list of analyzed games to `csv`

## Installation

```bash
pip install chess-insight
```

## Usage

- get games 

```python
from chess_insight import ChessComApiCommunicator, LichessApiCommunicator

c1 = LichessApiCommunicator(depth=1)
c2 = ChessComApiCommunicator(depth=1)

games = c1.games_generator("your lichess username", 10, "blitz")
games += c2.games_generator("your chess com username", 10, "blitz")
```

- export games to csv

```python 
chess_insight.export_games_to_csv(list(games))
```

- get games as dict

```python
for game in games:
    print(game.asdict())
```

## Architecture 

### Game object

| Attribute          | Description                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| `host`             | Server where game was played.                                                                     |
| `url`              | Url to game.                                                                                      |
| `player_color`     | Player color in game.                                                                             |
| `time_control`     | time control in format "time+increment" in seconds.         e.g. "600+0" or "180+2"               |
| `date`             | Date and time of game in UTC.                                                                     |
| `result`           | Returns tuple (result, reason)         eg:         (white, resign) -> white won by resignation    |
| `opening_short`    | Short opening name in ECO format.         e.g. "Sicilian Defense: Alapin Variation" ->            |
| "Sicilian Defense" |
| `phases`           | Phases in half moves         https://en.wikipedia.org/wiki/Chess_endgame#The_start_of_the_endgame |  | `host` | Server where game was played. |
| `username`         | Username of player.                                                                               |
| `time_class`       | Time class of game.                                                                               |
| `opening`          | Opening name in ECO format.                                                                       |
| `player`           | Dict containing player data. Determined by `username`.                                            |
| `opponent`         | Dict containing opponent data.                                                                    |
| `url`              | Url to game.                                                                                      |

### Player object

| Attribute       | Description                                  |
| --------------- | -------------------------------------------- |
| `elo`           | elo of player at the time of game.           |
| `avg_move_time` | list with average move time for each phase.  |
| `accuracy`      | dict with number of mistakes for each phase. |


- example game:

```python
game.asdict()
```

```json
{
    "player_color": "white",
    "date": datetime.datetime(2023, 9, 14, 21, 57, 47),
    "host": "chess.com",
    "opening": "Sicilian Defense: Closed, Traditional",
    "opening_short": "Sicilian Defense",
    "opponent": {
        "accuracy": {
            "opening": {"inaccuracy": 1, "mistake": 1, "blunder": 1},
            "middle_game": {"inaccuracy": 13, "mistake": 13, "blunder": 15},
            "end_game": {"inaccuracy": 6, "mistake": 7, "blunder": 7}
        },
        "avg_move_time": {"opening": 1.2, "middle_game": 5.1906, "end_game": 3.9467},
        "elo": 1603
    },
    "phases": {"opening": 4, "middle_game": 64, "end_game": 91},
    "player": {
        "accuracy": {
            "opening": {"inaccuracy": 0, "mistake": 0, "blunder": 0},
            "middle_game": {"inaccuracy": 1, "mistake": 1, "blunder": 1},
            "end_game": {"inaccuracy": 1, "mistake": 1, "blunder": 1}
        },
        "avg_move_time": {"opening": 1.65, "middle_game": 3.4875, "end_game": 3.0109},
        "elo": 1619
    },
    "result": ["white", "timeout"],
    "time_class": "blitz",
    "time_control": "180+0",
    "url": "https://www.chess.com/game/live/88467619273",
    "username": "barabasz60"
}
```
