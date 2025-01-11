from f_ds.nodes.i_1_prev_next import NodePrevNext
from f_ds.mixins.has_head import HasHead
from f_core.mixins.has_name import HasName


def study_1():
    a = HasName('A')
    b = HasName('B')
    li = HasHead()
    print(li.head)
    li.head = a
    print(li.head)
    li.head = b
    print(li.head)
    print(a)
    a = b
    print(a)


def study_2():
    a = NodePrevNext(uid='A')
    b = NodePrevNext(uid='B')
    li = HasHead()
    print(li.tail)
    li.tail = a
    print(li.tail)
    li.tail.next = b
    print(li.tail, b.prev)
    li.tail = b
    print(li.tail, li.tail.prev, b.prev, a.next, b.next)


# study_1()
study_2()
