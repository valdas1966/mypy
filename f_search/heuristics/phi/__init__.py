from f_core.imports import ULazy

ULazy.install(globals(), {
    'UPhi': 'f_search.heuristics.phi.main:UPhi',
    'PhiFunc': 'f_search.heuristics.phi.main:PhiFunc',
})
