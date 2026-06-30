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

    # ──────────────────────────────────────────────────
    #  Toy fixtures for the `absorb` study / tests
    # ──────────────────────────────────────────────────

    @staticmethod
    def frontier_priority() -> Counters:
        """
        ====================================================================
         Toy priority-frontier tally: tracks the decrease op.
        ====================================================================
        """
        return Counters(names=(
            'cnt_push', 'cnt_pop', 'cnt_decrease'))

    @staticmethod
    def frontier_fifo() -> Counters:
        """
        ====================================================================
         Toy FIFO-frontier tally: no decrease op. Mirroring it
         into an algo scaffold is the case `absorb` synthesizes
         a structural `cnt_decrease = 0` for.
        ====================================================================
        """
        return Counters(names=('cnt_push', 'cnt_pop'))

    @staticmethod
    def algo() -> Counters:
        """
        ====================================================================
         Toy algorithm scaffold: a heap-op group an algorithm
         mirrors from its frontier (via `absorb`), plus a
         search-semantic group it owns itself.
        ====================================================================
        """
        return Counters(names=(
            ('cnt_push', 'cnt_pop', 'cnt_decrease'),
            ('cnt_expanded', 'cnt_generated'),
        ))
