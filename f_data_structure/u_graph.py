import networkx as nx


def get_descendants(edges, root):
    """
    ============================================================================
     Description: Get Sequence of Edges and Return the Root Descendants.
    ============================================================================
    """
    assert type(edges) in {tuple, list, set}
    g = nx.Graph()
    for e in edges:
        assert len(e) == 2
        g.add_edge(e[0], e[1])
    return nx.descendants(g, root)
