from collections import namedtuple

Dimensions = namedtuple('list', 'x y z', defaults=(0, 0, 0))
Point = namedtuple('Point', 'name dimensions', defaults=('Point', Dimensions()))
p = Point()
print(p)