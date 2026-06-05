from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.protocols.equality.main import SupportsEquality

ULazy.install(globals(), {'SupportsEquality': 'f_core.protocols.equality.main:SupportsEquality'})
