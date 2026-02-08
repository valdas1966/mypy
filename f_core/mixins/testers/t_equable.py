from f_core.mixins.equatable.main import Equatable
from f_core.protocols.equable import Equable as ProtocolEquable


class C(Equatable):

    def key_comparison(self) -> ProtocolEquable:
        return 1, 1


a = C()
b = C()

print(a == b)
