from typing import Type, Any, Sequence
from enum import Enum
from types import DynamicClassAttribute


class Shared:

    def __init__(self, keys_shared: set[str]) -> None:
        self._keys_shared = set(keys_shared)
        self._enum_keys = Shared.create_enum(name='Keys',
                                             keys=self._keys_shared)
        self._shared = {key: None for key in self._enum_keys}

    @staticmethod
    def create_enum(name: str, keys: set[str]) -> Type[Enum]:
        return Enum(name, {key: key for key in keys})
