from f_graph.path.generators.g_graph import GenGraphPath


def test_children() -> None:
    graph = GenGraphPath.gen_3x3()
    graph[0, 1].parent = graph[0, 0]
    children = graph.children(node=graph[0, 1])
    assert len(children) == 2
    assert children[0] == graph[0, 2]
    assert children[1] == graph[1, 1]
