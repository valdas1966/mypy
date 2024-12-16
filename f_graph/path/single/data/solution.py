from f_graph.path.data.solution import SolutionPath, NodePath, dataclass
from f_graph.path.single.components.state import State
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


@dataclass(frozen=True)
class SolutionSingle(Generic[Node], SolutionPath):
    """
    ============================================================================
     Solution of Path-Algorithm with Single-Goal.
    ============================================================================
    """
    path: list[Node]

    def __init__(self,
                 state: State,
                 cache: dict[Node, Node],
                 elapsed: int,
                 is_path_found: bool):
        path: list[Node] = list()

        if is_path_found:
            path_from_best: list[Node] = list()
            if state.best in cache:
                path_from_best = cache[state.best].path_from_start()
                path_from_best = list(reversed(path_from_best[:-1]))
            path = state.best.path_from_start() + path_from_best

        # Set values directly using `object.__setattr__()` since `frozen=True`
        object.__setattr__(self, 'path', path)
        object.__setattr__(self, 'nodes_generated', len(state.generated))
        object.__setattr__(self, 'nodes_explored', len(state.explored))
        object.__setattr__(self, 'elapsed', elapsed)
