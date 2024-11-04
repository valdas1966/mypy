from f_graph.problems.i_2_one_to_many import ProblemOneToMany
from f_graph.ops.i_0_node_abc import OpsNodeABC, Data, Node
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToMany)


class OpsNodeOneToMany(OpsNodeABC[Problem, Data, Node]):
    pass
