from f_core.imports import ULazy

ULazy.install(globals(), {
    'Algo': 'f_cs.algo:Algo',
    'ProblemAlgo': 'f_cs.problem:ProblemAlgo',
    'SolutionAlgo': 'f_cs.solution:SolutionAlgo',
})
