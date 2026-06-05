from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.heuristic.i_0_base import HBase
    from f_hs.heuristic.i_0_base import CacheEntry
    from f_hs.heuristic.i_1_callable import HCallable
    from f_hs.heuristic.i_1_cached import HCached
    from f_hs.heuristic.i_1_bounded import HBounded

ULazy.install(globals(), {
    'HBase': 'f_hs.heuristic.i_0_base:HBase',
    'CacheEntry': 'f_hs.heuristic.i_0_base:CacheEntry',
    'HCallable': 'f_hs.heuristic.i_1_callable:HCallable',
    'HCached': 'f_hs.heuristic.i_1_cached:HCached',
    'HBounded': 'f_hs.heuristic.i_1_bounded:HBounded',
})
