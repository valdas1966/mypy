from f_ds.groups.view import View, Group


def is_even(n: int) -> bool:
    return n % 2 == 0


data = list(range(1, 11))
group = Group(name='All Numbers', data=data)
print(group)

view = View(name='Even Numbers', group=group, predicate=is_even)
print(view)
print(len(view))
print(view.pct())

group.remove(10)
print(group)
print(view)
print(len(view))
print(view.pct())
print(4/9)
