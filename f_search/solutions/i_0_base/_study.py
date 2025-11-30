from f_search.solutions import SolutionSearch


solution_valid = SolutionSearch.Factory.zero_valid()
print(solution_valid.record)

solution_invalid = SolutionSearch.Factory.zero_invalid()
print(solution_invalid.record)
