from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.protocols.equality import SupportsEquality
    from f_core.protocols.comparison import SupportsComparison
    from f_core.protocols.bounds import SupportsBounds

ULazy.install(globals(), {
    'SupportsEquality': 'f_core.protocols.equality:SupportsEquality',
    'SupportsComparison': 'f_core.protocols.comparison:SupportsComparison',
    'SupportsBounds': 'f_core.protocols.bounds:SupportsBounds',
})
