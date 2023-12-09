import pandas as pd
import os
from unittest.mock import patch, MagicMock
from chess_insight import export_games_to_csv


class TestExportGamesToCSV:
    @patch("chess_insight.pd.DataFrame")
    def test_FR5_export_games_to_csv(self, mock_df):
        mock_to_csv = MagicMock()
        mock_df.return_value.to_csv = mock_to_csv
        games = [MagicMock(), MagicMock()]
        games[0].flatten.return_value = {
            "game1_key1": "game1_value1",
            "game1_key2": "game1_value2",
        }
        games[1].flatten.return_value = {
            "game2_key1": "game2_value1",
            "game2_key2": "game2_value2",
        }
        file_name = "test_games.csv"

        result = export_games_to_csv(games, file_name)

        mock_df.assert_called_once_with(
            [
                {"game1_key1": "game1_value1", "game1_key2": "game1_value2"},
                {"game2_key1": "game2_value1", "game2_key2": "game2_value2"},
            ]
        )
        mock_to_csv.assert_called_once_with(file_name, index=False)

        if os.path.exists(file_name):
            os.remove(file_name)  # cleanup
