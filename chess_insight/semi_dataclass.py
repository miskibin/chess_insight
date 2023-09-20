from __future__ import annotations
from abc import ABC
from enum import Enum
from rich.console import Console
from rich.markdown import Markdown
from typing import get_type_hints
from collections.abc import MutableMapping
from easy_logs import get_logger

logger = get_logger()


class SemiDataclass(ABC):
    _ROUND_TO = 4

    def print_md(self) -> None:
        """
        Prints markdown documentation of class.
        """

        console = Console()
        md = Markdown(self.markdown_docs())
        console.print(md)

    def markdown_docs(self) -> str:
        docs_content = "## " + self.__class__.__name__ + "\n\n"
        table_data = []
        for name, value in vars(self.__class__).items():
            if not name.startswith("_"):  # Exclude special attributes
                docstring = (
                    getattr(value, "__doc__", "NO DOCSTRING").strip().replace("\n", " ")
                )
                value = getattr(self, name)
                table_data.append([name, docstring, value])

        annotated_hints = get_type_hints(self.__class__, include_extras=True)
        for name, hint in annotated_hints.items():
            docstring = hint.__metadata__[0]
            value = getattr(self, name)
            table_data.append([name, docstring, value])

        docs_content += "| Attribute | Description  |\n"
        docs_content += "| --- | --- | \n"
        for row in table_data:
            docs_content += f"| `{row[0]}` | {row[1]}  |\n"

        return docs_content

    def _convert_enum_values(self, obj):
        if isinstance(obj, SemiDataclass):
            return obj.asdict()
        if isinstance(obj, Enum):
            return obj.name.lower()
        if isinstance(obj, float):
            return round(obj, self._ROUND_TO)
        elif isinstance(obj, dict):
            return {
                self._convert_enum_values(k): self._convert_enum_values(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list) or isinstance(obj, tuple):
            return [self._convert_enum_values(item) for item in obj]
        else:
            return obj

    def _flatten_dict(cls, dictionary: dict, parent_key="", separator="_"):
        items = []
        for key, value in dictionary.items():
            new_key = parent_key + separator + key if parent_key else key
            if isinstance(value, MutableMapping):
                items.extend(
                    cls._flatten_dict(value, new_key, separator=separator).items()
                )
            else:
                items.append((new_key, value))
        return dict(items)

    def flatten(self) -> dict:
        dict_data = self.asdict()
        return self._flatten_dict(dict_data)

    def asdict(self) -> dict:
        """
        Returns class represented as dict. Changes enum classes to its values.
        """
        game_dict = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if not attr_name.startswith("_") and not callable(attr):
                # Convert Enum members to their values
                attr = self._convert_enum_values(attr)
                game_dict[attr_name] = attr
        return game_dict
