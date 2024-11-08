from typing import Generic, TypeVar

Data = TypeVar('Data')


class HasData(Generic[Data]):

    def __init__(self, data: Data) -> None:
        self._data = data

    @property
    def data(self) -> Data:
        return self._data
