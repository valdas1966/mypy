from f_graph.path.cache.i_1_explored import CacheExplored, Node


node = Node.generate_zero()
explored: set[Node] = {node}
cache = CacheExplored(explored)
print(cache[node].path())