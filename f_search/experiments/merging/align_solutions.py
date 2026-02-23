from f_utils import u_pickle
from f_search.problems import ProblemOMSPP as Problem


def align_solutions(path_problems: str,
                    path_solutions: str,
                    path_output: str) -> None:
    """
    ============================================================================
     Align solutions list to match problems list order.
     Output aligned solutions to pickle file.
    ============================================================================
    """
    problems: list[Problem] = u_pickle.load(path=path_problems)
    solutions: list = u_pickle.load(path=path_solutions)
    print(f'Loaded {len(problems)} problems, {len(solutions)} solutions')
    # Build index: (grid, start, goals) -> solution
    solution_map: dict = {}
    for solution in solutions:
        prob = solution.problem
        key = (prob.grid, prob.start, tuple(prob.goals))
        solution_map[key] = solution
    # Align solutions to problems order
    aligned: list = []
    missing: list[int] = []
    for i, problem in enumerate(problems):
        key = (problem.grid, problem.start, tuple(problem.goals))
        if key in solution_map:
            aligned.append(solution_map[key])
        else:
            missing.append(i)
    if missing:
        print(f'Missing solutions for {len(missing)} problems at indices: {missing[:10]}...')
        return
    u_pickle.dump(obj=aligned, path=path_output)
    print(f'Saved {len(aligned)} aligned solutions to: {path_output}')


def main() -> None:
    path_problems = 'f:\\paper\\i_3_problems\\100k\\problems.pkl'
    path_solutions = 'f:\\paper\\i_4_solutions\\dijkstra\\dijkstra.pkl'
    path_output = 'f:\\paper\\i_4_solutions\\dijkstra\\dijkstra_aligned.pkl'
    align_solutions(path_problems=path_problems,
                    path_solutions=path_solutions,
                    path_output=path_output)


if __name__ == '__main__':
    main()