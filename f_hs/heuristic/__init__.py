from f_core.imports import ULazy

ULazy.install(globals(), {
    'HBase': 'f_hs.heuristic.i_0_base:HBase',
    'CacheEntry': 'f_hs.heuristic.i_0_base:CacheEntry',
    'HCallable': 'f_hs.heuristic.i_1_callable:HCallable',
    'HCached': 'f_hs.heuristic.i_1_cached:HCached',
    'HBounded': 'f_hs.heuristic.i_1_bounded:HBounded',
})
