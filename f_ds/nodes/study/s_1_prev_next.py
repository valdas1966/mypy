from f_ds.nodes.i_2_prev_next import NodePrevNext


def study_1():
    node = NodePrevNext(uid='A')
    print(node)

    cloned = node.clone()
    print(cloned)


def clone():
    node = NodePrevNext(uid='A')
    cloned = node.clone()
    print(type(cloned))


clone()
