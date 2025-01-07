from f_ds.mixins.has_hierarchy import HasHierarchy


root = HasHierarchy(name='root')
leaf = HasHierarchy(name='leaf')
leaf.parent = root
print(root.children())
print(leaf in root.children())
