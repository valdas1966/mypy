from f_hs.algo.i_0_oospp.i_2_astar_bpmx.main import AStarBPMX
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


class Factory:
    """
    ============================================================================
     Factory for AStarBPMX test instances.

     The grid_4x4 builder is parametric over `(rule_bpmx,
     depth_bpmx)`. Defaults (`rule_bpmx=None`) reproduce the
     off-mode (≡ plain AStar).
    ============================================================================
    """

    @staticmethod
    def grid_4x4(rule_bpmx: str | None = None,
                 depth_bpmx: int | None = 1) -> AStarBPMX:
        """
        ========================================================================
         AStarBPMX on the canonical 4x4 obstacle grid with
         Manhattan h. Defaults (rule_bpmx=None) reproduce
         off-mode (behaviourally identical to plain AStar).
         See AStarBPMX / BPMXMixin docstrings for the
         (rule_bpmx, depth_bpmx) semantics.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
        )

    @staticmethod
    def graph_diamond_inconsistent_cascade() -> AStarBPMX:
        """
        ========================================================================
         Diamond graph with an artificially inconsistent heuristic
         (B has h=4, others h=0) + CASCADE (full reach) so BPMX
         has something to lift. Useful for verifying lift events
         fire.
        ========================================================================
        """
        h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
        return AStarBPMX(
            problem=ProblemSPP.Factory.graph_diamond(),
            h=lambda s: h_inc.get(s.key, 0.0),
            rule_bpmx='CASCADE',
            depth_bpmx=None,
            is_recording=True,
        )
