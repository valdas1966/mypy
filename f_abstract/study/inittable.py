from f_abstract.inittable import Inittable


class T(Inittable):

    def _add_kwargs(self) -> None:
        self.b = 2


t = T(a=1)
print(t.a, t.b)
kwargs = t._filter_kwargs(keys=['b'])
print(kwargs)
