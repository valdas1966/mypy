from f_hs.algo.i_1_mospp.i_1_astar_inc.main import AStarIncMOSPP
from f_hs.problem.i_0_base._factory import _ProblemGraph
from f_hs.problem.i_1_grid import ProblemGrid


class Factory:
    """
    ============================================================================
     Factory for AStarIncMOSPP test instances.
    ============================================================================
    """

    @staticmethod
    def canonical(**kwargs) -> AStarIncMOSPP:
        """
        ========================================================================
         AStarIncMOSPP on the canonical incremental-MOSPP
         fixture `grid_6x6_zigzag_mospp` (starts (0,0) / (2,3)
         / (0,3); goal (5,0); per-start costs 15 / 10 / 12;
         Manhattan h to the fixed goal). Extra kwargs override
         the algorithm config (e.g. `carry_cache=False`,
         `rule_bpmx='CASCADE'`).
        ========================================================================
        """
        p = ProblemGrid.Factory.grid_6x6_zigzag_mospp()
        return AStarIncMOSPP(
            problem=p,
            h=lambda s, g: float(s.key.distance(g.key)),
            **kwargs,
        )

    @staticmethod
    def graph_abc_two_starts() -> AStarIncMOSPP:
        """
        ========================================================================
         A -> B -> C with starts [A, B], goal C. Two sequential
         sub-searches: from A (cost 2), from B (cost 1). After
         sub-search 1 the on-path cache covers {A, B, C}, so
         sub-search 2 from B is a cache-hit-at-init.
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='C',
        )
        p._starts = [p._states['A'], p._states['B']]
        p._goals = [p._states['C']]
        pos = {'A': 0, 'B': 1, 'C': 2}
        return AStarIncMOSPP(
            problem=p,
            h=lambda s, g: abs(pos[s.key] - pos[g.key]),
            order_starts='near',
        )

    @staticmethod
    def graph_abc_repeated_start() -> AStarIncMOSPP:
        """
        ========================================================================
         A -> B -> C with starts [A, A], goal B. Sub-search 1
         expands and finalizes A (cost 1); sub-search 2 hits
         the `already_reached` fast-path (duplicate start).
        ========================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='B',
        )
        p._starts = [p._states['A'], p._states['A']]
        p._goals = [p._states['B']]
        pos = {'A': 0, 'B': 1, 'C': 2}
        return AStarIncMOSPP(
            problem=p,
            h=lambda s, g: abs(pos[s.key] - pos[g.key]),
            order_starts='near',
        )
