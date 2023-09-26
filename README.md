[![PyPI version](https://badge.fury.io/py/chess_insight.svg)](https://badge.fury.io/py/chess_insight)


# chess_insight

__Modern application for gathering chess data and analyzing chess games.__

 
### Features:
1. Download games from `lichess.org` and `chess.com`
2. Analyze games using set of custom methods and `stockfish-16` engine.
3. Parses games to `Game` object which contains all information about game and players to python object and `json`.
4. Provides method for exporting list of analyzed games to `csv`

## interactive mode
![image](https://github.com/michalskibinski109/chess_insight/assets/77834536/6bb89db2-ae38-423f-991f-eb696377b38a)


### installation
1.  ```bash
    pip install chess_insight # download application
    ```
2. [Optional] Download stockfish-16 from [here](https://stockfishchess.org/download/)


3.  ```bash
    python -m chess_insight # run app
    ```
Now answer questions and have fun with [csv](#csv) or [json](#json) data



## Python module

```bash
pip install chess_insight
```
 [Optional] Download stockfish-16 from [here](https://stockfishchess.org/download/)




## Usage

- get games 

```python
from chess_insight import ChessComApiCommunicator, LichessApiCommunicator

c1 = LichessApiCommunicator("path/to/stockfish")
c2 = ChessComApiCommunicator("path/to/stockfish" # if blank stocfish wont be used
)

games = list(c1.games_generator("your lichess username", 10, "blitz"))
games += list(c2.games_generator("your chess com username", 10, "blitz"))
```

- export games to csv

```python 
chess_insight.export_games_to_csv(list(games))
```
 
#### CSV 

| date                | host        | opening                               | opening_short    | opponent_accuracy_opening_inaccuracy | opponent_accuracy_opening_mistake | opponent_accuracy_opening_blunder | opponent_accuracy_middle_game_inaccuracy | opponent_accuracy_middle_game_mistake | opponent_accuracy_middle_game_blunder | opponent_accuracy_end_game_inaccuracy | opponent_accuracy_end_game_mistake | opponent_accuracy_end_game_blunder | opponent_avg_move_time_opening | opponent_avg_move_time_middle_game | opponent_avg_move_time_end_game | opponent_elo | phases_opening | phases_middle_game | phases_end_game | player_accuracy_opening_inaccuracy | player_accuracy_opening_mistake | player_accuracy_opening_blunder | player_accuracy_middle_game_inaccuracy | player_accuracy_middle_game_mistake | player_accuracy_middle_game_blunder | player_accuracy_end_game_inaccuracy | player_accuracy_end_game_mistake | player_accuracy_end_game_blunder | player_avg_move_time_opening | player_avg_move_time_middle_game | player_avg_move_time_end_game | player_elo | player_color | result               | time_class | time_control | url                          | username    |
| ------------------- | ----------- | ------------------------------------- | ---------------- | ------------------------------------ | --------------------------------- | --------------------------------- | ---------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- | ---------------------------------- | ---------------------------------- | ------------------------------ | ---------------------------------- | ------------------------------- | ------------ | -------------- | ------------------ | --------------- | ---------------------------------- | ------------------------------- | ------------------------------- | -------------------------------------- | ----------------------------------- | ----------------------------------- | ----------------------------------- | -------------------------------- | -------------------------------- | ---------------------------- | -------------------------------- | ----------------------------- | ---------- | ------------ | -------------------- | ---------- | ------------ | ---------------------------- | ----------- |
| 2022-05-26 16:51:04 | lichess.org | Pirc Defense: Classical Variation     | Pirc Defense     | 2                                    | 2                                 | 2                                 | 10                                       | 11                                    | 11                                    | 0                                     | 0                                  | 0                                  | 0.25                           | 2.88                               | 2.88                            | 1737         | 8              | 51                 | 51              | 1                                  | 0                               | 0                               | 2                                      | 1                                   | 1                                   | 0                                   | 0                                | 0                                | 1.0                          | 2.2308                           | 2.2308                        | 1779       | white        | ["white", "timeout"] | blitz      | 180+0        | https://lichess.org/vf8yqCKh | pro100wdupe |
| 2022-05-11 20:26:37 | lichess.org | Vienna Game                           | Vienna Game      | 1                                    | 1                                 | 1                                 | 8                                        | 9                                     | 9                                     | 14                                    | 14                                 | 14                                 | 0.0                            | 2.875                              | 2.2692                          | 1792         | 3              | 48                 | 104             | 0                                  | 0                               | 0                               | 3                                      | 2                                   | 2                                   | 0                                   | 0                                | 0                                | 1.5                          | 5.9167                           | 3.3462                        | 1790       | white        | ["black", "timeout"] | blitz      | 180+0        | https://lichess.org/PjE2bZ8r | pro100wdupe |
| 2022-05-11 20:22:35 | lichess.org | Sicilian Defense: Chekhover Variation | Sicilian Defense | 0                                    | 0                                 | 0                                 | 1                                        | 1                                     | 1                                     | 0                                     | 0                                  | 0                                  | 1.0                            | 6.2                                | 6.2                             | 1772         | 7              | 30                 | 30              | 2                                  | 2                               | 2                               | 5                                      | 5                                   | 5                                   | 0                                   | 0                                | 0                                | 0.3333                       | 5.9333                           | 5.9333                        | 1778       | black        | ["black", "timeout"] | blitz      | 180+0        | https://lichess.org/y1OSLD9A | pro100wdupe |
| 2022-05-05 07:52:37 | lichess.org | Indian Defense: Knights Variation     | Indian Defense   | 0                                    | 0                                 | 0                                 | 1                                        | 1                                     | 1                                     | 4                                     | 1                                  | 1                                  | 0.0                            | 1.7917                             | 2.5211                          | 1789         | 3              | 48                 | 142             | 1                                  | 1                               | 1                               | 11                                     | 11                                  | 11                                  | 18                                  | 22                               | 22                               | 0.0                          | 2.3333                           | 2.2676                        | 1778       | black        | ["draw", "timeout"]  | blitz      | 180+0        | https://lichess.org/Yn1BxD8r | pro100wdupe |


- get games as dict

```python
for game in games:
    print(game.asdict())
```

#### json

```json
{
    "date": datetime.datetime(2023, 9, 14, 21, 57, 47),
    "host": "chess.com",
    "opening": "Sicilian Defense: Closed, Traditional",
    "opening_short": "Sicilian Defense",
    "opponent": {
        "avg_move_time": {"opening": 1.2, "middle_game": 5.1906, "end_game": 3.9467},
        "elo": 1603,
        "evaluation": {
            "opening": {"inaccuracy": 1, "mistake": 1, "blunder": 1},
            "middle_game": {"inaccuracy": 13, "mistake": 13, "blunder": 15},
            "end_game": {"inaccuracy": 6, "mistake": 7, "blunder": 7}
        }
    },
    "phases": {"opening": 4, "middle_game": 64, "end_game": 91},
    "player": {
        "avg_move_time": {"opening": 1.65, "middle_game": 3.4875, "end_game": 3.0109},
        "elo": 1619,
        "evaluation": {
            "opening": {"inaccuracy": 0, "mistake": 0, "blunder": 0},
            "middle_game": {"inaccuracy": 1, "mistake": 1, "blunder": 1},
            "end_game": {"inaccuracy": 1, "mistake": 1, "blunder": 1}
        }
    },
    "player_color": "white",
    "result": ["white", "timeout"],
    "time_class": "blitz",
    "time_control": "180+0",
    "url": "https://www.chess.com/game/live/88467619273",
    "username": "barabasz60"
}
```


## Architecture 

### Game object

| Attribute       | Description                                                                                               |
| --------------- | --------------------------------------------------------------------------------------------------------- |
| `host`          | Server where game was played.                                                                             |
| `url`           | Url to game.                                                                                              |
| `player_color`  | Player color in game.                                                                                     |
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
| `url`           | Url to game.                                                                                              |

### Player object

| Attribute       | Description                                  |
| --------------- | -------------------------------------------- |
| `elo`           | elo of player at the time of game.           |
| `avg_move_time` | list with average move time for each phase.  |
| `evaluation`    | dict with number of mistakes for each phase. |



- example game:



## Example charts (Code can be found in [here](./example.py))
![image](https://github.com/michalskibinski109/chess_insight/assets/77834536/f6bb0e67-6a3b-448a-9cf7-186c434ebd9e)



