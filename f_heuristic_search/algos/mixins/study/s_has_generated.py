from f_data_structure.collections.i_2_queue_fifo import QueueFIFO
from f_heuristic_search.algos.mixins.has_generated import HasGenerated, NodeBase


class Algo(HasGenerated[NodeBase]):

    def __init__(self):
        HasGenerated.__init__(self, type_queue=QueueFIFO)

    def run(self) -> None:
        a = NodeBase('A')
        b = NodeBase('B')
        self._generated.push(b)
        self._generated.push(a)


algo = Algo()
algo.run()
print(algo.generated)
