from f_graph.graphs.u_1_grid import UGraphGrid as u_graph, NodeCell


def test_generate():
    graph = u_graph.generate(rows=5, pct_valid=80, type_node=NodeCell)
    assert len(graph) == 20
    assert type(graph[0, 0]) == NodeCell


def test_generate_multiple():
    graphs = u_graph.generate_multiple(n=10, rows=5)
    assert len(graphs) == 10
