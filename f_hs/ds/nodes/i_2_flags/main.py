from f_hs.ds.nodes.i_1_cost import NodeCost
from typing import Generic, TypeVar, Self

Key = TypeVar('Key')


class NodeFlags(Generic[Key], NodeCost[Key]):
    
    # Factory
    Factory: type = None
    
    def __init__(self,
                 key: Key,
                 h: int = None,
                 name: str = 'NodeFlags',
                 parent: Self = None) -> None:
        """
        ========================================================================
        
        ========================================================================
        """
        NodeCost.__init__(self, key=key, h=h, name=name, parent=parent)
        self._is_cached: bool = False
        self._is_bounded: bool = False
        
    @property
    def is_cached(self) -> bool:
        """
        ========================================================================
         Get the is_cached flag.
        ========================================================================
        """
        return self._is_cached
    
    @is_cached.setter
    def is_cached(self, value: bool) -> None:
        """
        ========================================================================
         Set the is_cached flag.
        ========================================================================
        """
        self._is_cached = value
        
    @property
    def is_bounded(self) -> bool:
        """
        ========================================================================
         Get the is_bounded flag.
        ========================================================================
        """
        return self._is_bounded
    
    @is_bounded.setter
    def is_bounded(self, value: bool) -> None:
        """
        ========================================================================
         Set the is_bounded flag.
        ========================================================================
        """
        self._is_bounded = value

    def key_comparison(self) -> tuple[int, int, int, int, Key]:
        """
        ========================================================================
         Compare the node with another node.
        ========================================================================
        """
        return (self.f(),
                int(not self.is_cached),
                int(not self.is_bounded),
                self.h,
                self.key)

    def print_details(self) -> None:
        """
        ========================================================================
         Print the details of the node.
        ========================================================================
        """
        key = f'key={self.key}'
        g = f'g={self.g}'
        h = f'h={self.h}'
        f = f'f={self.f()}'
        is_cached = f'is_cached={self.is_cached}'
        is_bounded = f'is_bounded={self.is_bounded}'
        print(f'{key}, {g}, {h}, {f}, {is_cached}, {is_bounded}')
