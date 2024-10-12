from f_abstract.components.groups.nested import NestedGroup, Group


b = Group(name='B')
c = Group(name='C')
nested = NestedGroup(name='A', data=[b, c])

for g in nested:
    print(str(g))

print(nested)

