from f_graph.path.solution import SolutionPath, Node
from f_graph.path.one_to_one.solution import SolutionSingle
from f_graph.path.multi.state import StateMulti as State


class SolutionMulti(SolutionPath[State]):
    """
    ============================================================================
     Solution for Path-Problems with Multiple-Goals.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionPath.__init__(self)
        self._state = State()
        self._paths: dict[Node, list[Node]] = dict()

    @property
    def paths(self) -> dict[Node, list[Node]]:
        """
        ========================================================================
         Return Optimal-Paths from Start to Goals.
        ========================================================================
        """
        return self._paths

    def update(self,
               goal: Node,
               sol_single: SolutionSingle,
               is_shared: bool) -> None:
        """
        ========================================================================
         Update SolutionMulti with SolutionSingle.
        ========================================================================
        """
        if not is_shared:
            self._state.update(state=sol_single.state)
        self._elapsed += sol_single.elapsed
        self._paths[goal] = sol_single.path
        self.set_valid() if sol_single else self.set_invalid()
