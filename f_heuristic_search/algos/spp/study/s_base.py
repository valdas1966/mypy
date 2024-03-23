from f_heuristic_search.algos.spp.base import SPPAlgoBase
from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete
from f_heuristic_search.graphs.graph import Graph
from f_data_structure.collections.queue_fifo import QueueFIFO


class Algo(SPPAlgoBase):

    def run(self) -> None:
        self._generated.push(self.spp.start)
        self._expanded.add(self.spp.goal)


graph = Graph(rows=5)
start = graph[0][0]
goal = graph[4][4]
spp = SPPConcrete(graph=graph, start=start, goal=goal)
algo = Algo(spp=spp, type_queue=QueueFIFO)
algo.run()
print(algo.generated)
print(algo.expanded)