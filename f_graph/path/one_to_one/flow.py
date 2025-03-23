from f_graph.path.one_to_one.ops import OpsOneToOne
from f_graph.path.one_to_one.state import StateOneToOne
from f_graph.path.one_to_one.problem import ProblemOneToOne


class FlowOneToOne:
    """
    ============================================================================
     Flow for One-to-One Path-Finding Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOneToOne,
                 state: StateOneToOne,
                 ops: OpsOneToOne) -> None:
        """
        ========================================================================
         Initialize the Flow.
        ========================================================================
        """
        self._problem = problem
        self._state = state
        self._ops = ops
    
    def generate_start(self) -> None:
        """
        ========================================================================
         Generate the Start-Node.
        ========================================================================
        """
        self._ops.generate_node(node=self._problem.start)

    def should_continue(self) -> bool:
        """
        ========================================================================
         Return True if there are generated and not explored nodes.
        ========================================================================
        """
        return bool(self._state.generated)

    def select_best(self) -> None:
        """
        ========================================================================
         Select the best node to be the best generated node
        ========================================================================
        """
        # print('Select Best')
        # for node in sorted(self._state.generated):
        #     node.print_details()
        nodes = list(sorted(self._state.generated))
        node_first = nodes[0]
        if node_first.cell.to_tuple() == (4, 4):
            if self._problem.start.cell.to_tuple() == (1, 5):
                from f_utils import u_pickle
                u_pickle.dump(obj=self._state.generated, path='g:\\temp\\generated.pkl')
                exit(1)
        self._state.best = self._state.generated.pop()
        #self._state.generated.push(self._state.best)
        #self._state.best = self._state.generated.pop()
        #self._state.generated.push(self._state.best)
        #self._state.best = self._state.generated.pop()

    def is_path_found(self) -> bool:
        """
        ========================================================================
         Return True if the best node is the goal or is cached.
        ========================================================================
        """
        if self._state.best == self._problem.goal:
            return True
        if self._state.best.is_cached:
            return True
        return False
    
    def explore_best(self) -> None:
        """
        ========================================================================
         Explore the best node.
        ========================================================================
        """
        self._ops.explore_node(node=self._state.best)
