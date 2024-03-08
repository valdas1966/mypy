from f_heuristic_search.domain.grid.graph import Graph
from f_heuristic_search.domain.grid.node import Node
from f_heuristic_search.problem_types.spp import SPP
from collections import namedtuple
from f_utils import u_pickle


def generate_graphs(cnt: int,
                    rows: int,
                    pcts: list[int]) -> list[Graph]:
    res = list()
    for pct_non_valid in pcts:
        res.extend(Graph.generate_many(cnt=cnt,
                                       rows=rows,
                                       pct_non_valid=pct_non_valid,
                                       type_node=Node))
    return res


pcts = list(range(10, 51, 10))
graphs = generate_graphs(cnt=10, rows=10, pcts=pcts)
pickle_graphs = 'd:\\temp\\kg\\exp\\graphs_gen_10_x_10.pickle'
u_pickle.dump(obj=graphs, path=pickle_graphs)
