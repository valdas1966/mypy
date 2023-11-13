from f_heuristic_search.problem_types.spp import SPP
from f_data_structure.f_tree.node import Node


def test_spp():
    a = Node(name='A')
    b = Node(name='B')
    c = Node(name='C')
    nodes = [a, b, c]
    edges = {a: [b, c], b: [a], c: [a]}
    spp = SPP(start=a, goal=c, )