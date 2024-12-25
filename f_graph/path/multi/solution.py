from f_graph.path.single.solution import SolutionSingle, Node
from f_ds.mixins.collectionable import Collectionable
from f_core.mixins.validatable import Validatable


class SolutionMulti(Collectionable):

    def __init__(self, solutions: dict[Node, SolutionSingle]) -> None:
        Validatable.__init__(self, is_valid=all(solutions))
        self._solutions = solutions

    @property
    def elapsed(self) -> int:
        return sum(solution.elapsed for solution in self._solutions)

    @property
    def generated(self) -> int:
        return sum(len(solution.state.generated) for solution
                   in self._solutions)

    @property
    def explored(self) -> int:
        return sum(len(solution.state.explored) for solution in self._solutions)

    def to_iterable(self) -> tuple[Node, SolutionSingle]:
        return self._solutions.items()

    def __getitem__(self, item: Node) -> SolutionSingle:
        return self._solutions[item]

