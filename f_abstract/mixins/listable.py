from collections.abc import Collection
from f_abstract.mixins.sizable import Sizable
from typing import TypeVar, Generic, Iterator
from abc import abstractmethod

Item = TypeVar('Item')


class Listable(Generic[Item], Collection, Sizable):

    @abstractmethod
    def to_list(self) -> list[Item]:
        pass

    def __len__(self) -> int:
        return len(self.to_list())

    def __contains__(self, item: Item) -> bool:
        return item in self.to_list()

    def __iter__(self) -> Iterator[Item]:
        return iter(self.to_list())