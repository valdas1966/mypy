from f_ds.linked_list import LinkedList, NodePrevNext as Node
import pytest


@pytest.fixture
def node_a() -> Node:
    """
    ========================================================================
     Create a Node with name 'A'.
    ========================================================================
    """
    return Node(uid='A')


@pytest.fixture
def node_b() -> Node:
    """
    ========================================================================
     Create a Node with name 'B'.
    ========================================================================
    """
    return Node(uid='B')


@pytest.fixture
def node_c() -> Node:
    """
    ========================================================================
     Create a Node with name 'C'.
    ========================================================================
    """
    return Node(uid='C')


@pytest.fixture
def linked_1(node_a: Node, node_b: Node) -> LinkedList:
    """
    ========================================================================
     Create a Linked-List with two old_nodes (A -> B).
    ========================================================================
    """
    linked = LinkedList(name='L1')
    linked.append(node_a)
    linked.append(node_b)
    return linked


@pytest.fixture
def linked_2(node_c: Node) -> LinkedList:
    """
    ========================================================================
     Create a Linked-List with one node (C).
    ========================================================================
    """
    linked = LinkedList(name='L2')
    linked.append(node_c)
    return linked


def test_init_and_append(linked_1: LinkedList, linked_2: LinkedList):
    """
    ========================================================================
     Test the initialization of the Linked-List and append_list()
    ========================================================================
    """
    assert linked_1.name == 'L1'
    assert linked_2.name == 'L2'
    assert len(linked_1) == 2
    assert len(linked_2) == 1


def test_empty():
    """
    ========================================================================
     Test empty LinkedList behavior
    ========================================================================
    """
    linked_empty = LinkedList(name='Empty')
    assert not linked_empty
    assert len(linked_empty) == 0
    assert linked_empty.head is None
    assert str(linked_empty) == 'Empty: None'


def test_chain(linked_1: LinkedList, linked_2: LinkedList):
    """
    ========================================================================
     Test chain() method
    ========================================================================
    """
    linked = linked_1.chain(node=linked_2.head, name='L3')
    assert len(linked) == 3
    assert [node.uid for node in linked] == ['A', 'B', 'C']


def test_to_group(linked_1: LinkedList):
    """
    ========================================================================
     Test to_group() method
    ========================================================================
    """
    group = linked_1.to_group(name='test_group')
    assert len(group) == 2
    assert [node.uid for node in group] == ['A', 'B']


def test_str(linked_1: LinkedList):
    """
    ========================================================================
     Test string representation
    ========================================================================
    """
    assert str(linked_1) == 'L1: NodePrevNext(A) -> NodePrevNext(B)'


def test_iteration(linked_1: LinkedList):
    """
    ========================================================================
     Test iteration over LinkedList
    ========================================================================
    """
    nodes = list(linked_1)
    assert len(nodes) == 2
    assert [node.uid for node in nodes] == ['A', 'B']


def test_from_list(node_a: Node, node_b: Node):
    """
    ========================================================================
     Test from_list() method
    ========================================================================
    """
    li = [node_a, node_b]
    linked = LinkedList.from_list(li=li)
    assert [node.uid for node in linked] == ['A', 'B']
    assert node_a.prev is None
    assert node_a.next == node_b
    assert node_b.prev == node_a
    assert node_b.next is None


def test_reverse(linked_1: LinkedList):
    """
    ========================================================================
     Test reverse() method
    ========================================================================
    """
    linked_reverse = linked_1.reverse()
    assert [node.uid for node in linked_reverse] == ['B', 'A']


def test_clone(linked_1: LinkedList):
    """
    ========================================================================
     Test clone() method
    ========================================================================
    """
    cloned = linked_1.clone()
    cloned.remove_all()
    assert cloned.head is None
    assert linked_1.head is not None
