from f_graph.nodes.i_0_base import NodeBase
from f_graph.nodes.mixins.has_cell import HasCell, Cell


class NodeCell(NodeBase, HasCell):

    def __init__(self, cell: Cell = Cell(), name: str = None) -> None:
        NodeBase.__init__(self, name=name)
        HasCell.__init__(self, cell=cell)