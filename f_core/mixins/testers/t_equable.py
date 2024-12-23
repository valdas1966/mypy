from f_core.mixins.equable import Equable
from f_core.protocols.equable import Equable as ProtocolEquable


class C(Equable):

    def key_comparison(self) -> ProtocolEquable:
        return 1, 1


a = C()
b = C()

print(a == b)
