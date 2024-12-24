from f_graph.path.solution import SolutionPath, Node
from f_graph.path.single.solution import SolutionSingle
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
        self.state = State()

    def update(self, sol_single: SolutionSingle) -> None:
        """
        ========================================================================
         Update SolutionMulti with SolutionSingle.
        ========================================================================
        """
        self.state.update(state=sol_single.state)
        self.elapsed += sol_single.elapsed
        self.set_valid(sol_single.is_found)
