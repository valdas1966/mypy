from f_ds.graphs.u_1_grid import UGraphGrid as u_graph, NodeCell


def test_generate():
    graph = u_graph.generate(rows=5, pct_valid=80, type_node=NodeCell)
    assert len(graph) == 25
    assert