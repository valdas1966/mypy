from f_graph.path.cache.i_1_explored import CacheExplored, Node


branch = Node.generate_branch(depth=3)
explored = set(branch)
cache = CacheExplored(explored=explored)
for node in cache:
    print(node.uid)
    print([node.uid for node in cache[node].path()])
    print(cache[node].distance())