from f_graph.old_path.generators.g_graph import GenGraphPath


def test_children() -> None:
    """
    ============================================================================
     Test the children method.
    ============================================================================
    """
    graph = GenGraphPath.gen_3x3()
    graph[0, 1].parent = graph[0, 0]
    children = graph.children(node=graph[0, 1])
    assert len(children) == 2
    assert children[0] == graph[0, 2]
    assert children[1] == graph[1, 1]


def test_random() -> None:
    """
    ============================================================================
     Test the random method.
    ============================================================================
    """
    graph = GenGraphPath.gen_random(rows=10, pct_invalid=20)
    assert len(graph) == 80
