from f_abstract.mixins.listable import Listable
from f_abstract.mixins.to_list import ToList, Item


class A(ToList):

    def to_list(self) -> Listable[Item]:
        return Listable(data=[1, 2, 3])


a = A()
for item in a:
    print(item)
