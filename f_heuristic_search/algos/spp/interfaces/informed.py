from f_heuristic_search.algos.spp.interfaces.sppable import SPPAble
from f_heuristic_search.problem_types.spp import SPP
from f_data_structure.cell import Cell


class Informed(SPPAble):

    def __init__(self, spp: SPP, to_node: 'NodeClass') -> None:
        super().__init__(spp=spp)
        self._to_node = to_node

    def search(self) -> None:
        self._generate_node(cell=self.start)
        while self.open:
            best = self.open.heappop()

    def _generate_node(self,
                       cell: Cell,
                       parent: 'NodeClass' = None) -> 'NodeClass':
        node = self._to_node(cell=cell, parent=parent)
        self.open.heappush(node)

    def _expand_node(self, node: 'NodeClass') -> None:
        for cell in node.neighbors():
            if cell in self.closed:
                continue
            if cell in self.open:
                if cell.g > node.g + 1:
                    cell.update_parent(node)
            self._generate_node(cell=cell, parent=node)
