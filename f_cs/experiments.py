import os
import json
from typing import Callable, Optional
from datetime import datetime
from f_utils import u_pickle
from f_cs.algo import Algo
from f_cs.problem import ProblemAlgo
from f_cs.solution import SolutionAlgo


class ExperimentsRunner:
    """
    ============================================================================
     Generic experiments runner for running algorithms on problems.

     Usage:
         1. Create problems.pkl file in a folder
         2. Create runner with algo_factory and folder path
         3. Call run() to process all problems

     The runner will:
         - Load problems from problems.pkl
         - Create/load solutions.pkl (parallel list to problems)
         - Track progress in .progress.json
         - Skip already completed problems (resume capability)
         - Save after each solution (crash-safe)
    ============================================================================
    """

    def __init__(self,
                 algo_factory: Callable[[ProblemAlgo], Algo],
                 folder_path: str) -> None:
        """
        ========================================================================
         Initialize the experiments runner.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            algo_factory: Callable that takes a problem and returns an algo
            folder_path: Path to folder containing problems/solutions/progress
        ========================================================================
        """
        self._algo_factory = algo_factory
        self._folder_path = folder_path

        # File paths
        self._problems_path = os.path.join(folder_path, 'problems.pkl')
        self._solutions_path = os.path.join(folder_path, 'solutions.pkl')
        self._progress_path = os.path.join(folder_path, '.progress.json')

        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Load or initialize data
        self._problems = self._load_problems()
        self._solutions = self._load_solutions()
        self._progress = self._load_progress()

    def _load_problems(self) -> list[ProblemAlgo]:
        """
        ========================================================================
         Load problems from pickle file.
        ========================================================================
        """
        if not os.path.exists(self._problems_path):
            raise FileNotFoundError(
                f"Problems file not found: {self._problems_path}\n"
                f"Please create a problems.pkl file in the folder."
            )
        return u_pickle.load(path=self._problems_path)

    def _load_solutions(self) -> list[Optional[SolutionAlgo]]:
        """
        ========================================================================
         Load solutions from pickle file, or create empty list.
        ========================================================================
        """
        if os.path.exists(self._solutions_path):
            solutions = u_pickle.load(path=self._solutions_path)
            # Extend if problems were added
            if len(solutions) < len(self._problems):
                solutions.extend([None] * (len(self._problems) - len(solutions)))
            return solutions
        else:
            # Create empty solutions list (same length as problems)
            return [None] * len(self._problems)

    def _load_progress(self) -> dict:
        """
        ========================================================================
         Load progress from JSON file.
        ========================================================================
        """
        if os.path.exists(self._progress_path):
            with open(self._progress_path, 'r') as f:
                return json.load(f)
        else:
            # Initialize progress
            return {
                'last_completed_idx': -1,
                'total_problems': len(self._problems),
                'completed_count': 0,
                'last_updated': None
            }

    def _save_solutions(self) -> None:
        """
        ========================================================================
         Save all solutions to pickle file.
        ========================================================================
        """
        u_pickle.dump(obj=self._solutions, path=self._solutions_path)

    def _save_progress(self) -> None:
        """
        ========================================================================
         Save progress to JSON file.
        ========================================================================
        """
        with open(self._progress_path, 'w') as f:
            json.dump(self._progress, f, indent=2)

    def run(self,
            start_idx: Optional[int] = None,
            verbose: bool = True) -> None:
        """
        ========================================================================
         Run experiments on all unsolved problems.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            start_idx: Index to start from (None = resume from last progress)
            verbose: Print progress information
        ========================================================================
        """
        # Determine starting index
        if start_idx is None:
            start_idx = self._progress['last_completed_idx'] + 1

        total_problems = len(self._problems)

        if verbose:
            print("=" * 80)
            print("Starting Experiments")
            print("=" * 80)
            print(f"Total problems: {total_problems}")
            print(f"Starting from index: {start_idx}")
            print(f"Remaining: {total_problems - start_idx}")
            print("=" * 80)
            print()

        # Run experiments
        for idx in range(start_idx, total_problems):
            if verbose:
                print(f"[{idx + 1}/{total_problems}] Running problem {idx}...",
                      end=' ', flush=True)

            try:
                # Get problem
                problem = self._problems[idx]

                # Create algorithm instance
                algo = self._algo_factory(problem)

                # Run algorithm
                solution = algo.run()

                # Store solution
                self._solutions[idx] = solution

                # Update progress
                self._progress['last_completed_idx'] = idx
                self._progress['completed_count'] = sum(
                    1 for s in self._solutions if s is not None
                )
                self._progress['last_updated'] = datetime.now().isoformat()

                # Save after each problem (crash-safe)
                self._save_solutions()
                self._save_progress()

                if verbose:
                    status = "✓" if solution.is_valid else "✗"
                    stats_str = f"(valid={solution.is_valid}"
                    if hasattr(solution.stats, 'explored'):
                        stats_str += f", explored={solution.stats.explored}"
                    if hasattr(solution.stats, 'generated'):
                        stats_str += f", generated={solution.stats.generated}"
                    if hasattr(solution.stats, 'elapsed'):
                        stats_str += f", time={solution.stats.elapsed:.2f}s"
                    stats_str += ")"
                    print(f"{status} {stats_str}")

            except Exception as e:
                if verbose:
                    print(f"✗ ERROR: {str(e)}")
                # Continue to next problem
                continue

        if verbose:
            print()
            print("=" * 80)
            print("Experiments Completed!")
            print("=" * 80)
            print(f"Total completed: {self._progress['completed_count']}/{total_problems}")
            print()

    @property
    def problems(self) -> list[ProblemAlgo]:
        """
        ========================================================================
         Return the list of problems.
        ========================================================================
        """
        return self._problems

    @property
    def solutions(self) -> list[Optional[SolutionAlgo]]:
        """
        ========================================================================
         Return the list of solutions.
        ========================================================================
        """
        return self._solutions

    @property
    def progress(self) -> dict:
        """
        ========================================================================
         Return the progress dictionary.
        ========================================================================
        """
        return self._progress
