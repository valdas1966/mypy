from f_graph.path.cache.i_0_base import Cache, DataCache, Node
import unittest


class TestCacheExplored(unittest.TestCase):

    def setUp(self):
        self.node_a = Node('A')
        self.node_b = Node('B') 
        self.node_c = Node('C')
        self.node_b.g = 1
        self.node_c.g = 2
        self.node_b.parent = self.node_a
        self.node_c.parent = self.node_b
        self.explored = {self.node_a, self.node_b, self.node_c}
        self.cache = CacheExplored(self.explored)

    def test_init(self):
        self.assertEqual(len(self.cache._data), 3)
        self.assertIn(self.node_a, self.cache._data)
        self.assertIn(self.node_b, self.cache._data)
        self.assertIn(self.node_c, self.cache._data)

    def test_path_calculation(self):
        path_c = self.cache._data[self.node_c].path()
        self.assertEqual(path_c, [self.node_a, self.node_b, self.node_c])

    def test_distance_calculation(self):
        dist_c = self.cache._data[self.node_c].distance()
        self.assertEqual(dist_c, 2)


if __name__ == '__main__':
    unittest.main()


class CacheExplored(Cache):
    """
    ========================================================================
     Cache from Explored-Nodes.
    ========================================================================
    """

    def __init__(self, explored: set[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Cache.__init__(self)
        for node in explored:
            path = lambda: list(reversed(node.path_from()))
            distance = lambda: node.g
            self._data[node] = DataCache(path=path, distance=distance)

