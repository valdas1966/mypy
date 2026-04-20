from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for HBase / CacheEntry test instances.
    ========================================================================
    """

    @staticmethod
    def base() -> HBase[StateBase[str]]:
        """
        ====================================================================
         Plain HBase — exercises the default is_perfect / suffix_next.
         __call__ raises NotImplementedError by design.
        ====================================================================
        """
        return HBase[StateBase[str]]()

    @staticmethod
    def entry_goal() -> CacheEntry[StateBase[str]]:
        """
        ====================================================================
         CacheEntry for a goal node: h_perfect=0, suffix_next=None.
        ====================================================================
        """
        return CacheEntry(h_perfect=0.0, suffix_next=None)

    @staticmethod
    def entry_pre_goal() -> CacheEntry[StateBase[str]]:
        """
        ====================================================================
         CacheEntry one hop before the goal: h_perfect=1,
         suffix_next = StateBase('C').
        ====================================================================
        """
        return CacheEntry(h_perfect=1.0,
                          suffix_next=StateBase[str](key='C'))
