"""
================================================================================
 Example usage of ExperimentsRunner

 This example shows how to use the generic ExperimentsRunner class.
================================================================================
"""

from f_cs.experiments import ExperimentsRunner


# Example 1: Basic Usage
# ------------------------------------------------------------------------------
def example_basic():
    """
    Basic usage example with a simple algorithm factory.
    """
    # Define your algorithm factory
    # This function takes a problem and returns an algorithm instance
    def algo_factory(problem):
        # Import your specific algorithm
        from f_search.algos.i_1_spp.i_1_astar import AStar
        return AStar(problem=problem, verbose=False)

    # Create runner with folder containing problems.pkl
    runner = ExperimentsRunner(
        algo_factory=algo_factory,
        folder_path='/path/to/experiments/folder'
    )

    # Run experiments (will resume from last progress automatically)
    runner.run()


# Example 2: Custom Algorithm Configuration
# ------------------------------------------------------------------------------
def example_with_config():
    """
    Example with algorithm configuration parameters.
    """
    # Algorithm factory with custom configuration
    def algo_factory_with_config(problem):
        from f_search.algos.i_2_omspp.i_1_repeated.astar import AStarRepeated
        return AStarRepeated(
            problem=problem,
            verbose=False
            # Add any algorithm-specific parameters here
        )

    runner = ExperimentsRunner(
        algo_factory=algo_factory_with_config,
        folder_path='/path/to/experiments/folder'
    )

    # Start from specific index (useful for manual restart)
    runner.run(start_idx=0)


# Example 3: Using Lambda
# ------------------------------------------------------------------------------
def example_lambda():
    """
    Example using lambda for simple algorithm factory.
    """
    from f_search.algos.i_1_spp.i_2_dijkstra import Dijkstra

    runner = ExperimentsRunner(
        algo_factory=lambda problem: Dijkstra(problem=problem, verbose=False),
        folder_path='/path/to/experiments/folder'
    )

    runner.run(verbose=True)


# Example 4: Access Results After Running
# ------------------------------------------------------------------------------
def example_access_results():
    """
    Example showing how to access problems, solutions, and progress.
    """
    from f_search.algos.i_1_spp.i_1_astar import AStar

    runner = ExperimentsRunner(
        algo_factory=lambda p: AStar(problem=p, verbose=False),
        folder_path='/path/to/experiments/folder'
    )

    # Run experiments
    runner.run()

    # Access results
    problems = runner.problems
    solutions = runner.solutions
    progress = runner.progress

    print(f"Total problems: {len(problems)}")
    print(f"Completed: {progress['completed_count']}")

    # Analyze solutions
    valid_solutions = [s for s in solutions if s and s.is_valid]
    print(f"Valid solutions: {len(valid_solutions)}/{len(solutions)}")

    # Access individual solution stats
    for idx, solution in enumerate(solutions):
        if solution and solution.is_valid:
            print(f"Problem {idx}: explored={solution.stats.explored}")


# Example 5: Creating Problems File
# ------------------------------------------------------------------------------
def example_create_problems():
    """
    Example showing how to create a problems.pkl file.
    """
    from f_utils import u_pickle
    from f_search.problems.i_1_spp import ProblemSPP
    from f_search.ds.state.i_0_base import StateBase
    from f_ds.grids import GridMap

    # Create some example problems
    grid = GridMap(...)  # Your grid initialization
    problems = []

    for i in range(100):
        # Create problem instances
        problem = ProblemSPP(
            grid=grid,
            start=StateBase(key=(0, 0)),
            goal=StateBase(key=(10, 10))
        )
        problems.append(problem)

    # Save to pickle file
    folder_path = '/path/to/experiments/folder'
    u_pickle.dump(obj=problems, path=f'{folder_path}/problems.pkl')

    print(f"Created problems.pkl with {len(problems)} problems")


# Example 6: Resume After Interruption
# ------------------------------------------------------------------------------
def example_resume():
    """
    Example showing automatic resume after interruption.
    """
    from f_search.algos.i_1_spp.i_1_astar import AStar

    # If your script was interrupted, just run again
    # It will automatically resume from where it left off
    runner = ExperimentsRunner(
        algo_factory=lambda p: AStar(problem=p, verbose=False),
        folder_path='/path/to/experiments/folder'
    )

    # This will resume from last completed index in .progress.json
    runner.run()

    # Or manually specify starting index
    # runner.run(start_idx=50)


if __name__ == "__main__":
    # Run the example you want
    # example_basic()
    # example_with_config()
    # example_lambda()
    # example_access_results()
    # example_create_problems()
    # example_resume()
    pass
