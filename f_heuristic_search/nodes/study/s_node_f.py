from f_heuristic_search.nodes.node_f import NodeF


a = NodeF(x=1, y=1)
a._g, a.h = 7, 3
b = NodeF(x=2, y=2)
b._g, b.h = 4, 6

print(a < b, b > a, a <= b, b >= a, a == b)