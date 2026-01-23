from f_search.ds.priority.i_2_gh.main import PriorityGH, Key
from f_search.ds.priority.i_1_g import PriorityG


class PriorityGHFlags(PriorityGH[Key]):
    """
    ============================================================================
     Priority based on the G-Value, H-Value and Flags of a State.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 key: Key,
                 g: int,
                 h: int,
                 is_cached: bool = False,
                 is_bounded: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        PriorityGH.__init__(self, key=key, g=g, h=h)
        self._is_cached = is_cached
        self._is_bounded = is_bounded

    def key_comparison(self) -> tuple[int, bool, bool, int, Key]:
        """
        ========================================================================
         Return the Key of the State.
        ========================================================================
        """
        return self._g + self._h, not self._is_cached, not self._is_bounded, PriorityG.key_comparison(self)

    def __repr__(self) -> str:
        """
        ========================================================================
         Return the string representation of the PriorityGHFlags.
        ========================================================================
        """
        key = f'key={self._key}'
        g = f'g={self._g}'
        h = f'h={self._h}'
        is_cached = f'is_cached={self._is_cached}'
        is_bounded = f'is_bounded={self._is_bounded}'
        return f'PriorityGHFlags({key}, {g}, {h}, {is_cached}, {is_bounded})'
