# Chess-insights

Modern package for analyzing chess games. It provides method to download games from `lichess.org` and `chess.com` and analyze them using `stockfish` engine. Parses games to `Game` object which contains all information about game and players. `Game` object can be converted to `dict` or `json` for further processing.

## Installation

```bash
pip install chess-insights
```

## Game

| Attribute       | Description                                                                                               |
| --------------- | --------------------------------------------------------------------------------------------------------- |
| `color`         | Player color in game.                                                                                     |
| `time_control`  | time control in format "time+increment" in seconds.         e.g. "600+0" or "180+2"                       |
| `date`          | Date and time of game in UTC.                                                                             |
| `result`        | Returns tuple (result, reason)         eg:         (white, resign) -> white won by resignation            |
| `opening_short` | Short opening name in ECO format.         e.g. "Sicilian Defense: Alapin Variation" -> "Sicilian Defense" |
| `phases`        | Phases in half moves         https://en.wikipedia.org/wiki/Chess_endgame#The_start_of_the_endgame         |
| `host`          | Server where game was played.                                                                             |
| `username`      | Username of player.                                                                                       |
| `time_class`    | Time class of game.                                                                                       |
| `opening`       | Opening name in ECO format.                                                                               |
| `player`        | Dict containing player data. Determined by `username`.                                                    |
| `opponent`      | Dict containing opponent data.                                                                            |

## Player

| Attribute                 | Description                                  |
| ------------------------- | -------------------------------------------- |
| `elo`                     | elo of player at the time of game.           |
| `avg_move_time_per_phase` | list with average move time for each phase.  |
| `mistakes_per_phase`      | dict with number of mistakes for each phase. |



- example game:

```python
game.as_dict()
```

```json
{
    "color": "white",
    "date": datetime.datetime(2022, 5, 26, 16, 51, 4),
    "host": "lichess.org",
    "opening": "Pirc Defense: Classical Variation",
    "opening_short": "Pirc Defense",
    "opponent": {
        "avg_move_time_per_phase": {"opening": 1.25, "middle_game": 2.3846, "end_game": 2.3846},
        "elo": 1737,
        "mistakes_per_phase": {
            "opening": {"inaccuracy": 2, "mistake": 2, "blunder": 2},
            "middle_game": {"inaccuracy": 10, "mistake": 11, "blunder": 11},
            "end_game": {"inaccuracy": 0, "mistake": 0, "blunder": 0}
        }
    },
    "phases": {"opening": 8, "middle_game": 51, "end_game": 51},
    "player": {
        "avg_move_time_per_phase": {"opening": 1.0, "middle_game": 2.0769, "end_game": 2.0769},
        "elo": 1779,
        "mistakes_per_phase": {
            "opening": {"inaccuracy": 1, "mistake": 0, "blunder": 0},
            "middle_game": {"inaccuracy": 1, "mistake": 1, "blunder": 1},
            "end_game": {"inaccuracy": 0, "mistake": 0, "blunder": 0}
        }
    },
    "result": ["white", "resign"],
    "time_class": "blitz",
    "time_control": "180+0",
    "username": "pro100wdupe"
}
```