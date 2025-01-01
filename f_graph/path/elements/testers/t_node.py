from f_graph.path.elements.node import NodePath as Node


def test_key_comparison():
    a = Node(uid='a', h=0)
    b = Node(uid='b', h=0)
    assert a < b


def test_generate_branch():
    branch_true = [Node(uid=i) for i in range(3)]
    branch_true[1].parent = branch_true[0]
    branch_true[2].parent = branch_true[1]
    assert Node.generate_branch(depth=3) == branch_true
