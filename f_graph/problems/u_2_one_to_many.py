from f_ds.grids.grid import Grid
from f_graph.graphs.i_1_grid import GraphGrid, NodePathCell
from f_graph.problems.i_2_one_to_many import ProblemOneToMany
from typing import Type


class UProblemOneToMany:

    @staticmethod
    def gen_3x3(type_node: Type[NodePathCell] = NodePathCell) -> ProblemOneToMany:
        grid = Grid(3)
        graph = GraphGrid(grid=grid, type_node=type_node)
        start = graph[0, 0]
        goals = {graph[0, 2], graph[2, 0]}
        return ProblemOneToMany(graph, start, goals)

