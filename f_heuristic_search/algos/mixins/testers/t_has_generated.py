from f_heuristic_search.algos.mixins.has_generated import HasGenerated, NodeBase
from f_data_structure.collections.queue_fifo import QueueFIFO


def test_has_generated():
    a = NodeBase('A')
    b = NodeBase('B')
    algo = HasGenerated(type_queue=QueueFIFO)
    algo._generated.push(b)
    algo._generated.push(a)
    assert algo.generated == [b, a]
