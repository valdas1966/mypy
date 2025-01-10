from f_ds.linked_list import LinkedList, NodePrevNext as Node
import pytest


@pytest.fixture
def node_a() -> Node:
    """
    ========================================================================
     Create a Node with name 'A'.
    ========================================================================
    """
    return Node(name='A', uid='A')


@pytest.fixture
def node_b() -> Node:
    """
    ========================================================================
     Create a Node with name 'B'.
    ========================================================================
    """
    return Node(name='B', uid='B')


@pytest.fixture
def node_c() -> Node:
    """
    ========================================================================
     Create a Node with name 'C'.
    ========================================================================
    """
    return Node(name='C', uid='C')


@pytest.fixture
def linked_1(node_a: Node, node_b: Node) -> LinkedList:
    """
    ========================================================================
     Create a Linked-List with two nodes (A -> B).
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


def test_linked_list_init(linked_1: LinkedList, linked_2: LinkedList):
    """
    ========================================================================
     Test the initialization of the Linked-List and append_list()
    ========================================================================
    """
    assert linked_1.name == 'L1'
    assert linked_2.name == 'L2'
    linked_1.append_list(list=linked_2)
    assert linked_1.head == linked_2.head
    assert linked_1.tail == linked_2.tail
    assert len(linked_1) == 3
