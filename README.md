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

c1 = LichessApiCommunicator()
c2 = ChessComApiCommunicator()

games = list(c1.games_generator("your lichess username", 10, "blitz"))
games += list(c2.games_generator("your chess com username", 10, "blitz"))
```

- export games to csv

```python 
chess_insight.export_games_to_csv(list(games))
```
 


| date                | host        | opening                               | opening_short    | opponent_accuracy_opening_inaccuracy | opponent_accuracy_opening_mistake | opponent_accuracy_opening_blunder | opponent_accuracy_middle_game_inaccuracy | opponent_accuracy_middle_game_mistake | opponent_accuracy_middle_game_blunder | opponent_accuracy_end_game_inaccuracy | opponent_accuracy_end_game_mistake | opponent_accuracy_end_game_blunder | opponent_avg_move_time_opening | opponent_avg_move_time_middle_game | opponent_avg_move_time_end_game | opponent_elo | phases_opening | phases_middle_game | phases_end_game | player_accuracy_opening_inaccuracy | player_accuracy_opening_mistake | player_accuracy_opening_blunder | player_accuracy_middle_game_inaccuracy | player_accuracy_middle_game_mistake | player_accuracy_middle_game_blunder | player_accuracy_end_game_inaccuracy | player_accuracy_end_game_mistake | player_accuracy_end_game_blunder | player_avg_move_time_opening | player_avg_move_time_middle_game | player_avg_move_time_end_game | player_elo | player_color | result               | time_class | time_control | url                          | username    |
| ------------------- | ----------- | ------------------------------------- | ---------------- | ------------------------------------ | --------------------------------- | --------------------------------- | ---------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- | ---------------------------------- | ---------------------------------- | ------------------------------ | ---------------------------------- | ------------------------------- | ------------ | -------------- | ------------------ | --------------- | ---------------------------------- | ------------------------------- | ------------------------------- | -------------------------------------- | ----------------------------------- | ----------------------------------- | ----------------------------------- | -------------------------------- | -------------------------------- | ---------------------------- | -------------------------------- | ----------------------------- | ---------- | ------------ | -------------------- | ---------- | ------------ | ---------------------------- | ----------- |
| 2022-05-26 16:51:04 | lichess.org | Pirc Defense: Classical Variation     | Pirc Defense     | 2                                    | 2                                 | 2                                 | 10                                       | 11                                    | 11                                    | 0                                     | 0                                  | 0                                  | 0.25                           | 2.88                               | 2.88                            | 1737         | 8              | 51                 | 51              | 1                                  | 0                               | 0                               | 2                                      | 1                                   | 1                                   | 0                                   | 0                                | 0                                | 1.0                          | 2.2308                           | 2.2308                        | 1779       | white        | ['white', 'timeout'] | blitz      | 180+0        | https://lichess.org/vf8yqCKh | pro100wdupe |
| 2022-05-11 20:26:37 | lichess.org | Vienna Game                           | Vienna Game      | 1                                    | 1                                 | 1                                 | 8                                        | 9                                     | 9                                     | 14                                    | 14                                 | 14                                 | 0.0                            | 2.875                              | 2.2692                          | 1792         | 3              | 48                 | 104             | 0                                  | 0                               | 0                               | 3                                      | 2                                   | 2                                   | 0                                   | 0                                | 0                                | 1.5                          | 5.9167                           | 3.3462                        | 1790       | white        | ['black', 'timeout'] | blitz      | 180+0        | https://lichess.org/PjE2bZ8r | pro100wdupe |
| 2022-05-11 20:22:35 | lichess.org | Sicilian Defense: Chekhover Variation | Sicilian Defense | 0                                    | 0                                 | 0                                 | 1                                        | 1                                     | 1                                     | 0                                     | 0                                  | 0                                  | 1.0                            | 6.2                                | 6.2                             | 1772         | 7              | 30                 | 30              | 2                                  | 2                               | 2                               | 5                                      | 5                                   | 5                                   | 0                                   | 0                                | 0                                | 0.3333                       | 5.9333                           | 5.9333                        | 1778       | black        | ['black', 'timeout'] | blitz      | 180+0        | https://lichess.org/y1OSLD9A | pro100wdupe |
| 2022-05-05 07:52:37 | lichess.org | Indian Defense: Knights Variation     | Indian Defense   | 0                                    | 0                                 | 0                                 | 1                                        | 1                                     | 1                                     | 4                                     | 1                                  | 1                                  | 0.0                            | 1.7917                             | 2.5211                          | 1789         | 3              | 48                 | 142             | 1                                  | 1                               | 1                               | 11                                     | 11                                  | 11                                  | 18                                  | 22                               | 22                               | 0.0                          | 2.3333                           | 2.2676                        | 1778       | black        | ['draw', 'timeout']  | blitz      | 180+0        | https://lichess.org/Yn1BxD8r | pro100wdupe |


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
