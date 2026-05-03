from f_core.counters.main import Counters


class Factory:
    """
    ========================================================================
     Factory for the Counters class.
    ========================================================================
    """

    @staticmethod
    def empty() -> Counters:
        """
        ====================================================================
         Empty Counters (no declared names). Useful for
         testing edge cases of `__repr__` / equality.
        ====================================================================
        """
        return Counters(names=())

    @staticmethod
    def flat() -> Counters:
        """
        ====================================================================
         3-counter flat (un-grouped) Counters.
        ====================================================================
        """
        return Counters(names=('cnt_a', 'cnt_b', 'cnt_c'))

    @staticmethod
    def grouped() -> Counters:
        """
        ====================================================================
         8-counter grouped Counters mirroring the OMSPP
         scaffold: h-calls, phi-calls, frontier ops.
        ====================================================================
        """
        return Counters(names=(
            ('cnt_h_search', 'cnt_h_update'),
            ('cnt_phi_search', 'cnt_phi_update'),
            ('cnt_push', 'cnt_pop',
             'cnt_pop_stale', 'cnt_decrease'),
        ))
