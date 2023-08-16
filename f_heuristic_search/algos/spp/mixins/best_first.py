from f_heuristic_search.algos.spp.mixins.sppable import SPPAble
from f_heuristic_search.algos.spp.mixins.open_closed import OpenClosed
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.alias.cell import Cell


class BestFirst(SPPAble, OpenClosed):

    def __init__(self, spp: SPP, to_node: 'NodeClass') -> None:
        SPPAble.__init__(self, spp=spp)
        OpenClosed.__init__(self)
        self._to_node = to_node

    def run(self) -> None:
        self._generate_node(cell=self.spp.start)
        while self.open:
            best = self.open.pop()


    def _generate_node(self,
                       cell: Cell,
                       parent: 'NodeClass' = None) -> 'NodeClass':
        node = self._to_node(cell=cell, parent=parent)
        self.open.heappush(node)

    def _expand_node(self, node: 'NodeClass') -> None:
        for cell in node.neighbors():
            if cell in self.closed:
                continue
            elif cell in self.open:
                if cell.g > node.g + 1:
                    cell.update_parent(node)
            else:
                self._generate_node(cell=cell, parent=node)
