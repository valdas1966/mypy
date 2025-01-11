from f_ds.nodes.mixins.has_hierarchy import HasHierarchy
from f_core.mixins.has_name import HasName


class Node(HasHierarchy, HasName):
    """
    ============================================================================
     Node Class.
    ============================================================================
    """
    def __init__(self, name: str) -> None:
        HasName.__init__(self, name=name)
        HasHierarchy.__init__(self)


root = Node(name='root')
leaf = Node(name='leaf')
leaf.parent = root
print(root.children())
print(leaf in root.children())
