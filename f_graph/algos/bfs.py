from f_graph.path.single.algo import AlgoPath
from f_graph.path.single.components.problem import Problem
from f_graph.path.single.components.solution import Path
from f_graph.path.single.components.state import State
from f_graph.path.single.components.ops import Ops


class BFS(AlgoPath[Problem, Path, State, Ops]):

    def __init__(self,
                 problem: Problem,
                 path: Path,
                 data: State,
                 ops: Ops,
                 name: str = 'BFS') -> None:
        AlgoPath.__init__(self,
                          problem=problem,
                          path=path,
                          data=data,
                          ops=ops,
                          name=name)
