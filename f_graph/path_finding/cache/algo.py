from f_graph.path_finding.algo import Algo as AlgoPath
from f_graph.path_finding.cache.config import Problem, Path, Ops, Data, Node


class Algo(AlgoPath[Problem, Path, Data, Ops]):

    def __init__(self,
                 problem: Problem,
                 data: Data,
                 ops: Ops,
                 cache: set[Node],
                 name: str = 'Algorithm-Path-Cache'):
        AlgoPath.__init__(self, problem=problem, data=data, ops=ops, name=name)
