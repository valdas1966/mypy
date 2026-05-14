from f_hs.algo.i_0_oospp.i_3_astar_bpmx.main import AStarBPMX
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for AStarBPMX test instances. Exercises the
     dict-based kwargs API (cache / goal / bounds) plus the
     BPMX kwargs (rule_bpmx / depth_bpmx) directly. Defaults
     reproduce off-mode (rule_bpmx=None) so factories that
     accept BPMX parameters can also be used as plain
     AStarLookup-equivalent instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc_cached_at_b(rule_bpmx: str | None = None,
                              depth_bpmx: int | None = 1,
                              is_recording: bool = False
                              ) -> AStarBPMX:
        """
        ====================================================================
         HCached covering only {B, C} on graph A → B → C.
         Pop(A) not cached → expand → push(B). Pop(B) triggers
         _early_exit. Cost 2.

         Parametric over BPMX kwargs — defaults reproduce
         off-mode (behaviourally identical to a plain
         AStarLookup with the same cache). Active mechanisms
         (e.g. `rule_bpmx='CASCADE', depth_bpmx=1,
         is_recording=True`) exercise the combined cache +
         BPMX path.
        ====================================================================
        """
        b = StateBase[str](key='B')
        c = StateBase[str](key='C')
        cache = {
            b: CacheEntry(h_perfect=1, suffix_next=c),
            c: CacheEntry(h_perfect=0, suffix_next=None),
        }
        h_map = {'A': 2}
        return AStarBPMX(
            problem=ProblemSPP.Factory.graph_abc(),
            h=lambda s: h_map.get(s.key, 0),
            cache=cache,
            goal=c,
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
            is_recording=is_recording,
        )

    @staticmethod
    def grid_4x4(rule_bpmx: str | None = None,
                 depth_bpmx: int | None = 1) -> AStarBPMX:
        """
        ====================================================================
         AStarBPMX on the canonical 4x4 obstacle grid with
         Manhattan h. Defaults (rule_bpmx=None) reproduce
         off-mode (behaviourally identical to plain
         AStarLookup). See AStarBPMX / BPMXMixin docstrings for
         the (rule_bpmx, depth_bpmx) semantics.
        ====================================================================
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
        ====================================================================
         Diamond graph with an artificially inconsistent heuristic
         (B has h=4, others h=0) + CASCADE (full reach) so BPMX
         has something to lift. Useful for verifying lift events
         fire.
        ====================================================================
        """
        h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
        return AStarBPMX(
            problem=ProblemSPP.Factory.graph_diamond(),
            h=lambda s: h_inc.get(s.key, 0.0),
            rule_bpmx='CASCADE',
            depth_bpmx=None,
            is_recording=True,
        )

    @staticmethod
    def grid_4x4_beacon(rule_bpmx: str | None = None,
                        depth_bpmx: int | None = 1,
                        is_recording: bool = False
                        ) -> AStarBPMX:
        """
        ====================================================================
         4x4 obstacle grid with a cached "beacon" at (0,1) holding
         its perfect heuristic value h*=6 (vs Manhattan=2; gap=4).
         The beacon is a successor of start, so BPMX from the
         start's expansion has immediate access to a high-h cell
         that lifts its neighbors and (under Rule 3 / CASCADE)
         lifts the start itself.

         Parametric over BPMX kwargs --- defaults reproduce
         off-mode (counters identical to plain AStarLookup with
         the same cache). Optimal cost is 7.

         Probed counter signature (cost=7, push=13, pop=8,
         expand=7, generated=13 across ALL valid (rule, depth)):
           rule_bpmx | depth | att | suc | depth_max
           ----------+-------+-----+-----+----------
           None      |   1   |  0  |  0  |     0
           '1'       |   1   |  7  |  0  |     0
           '1'       |  2..N |  7  |  2  |     2
           '2'       |   1   |  7  |  2  |     0
           '3'       |  1..N |  7  |  2  |     0
           CASCADE   |   1   |  7  |  2  |     0
           CASCADE   |  2..N |  7  |  2  |     2
        ====================================================================
        """
        from collections import deque
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        # Locate the beacon state (0, 1) by BFS from start.
        seen = {problem.start}
        q = deque([problem.start])
        beacon = None
        while q:
            s = q.popleft()
            if s.rc == (0, 1):
                beacon = s
                break
            for succ in problem.successors(s):
                if succ not in seen:
                    seen.add(succ)
                    q.append(succ)
        cache = {beacon: CacheEntry(h_perfect=6, suffix_next=None)}
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            cache=cache,
            goal=goal,
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
            is_recording=is_recording,
        )

    @staticmethod
    def grid_6x6_zigzag_beacon(rule_bpmx: str | None = None,
                               depth_bpmx: int | None = 1,
                               is_recording: bool = False
                               ) -> AStarBPMX:
        """
        ====================================================================
         6x6 zigzag grid (snake-detour) with a cached "beacon" at
         (1,0) holding its perfect heuristic h*=14 (vs Manhattan=4;
         gap=10). The grid forces a long detour from start (0,0)
         to goal (5,0); the beacon sits one step south of start
         on the optimal path. Many cells in the upper region have
         h* - Manhattan > 0, so BPMX has multi-cell, multi-depth
         lift opportunities.

         Grid layout (1 = valid, 0 = invalid):

               col:  0  1  2  3  4  5
             row 0:  1  1  1  1  1  1     <- start (0,0)
             row 1:  1  0  0  0  0  1     <- beacon (1,0); upper wall
             row 2:  1  1  1  1  1  1
             row 3:  0  0  0  0  0  1     <- lower wall
             row 4:  1  1  1  1  1  1
             row 5:  1  1  1  1  1  1     <- goal (5,0)

         Optimal path (cost 15):
           (0,0) -> (1,0) -> (2,0) -> (2,1) -> ... -> (2,5)
                 -> (3,5) -> (4,5) -> (4,4) -> ... -> (4,0)
                 -> (5,0)

         Used by depth-axis tests where the depth_bpmx parameter
         must visibly differentiate counter signatures (the 4x4
         grid is too shallow for that --- on 4x4 Rule 3 saturates
         at depth=1).

         Probed counter signature (cost=15 always):
           rule_bpmx | depth | att | suc | depth_max | exp | push
           ----------+-------+-----+-----+-----------+-----+-----
           None      |   1   |  0  |  0  |     0     | 20  |  27
           '1'       |   1   | 20  |  0  |     0     | 20  |  27
           '1'       |   2   | 19  |  1  |     2     | 19  |  27
           '1'       |   3   | 18  |  2  |     3     | 18  |  26
           '1'       |  None | 15  |  5  |     6     | 15  |  23
           '2'       |   1   | 20  |  6  |     0     | 20  |  27
           '3'       |   1   | 20  |  5  |     0     | 20  |  27
           '3'       |   2   | 19  |  6  |     1     | 19  |  27
           '3'       |   3   | 18  |  7  |     2     | 18  |  26
           '3'       |  None | 15  |  9  |     5     | 15  |  23
           CASCADE   |   1   | 20  |  6  |     1     | 20  |  27
           CASCADE   |   2   | 18  |  9  |     2     | 18  |  26
           CASCADE   |   3   | 16  |  9  |     3     | 16  |  24
           CASCADE   |  None | 15  |  9  |     6     | 15  |  23
        ====================================================================
        """
        from collections import deque
        problem = ProblemGrid.Factory.grid_6x6_zigzag()
        goal = problem.goal
        seen = {problem.start}
        q = deque([problem.start])
        beacon = None
        while q:
            s = q.popleft()
            if s.rc == (1, 0):
                beacon = s
                break
            for succ in problem.successors(s):
                if succ not in seen:
                    seen.add(succ)
                    q.append(succ)
        cache = {beacon: CacheEntry(h_perfect=14, suffix_next=None)}
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            cache=cache,
            goal=goal,
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
            is_recording=is_recording,
        )

    @staticmethod
    def grid_4x4_cached_suffix_cascade_d1() -> AStarBPMX:
        """
        ====================================================================
         4x4 obstacle grid with a small cached suffix near the
         goal + CASCADE depth=1. Exercises (a) cache-hit early
         term when a cached state is popped, (b) cascade
         skipping cached descendants from lift mutation.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        cache = {goal: CacheEntry(h_perfect=0, suffix_next=None)}
        return AStarBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            cache=cache,
            goal=goal,
            rule_bpmx='CASCADE',
            depth_bpmx=1,
        )
