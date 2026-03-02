from f_core.mixins.has.children import HasChildren

# Empty
empty = HasChildren.Factory.empty()
print(f'Children: {empty.children}')
# Children: []

# With two children
parent = HasChildren.Factory.with_two()
print(f'Count: {len(parent.children)}')
# Count: 2

# Add dynamically
child = HasChildren()
empty.add_child(child=child)
print(f'After add: {len(empty.children)}')
# After add: 1
