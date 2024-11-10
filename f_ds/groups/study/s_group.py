from f_ds.groups.group import Group


def study_key_comparison():
    g_a = Group(name='A', data=[3, 3])
    g_b = Group(name='B', data=[2])

    print(g_a.key_comparison())
    print(g_b.key_comparison())
    print(g_a.key_comparison() < g_b.key_comparison())
    print(g_a < g_b)


def study_sorted():
    g = Group(data=[3, 2, 1])
    print(g)
    print(type(sorted(g)))


def study_str():
    g = Group(data=[1, 2, 3])
    print(g)


def study_assignment():
    g = Group(data=[1, 2, 3])
    a, *b = g
    print(a, b)


# study_sorted()
# study_str()
study_assignment()
