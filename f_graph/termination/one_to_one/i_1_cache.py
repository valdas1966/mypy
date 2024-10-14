from f_graph.termination.one_to_one.i_0_goal import TerminationGoal, Node


class TerminationCache(TerminationGoal):

    def __init__(self, goal: Node, cache: set[Node]) -> None:
        TerminationGoal.__init__(self, goal=goal)
        self._cache = cache

    def can(self, node: Node) -> bool:
        return TerminationGoal.can(self, node=node) or node in self._cache
