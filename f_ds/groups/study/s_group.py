from f_ds.groups.group import Group


g_a = Group(name='A', data=[3, 3])
g_b = Group(name='B', data=[2])

print(g_a.key_comparison())
print(g_b.key_comparison())
print(g_a.key_comparison() < g_b.key_comparison())
print(g_a < g_b)
