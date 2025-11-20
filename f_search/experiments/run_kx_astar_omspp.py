from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_search.ds.state import State
from f_search.problems.i_1_omspp import ProblemOMSPP
from f_search.algos.i_2_omspp.i_1_kx_astar import KxAStar
from f_utils import u_pickle
from collections import defaultdict
import time
import os


def print_header() -> None:
    """
    ============================================================================
     Print the header of the script.
    ============================================================================
    """
    print("=" * 80)
    print("Run KxAStar on OMSPP Problems")
    print("=" * 80)
    print()


def load_problems() -> dict[str, dict[str, dict[int, list[dict]]]]:
    """
    ============================================================================
     Load problem details from pickle file.
     Structure: domain->map->percentile->list[problem_dicts]
    ============================================================================
    """
    print("Loading problems from g:\\paper\\problems_omspp.pkl...")
    problems = u_pickle.load(path='g:\\paper\\problems_omspp.pkl')

    total_problems = sum(
        len(problem_list)
        for domain_maps in problems.values()
        for map_problems in domain_maps.values()
        for problem_list in map_problems.values()
    )

    print(f"Loaded {len(problems)} domains")
    print(f"Total problems: {total_problems}")
    print()
    return problems


def load_existing_results() -> dict[str, dict[str, dict[int, list[dict]]]]:
    """
    ============================================================================
     Load existing results if available, otherwise return empty structure.
    ============================================================================
    """
    results_path = 'g:\\paper\\results_omspp.pkl'

    if os.path.exists(results_path):
        print(f"Loading existing results from {results_path}...")
        results = u_pickle.load(path=results_path)

        total_completed = sum(
            len(result_list)
            for domain_maps in results.values()
            for map_results in domain_maps.values()
            for result_list in map_results.values()
        )

        print(f"Found {total_completed} completed problems")
        print()
        return results
    else:
        print("No existing results found, starting fresh")
        print()
        return defaultdict(lambda: defaultdict(lambda: defaultdict(list)))


def is_problem_completed(
    results: dict,
    domain: str,
    map_name: str,
    percentile: int,
    problem_idx: int
) -> bool:
    """
    ============================================================================
     Check if a specific problem has already been completed.
    ============================================================================
    """
    if domain not in results:
        return False
    if map_name not in results[domain]:
        return False
    if percentile not in results[domain][map_name]:
        return False

    # Check if we have a result at this index
    results_list = results[domain][map_name][percentile]
    return problem_idx < len(results_list)


def load_grid(
    grids_cache: dict,
    domain: str,
    map_name: str,
    current_domain: list,
    current_map: list
) -> Grid:
    """
    ============================================================================
     Load grid on-demand with caching.
     Only loads grids.pkl when switching to a new domain/map.
    ============================================================================
    """
    # Check if we need to reload grids.pkl
    if current_domain[0] != domain or current_map[0] != map_name:
        # Clear cache if switching domain/map
        if current_domain[0] != domain or current_map[0] != map_name:
            grids_cache.clear()

        # Load only the specific grid we need
        all_grids = u_pickle.load(path='g:\\paper\\grids.pkl')

        if domain not in all_grids or map_name not in all_grids[domain]:
            raise ValueError(f"Grid not found: {domain}/{map_name}")

        grids_cache['current'] = all_grids[domain][map_name]
        current_domain[0] = domain
        current_map[0] = map_name

    return grids_cache['current']


def save_results(results: dict) -> None:
    """
    ============================================================================
     Save results to pickle file.
    ============================================================================
    """
    results_path = 'g:\\paper\\results_omspp.pkl'
    # Convert defaultdict to regular dict for pickling
    results_dict = {
        domain: {
            map_name: {
                percentile: result_list
                for percentile, result_list in map_results.items()
            }
            for map_name, map_results in domain_maps.items()
        }
        for domain, domain_maps in results.items()
    }
    u_pickle.dump(obj=results_dict, path=results_path)


def run_experiments(
    problems: dict[str, dict[str, dict[int, list[dict]]]],
    results: dict[str, dict[str, dict[int, list[dict]]]]
) -> dict[str, dict[str, dict[int, list[dict]]]]:
    """
    ============================================================================
     Run KxAStar on all problems, skipping already completed ones.
    ============================================================================
    """
    # Convert results to defaultdict if needed
    if not isinstance(results, defaultdict):
        results_dd = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for domain, domain_maps in results.items():
            for map_name, map_results in domain_maps.items():
                for percentile, result_list in map_results.items():
                    results_dd[domain][map_name][percentile] = result_list
        results = results_dd

    # Calculate total problems
    total_problems = sum(
        len(problem_list)
        for domain_maps in problems.values()
        for map_problems in domain_maps.values()
        for problem_list in map_problems.values()
    )

    # Count already completed
    completed_count = sum(
        len(result_list)
        for domain_maps in results.values()
        for map_results in domain_maps.values()
        for result_list in map_results.values()
    )

    remaining = total_problems - completed_count

    print("=" * 80)
    print("Starting experiments...")
    print(f"Total problems: {total_problems}")
    print(f"Already completed: {completed_count}")
    print(f"Remaining: {remaining}")
    print("=" * 80)
    print()

    # Grid cache and current tracking
    grids_cache = {}
    current_domain = [None]
    current_map = [None]

    problem_counter = 0
    skipped_counter = 0
    start_time = time.time()

    # Process each domain
    for domain, maps in problems.items():
        print(f"Domain: {domain}")
        print("  " + "-" * 76)

        # Process each map
        for map_name, percentile_problems in maps.items():

            # Process each percentile
            for percentile, problem_list in percentile_problems.items():
                print(f"  Map: {map_name}, Percentile: {percentile} ({len(problem_list)} problems)")

                # Process each problem
                for problem_idx, problem_dict in enumerate(problem_list):
                    problem_counter += 1

                    # Check if already completed
                    if is_problem_completed(results, domain, map_name, percentile, problem_idx):
                        skipped_counter += 1
                        print(f"    [{problem_counter}/{total_problems}] Problem {problem_idx + 1} "
                              f"({problem_dict['num_goals']} goals): SKIPPED (already completed)")
                        continue

                    # Print minimal header
                    print(f"    [{problem_counter}/{total_problems}] Problem {problem_idx + 1} "
                          f"({problem_dict['num_goals']} goals): Running...", end='', flush=True)

                    problem_start = time.time()

                    try:
                        # Load grid (on-demand with caching)
                        grid = load_grid(grids_cache, domain, map_name, current_domain, current_map)

                        # Create states from cells
                        start_state = State(key=problem_dict['start'])
                        goal_states = [State(key=goal_cell) for goal_cell in problem_dict['goals']]

                        # Create OMSPP problem
                        problem = ProblemOMSPP(
                            grid=grid,
                            start=start_state,
                            goals=goal_states
                        )

                        # Run KxAStar (verbose=False to avoid printing grid)
                        algo = KxAStar(problem=problem, verbose=True)
                        solution = algo.run()

                        # Create result dict
                        result_dict = {
                            'domain': domain,
                            'map': map_name,
                            'percentile': percentile,
                            'num_goals': problem_dict['num_goals'],
                            'start': problem_dict['start'],
                            'goals': problem_dict['goals'],
                            'stats': solution.stats,
                            'is_valid': bool(solution)
                        }

                        # Add to results
                        results[domain][map_name][percentile].append(result_dict)

                        # Save immediately
                        save_results(results)

                        # Print results on same line
                        problem_elapsed = time.time() - problem_start
                        total_elapsed = time.time() - start_time
                        avg_time = total_elapsed / (problem_counter - skipped_counter) if (problem_counter - skipped_counter) > 0 else 0
                        remaining_problems = total_problems - problem_counter
                        eta_seconds = avg_time * remaining_problems
                        eta_minutes = eta_seconds / 60

                        print(f" ✓ (gen={solution.stats.generated}, "
                              f"exp={solution.stats.explored}, "
                              f"upd={solution.stats.updated}, "
                              f"time={problem_elapsed:.2f}s, "
                              f"avg={avg_time:.2f}s, "
                              f"ETA={eta_minutes:.1f}min)")

                    except Exception as e:
                        print(f"    ✗ ERROR: {str(e)}")
                        # Still save progress even if this problem failed
                        continue

                print()

        print()

    # Final summary
    total_elapsed = time.time() - start_time
    completed_now = problem_counter - skipped_counter

    print("=" * 80)
    print("Experiments completed!")
    print("=" * 80)
    print(f"Total problems processed: {problem_counter}/{total_problems}")
    print(f"Skipped (already done): {skipped_counter}")
    print(f"Completed now: {completed_now}")
    print(f"Total time: {total_elapsed:.2f}s ({total_elapsed/60:.2f} minutes)")
    if completed_now > 0:
        print(f"Average time per problem: {total_elapsed/completed_now:.2f}s")
    print()

    return results


# Main execution
if __name__ == "__main__":
    # Print header
    print_header()

    # Load problems
    problems = load_problems()

    # Load existing results (if any)
    results = load_existing_results()

    # Run experiments
    results = run_experiments(problems, results)

    print("=" * 80)
    print("All done! Results saved to g:\\paper\\results_omspp.pkl")
    print("=" * 80)
