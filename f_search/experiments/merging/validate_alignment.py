from f_utils import u_pickle
from f_search.problems import ProblemOMSPP as Problem


def validate_alignment(path_problems: str, path_solutions: str) -> bool:
    """
    ============================================================================
     Validate that problems and solutions lists are aligned.
     Each index should have the same problem.
    ============================================================================
    """
    problems: list[Problem] = u_pickle.load(path=path_problems)
    solutions: list = u_pickle.load(path=path_solutions)
    if len(problems) != len(solutions):
        print(f'Length mismatch: {len(problems)} problems, {len(solutions)} solutions')
        return False
    for i, (problem, solution) in enumerate(zip(problems, solutions)):
        sol_problem = solution.problem
        is_grid_equal = problem.grid == sol_problem.grid
        is_start_equal = problem.start == sol_problem.start
        is_goals_equal = problem.goals == sol_problem.goals
        if not (is_grid_equal and is_start_equal and is_goals_equal):
            print(f'Mismatch at index {i}:')
            if not is_grid_equal:
                print(f'  Grid: {problem.grid} != {sol_problem.grid}')
            if not is_start_equal:
                print(f'  Start: {problem.start} != {sol_problem.start}')
            if not is_goals_equal:
                print(f'  Goals: {problem.goals} != {sol_problem.goals}')
            return False
    print(f'Validated: {len(problems)} problems aligned with solutions')
    return True


def main() -> None:
    path_problems = 'f:\\paper\\i_3_problems\\100k\\problems.pkl'
    path_solutions = 'f:\\paper\\i_4_solutions\\aggregative\\aggregative.pkl'
    validate_alignment(path_problems=path_problems, path_solutions=path_solutions)


if __name__ == '__main__':
    main()