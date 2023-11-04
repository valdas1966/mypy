from f_data_structure.mixins.hierarchical import Hierarchical


a = Hierarchical(name='A')
print(a, a.parent, a.children)

b = Hierarchical(name='B', parent=a)
print(a, a.parent, a.children)
print(b, b.parent, b.children)