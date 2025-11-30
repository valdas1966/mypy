from f_search.solutions import SolutionOMSPP


solution = SolutionOMSPP.Factory.invalid()
print(solution.record)
for path in solution.paths.values():
    print(len(path))
