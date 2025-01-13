from f_ds.linked_list import LinkedList, NodePrevNext as Node


def study_1():
    a = Node(uid='A')
    b = Node(uid='B')
    c = Node(uid='C')
    a.next = b
    linked = LinkedList()
    linked.append(node=a)
    print(linked)
    #linked.append(node=b)
    #print(linked)
    linked.append(node=c)
    print(linked)


def clone():
    node_a = Node(uid='A')
    node_b = Node(uid='B')
    linked = LinkedList()
    linked.append(node_a)
    linked.append(node_b)
    li = [node.clone() for node in linked]
    print(li)


def reverse():
    linked = LinkedList.gen_abc()
    print(linked)
    cloned = linked.clone('Cloned')
    print(cloned)
    li = list(reversed(list(cloned)))
    print(li)
    for node in li:
        node.detach()
        print(node, node.prev, node.next)
    rev = LinkedList.from_list(li=li, name='Reversed')
    print(rev)


# clone()
reverse()
