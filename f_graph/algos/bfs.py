from f_graph.path_finding.algo import AlgoPath
from f_graph.path_finding.components.problem import Problem
from f_graph.path_finding.components.path import Path
from f_graph.path_finding.components.data import Data
from f_graph.path_finding.components.ops import Ops


class BFS(AlgoPath[Problem, Path, Data, Ops]):

    def __init__(self,
                 problem: Problem,
                 path: Path,
                 data: Data,
                 ops: Ops,
                 name: str = 'BFS') -> None:
        AlgoPath.__init__(self,
                          problem=problem,
                          path=path,
                          data=data,
                          ops=ops,
                          name=name)
