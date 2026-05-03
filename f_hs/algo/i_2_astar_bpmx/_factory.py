from f_hs.algo.i_2_astar_bpmx.main import AStarBPMX
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


class Factory:
    """
    ============================================================================
     Factory for AStarBPMX test instances.

     Each method returns an `AStarBPMX` configured with a
     specific (rule_pathmax, depth_bpmx) profile on a known
     problem. Profiles span the four ablation corners
     (off / pathmax-only / BPMX-only / both) plus a few
     mixed configurations.
    ============================================================================
    """

    # ──────────────────────────────────────────────────
    #  Off (baseline, behaves like plain AStar)
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4_off() -> AStarBPMX:
        """
        ========================================================================
         AStarBPMX on 4x4 obstacle grid, both mechanisms off.
         Behaviourally identical to plain AStar.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=None,
            depth_bpmx=0,
        )

    # ──────────────────────────────────────────────────
    #  Isolated pathmax rules (depth 1 only)
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4_rule1() -> AStarBPMX:
        """
        ========================================================================
         AStarBPMX with Felner Rule 1 (parent -> child) only.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=1,
            depth_bpmx=0,
        )

    @staticmethod
    def grid_4x4_rule2() -> AStarBPMX:
        """
        ========================================================================
         AStarBPMX with Felner Rule 2 (children -> parent via min) only.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=2,
            depth_bpmx=0,
        )

    @staticmethod
    def grid_4x4_rule3() -> AStarBPMX:
        """
        ========================================================================
         AStarBPMX with Felner Rule 3 (single child -> parent reverse) only.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=3,
            depth_bpmx=0,
        )

    # ──────────────────────────────────────────────────
    #  BPMX(d) cascade
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4_bpmx_d1() -> AStarBPMX:
        """
        ========================================================================
         AStarBPMX with BPMX(1): cascade only at the immediate
         parent-children level.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=None,
            depth_bpmx=1,
        )

    @staticmethod
    def grid_4x4_bpmx_d2() -> AStarBPMX:
        """
        ========================================================================
         AStarBPMX with BPMX(2): cascade through 2 levels.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=None,
            depth_bpmx=2,
        )

    @staticmethod
    def grid_4x4_bpmx_full() -> AStarBPMX:
        """
        ========================================================================
         AStarBPMX with BPMX(infinity): cascade through the full
         reachable subtree, visited-set bounded.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=None,
            depth_bpmx=None,
        )

    # ──────────────────────────────────────────────────
    #  Combined (pathmax + BPMX)
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4_rule3_bpmx_d1() -> AStarBPMX:
        """
        ========================================================================
         Rule 3 isolated AND BPMX(1) -- both fire; redundant but
         correct. Useful for probing the redundancy claim.
        ========================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=3,
            depth_bpmx=1,
        )

    # ──────────────────────────────────────────────────
    #  Inconsistent-heuristic toy graph
    # ──────────────────────────────────────────────────

    @staticmethod
    def graph_diamond_inconsistent_bpmx_full() -> AStarBPMX:
        """
        ========================================================================
         Diamond graph with an artificially inconsistent heuristic
         (B has h=4, others h=0) so BPMX has something to lift.
         Useful for verifying lift events fire.
        ========================================================================
        """
        h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
        return AStarBPMX(
            problem=ProblemSPP.Factory.graph_diamond(),
            h=lambda s: h_inc.get(s.key, 0.0),
            rule_pathmax=None,
            depth_bpmx=None,
            is_recording=True,
        )
