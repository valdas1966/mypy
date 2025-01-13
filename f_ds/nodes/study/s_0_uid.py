from f_ds.nodes.i_0_uid import NodeUid


def study_1():
    node_a = NodeUid(uid=1, name='A')
    print(node_a)

    node_b = NodeUid(uid='B')
    print(node_b)
