from abc import abstractmethod
from typing import (TypeVar, Generic, Hashable, Iterator,
                    KeysView, ValuesView, ItemsView)
from f_ds.mixins.collectionable.main import Collectionable, Item


Key = TypeVar('Key', bound=Hashable)


class IndexableKey(Collectionable[Item], Generic[Key]):
    """
    ============================================================================
     Mixin-Class for Objects with key-based indexing functionality (str/hashable).
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

    def __getitem__(self, key: Key) -> Item:
        """
        ========================================================================
         Get item by key.
        ========================================================================
        """
        for k, v in self.to_key_value_pairs():
            if k == key:
                return v
        raise KeyError(key)

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

    def __contains__(self, key: Key) -> bool:
        """
        ========================================================================
         Return True if the Object contains the received key.
        ========================================================================
        """
        for k, _ in self.to_key_value_pairs():
            if k == key:
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

    def to_iterable(self):
        """
        ========================================================================
         Convert the Object's Items into an iterable (implements Collectionable).
        ========================================================================
        """
        return [v for _, v in self.to_key_value_pairs()]