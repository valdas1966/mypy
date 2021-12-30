from collections import namedtuple

Dimensions = namedtuple('a', 'x y z', defaults=(0, 0, 0))
Point = namedtuple('Point', 'name dimensions', defaults=('Point', Dimensions()))
p = Point()
print(p)