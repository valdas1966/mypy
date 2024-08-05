from f_graph.problems.i_2_one_to_one import ProblemOneToOne, NodePath
from f_graph.data.generated_explored import DataGeneratedExplored
from f_graph.path.one_to_one import PathOneToOne
from f_ds.queues.i_1_fifo import QueueFIFO
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class BFS(Generic[Node]):
    """
    ============================================================================
     Breadth-First-Search Algorithm.
    ============================================================================
    """

    def __init__(self, problem: ProblemOneToOne) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._data = DataGeneratedExplored[NodePath](type_queue=QueueFIFO)
        self._path = PathOneToOne[NodePath](goal=problem.goal)
        self._search()

    @property
    def problem(self) -> ProblemOneToOne:
        """
        ========================================================================
         Return the shortest path One-to-One Problem.
        ========================================================================
        """
        return self._problem

    @property
    def data(self) -> DataGeneratedExplored:
        """
        ========================================================================
         Return the Algo's Data (Generated and Explored).
        ========================================================================
        """
        return self._data

    @property
    def path(self) -> PathOneToOne:
        """
        ========================================================================
         Return the Path-Manager of the shortest path problem.
        ========================================================================
        """
        return self._path

    def _search(self) -> None:
        """
        ========================================================================
         Search the shortest path from Start to Goal.
        ========================================================================
        """
        self._generate_node(node=self._problem.start)
        while self._data.generated:
            best = self._data.generated.pop()
            if best == self._problem.goal:
                self._path.set_found()
                break
            self._explore_node(node=best)

    def _explore_node(self, node: Node) -> None:
        """
        ========================================================================
         Explore the Node (generate all node's children).
        ========================================================================
        """
        children = self._problem.graph.neighbors(node)
        for child in children:
            if child in self._data.explored:
                continue
            if child in self._data.generated:
                continue
            self._generate_node(node=child, parent=node)
        self._data.explored.add(node)

    def _generate_node(self,
                       node: Node,
                       parent: Node = None) -> None:
        """
        ========================================================================
         Generate list Node (set parent and add to list list).
        ========================================================================
        """
        node.parent = parent
        self._data.generated.push(node)
