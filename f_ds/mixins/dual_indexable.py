from abc import abstractmethod
from typing import TypeVar, Generic, Hashable, Union, overload, KeysView, ValuesView, ItemsView, Iterator
from f_ds.mixins.collectionable.main import Collectionable, Item


Key = TypeVar('Key', bound=Hashable)


class DualIndexable(Collectionable[Item], Generic[Key]):
    """
    ============================================================================
     Mixin-Class for Objects with both positional and key-based indexing.
    ============================================================================
    """

    @abstractmethod
    def to_key_value_pairs(self) -> Iterator[tuple[Key, Item]]:
        """
        ========================================================================
         Convert the Object's Items into key-value pairs.
        ========================================================================
        """
        pass

    @overload
    def __getitem__(self, index: int) -> Item: ...

    @overload
    def __getitem__(self, index: slice) -> list[Item]: ...

    @overload
    def __getitem__(self, key: Key) -> Item: ...

    def __getitem__(self, index: Union[int, slice, Key]) -> Union[Item, list[Item]]:
        """
        ========================================================================
         Get item(s) by positional index, slice, or key.
        ========================================================================
        """
        if isinstance(index, int):
            items = list(self.to_iterable())
            return items[index]
        elif isinstance(index, slice):
            items = list(self.to_iterable())
            return items[index]
        else:
            # Assume it's a key
            for k, v in self.to_key_value_pairs():
                if k == index:
                    return v
            raise KeyError(index)

    def keys(self) -> KeysView[Key]:
        """
        ========================================================================
         Return a view of the Object's keys.
        ========================================================================
        """
        return KeysView({k: v for k, v in self.to_key_value_pairs()})

    def values(self) -> ValuesView[Item]:
        """
        ========================================================================
         Return a view of the Object's values.
        ========================================================================
        """
        return ValuesView({k: v for k, v in self.to_key_value_pairs()})

    def items(self) -> ItemsView[Key, Item]:
        """
        ========================================================================
         Return a view of the Object's key-value pairs.
        ========================================================================
        """
        return ItemsView({k: v for k, v in self.to_key_value_pairs()})

    def get(self, key: Key, default: Item = None) -> Item:
        """
        ========================================================================
         Get item by key with optional default value.
        ========================================================================
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, item) -> bool:
        """
        ========================================================================
         Return True if the Object contains the received item (key or value).
        ========================================================================
        """
        # First check if it's a key
        for k, _ in self.to_key_value_pairs():
            if k == item:
                return True
        # Then check if it's a value
        for _, v in self.to_key_value_pairs():
            if v == item:
                return True
        return False

    def __iter__(self) -> Iterator[Key]:
        """
        ========================================================================
         Enable iteration over the Object's keys.
        ========================================================================
        """
        for k, _ in self.to_key_value_pairs():
            yield k

    def __reversed__(self):
        """
        ========================================================================
         Enable reversed iteration over the Object's Items.
        ========================================================================
        """
        return reversed(list(self.to_iterable()))

    def to_iterable(self):
        """
        ========================================================================
         Convert the Object's Items into an iterable (implements Collectionable).
        ========================================================================
        """
        return [v for _, v in self.to_key_value_pairs()]