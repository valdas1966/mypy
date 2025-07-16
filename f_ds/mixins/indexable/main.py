from typing import Union, overload
from f_ds.mixins.collectionable import Collectionable, IterableSized, Item
from abc import abstractmethod


class Indexable(Collectionable[Item]):
    """
    ============================================================================
     Mixin-Class for Objects with positional indexing functionality (int/slice).
    ============================================================================
    """

    @abstractmethod
    def to_iterable(self) -> IterableSized[Item]:
        """
        ========================================================================
         Convert the Object's Content into an Iterable of Items.
        ========================================================================
        """
        pass

    def __getitem__(self, index: Union[int, slice]) -> Union[Item, list[Item]]:
        """
        ========================================================================
         Get item(s) by positional index or slice.
        ========================================================================
        """
        li = list(self.to_iterable())
        
        if isinstance(index, int) or isinstance(index, slice):
            return li[index]
        else:
            msg = f"Invalid index type: {type(index)}. Expected int or slice."
            raise TypeError(msg)    
