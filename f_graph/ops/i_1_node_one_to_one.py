from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.ops.i_0_node_abc import OpsNodeABC, Data, Node
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToOne)


class OpsNodeOneToOne(OpsNodeABC[Problem, Data, Node]):
    pass
