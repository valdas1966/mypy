from f_graph.path.algos.one_to_many.generators.g_state import GenStateOneToMany
from f_graph.path.algos.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.generators.g_heuristic import GenHeuristic


def test_update() -> None:
    """
    ========================================================================
     Test that update() correctly updates heuristic of generated nodes.
    ========================================================================
    """
    state = GenStateOneToMany.gen_empty()
    problem = GenProblemOneToOne.gen_3x3()
    start = problem.start
    start.h = 0
    state.generated.push(item=start)
    heuristic = GenHeuristic.gen_manhattan(graph=problem.graph,
                                           goal=problem.goal)
    state.update(heuristic)
    assert start.h == heuristic(node=start)
