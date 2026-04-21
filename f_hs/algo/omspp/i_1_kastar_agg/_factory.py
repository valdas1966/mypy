from f_hs.algo.omspp.i_1_kastar_agg.main import KAStarAgg
from f_hs.problem.i_0_base._factory import _ProblemGraph


def _pos_h(pos: dict[str, int]):
    return lambda s, g: abs(pos[s.key] - pos[g.key])


class Factory:
    """
    ========================================================================
     Factory for KAStarAgg test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc_two_goals_min() -> KAStarAgg:
        """
        ====================================================================
         kA*_agg on A -> B -> C with goals [B, C] and Φ=MIN.
         Lazy + aggregate storage (defaults).
        ====================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B'], 'B': ['C'], 'C': []},
            start='A', goal='B',
        )
        p._goals = [p._states['B'], p._states['C']]
        return KAStarAgg(
            problem=p,
            h=_pos_h({'A': 0, 'B': 1, 'C': 2}),
            agg='MIN',
        )

    @staticmethod
    def diamond_two_goals_max() -> KAStarAgg:
        """
        ====================================================================
         Diamond A -> {B, C} -> D with goals [B, D] and Φ=MAX.
         Eager + vector storage — exercises both feature axes.
        ====================================================================
        """
        p = _ProblemGraph(
            adj={'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []},
            start='A', goal='B',
        )
        p._goals = [p._states['B'], p._states['D']]
        return KAStarAgg(
            problem=p,
            h=_pos_h({'A': 0, 'B': 1, 'C': 1, 'D': 2}),
            agg='MAX',
            is_lazy=False,
            store_vector=True,
        )
