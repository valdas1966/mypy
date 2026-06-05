from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.heuristics.phi.main import UPhi
    from f_search.heuristics.phi.main import PhiFunc

ULazy.install(globals(), {
    'UPhi': 'f_search.heuristics.phi.main:UPhi',
    'PhiFunc': 'f_search.heuristics.phi.main:PhiFunc',
})
