from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:                      # never runs — analyzers only
    from f_core.canonize.u_canonize import canonize

ULazy.install(globals(), {
    'canonize': 'f_core.canonize.u_canonize:canonize',
})
