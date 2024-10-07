from f_abstract.components.nested_group import NestedGroup, Group


b = Group(name='B')
c = Group(name='C')
nested = NestedGroup(name='A', data=[b, c])

for g in nested:
    print(str(g))

print(nested)

