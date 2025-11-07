from f_graph.old_path.algos.many_to_one.problem import ProblemManyToOne
from f_graph.old_path.generators.g_graph import GenGraphPath, Graph


class GenProblemManyToOne:
    """
    ============================================================================
     Generator for Many-to-One Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> ProblemManyToOne:

        """
        ========================================================================
         Generate a 3x3 Many-to-One problem.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        starts = [graph[0, 2], graph[2, 2]]
        goal = graph[0, 0]
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)
    
    @staticmethod
    def gen_3x3x3() -> ProblemManyToOne:
        """
        ========================================================================
         Generate a 3x3 Many-to-One problem with 3 starts.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        starts = [graph[0, 2], graph[2, 2], graph[2, 0]]
        goal = graph[0, 0]
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)

    @staticmethod
    def gen_random(rows: int,
                   pct_invalid: int,
                   num_starts: int) -> ProblemManyToOne:
        """
        ========================================================================
         Generate a random Many-to-One problem.
        ========================================================================
        """
        graph = GenGraphPath.gen_random(rows=rows,
                                        pct_invalid=pct_invalid)
        nodes = graph.sample(num_starts + 1)
        starts = nodes[:num_starts]
        goal = nodes[-1]
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)

    @staticmethod
    def spec_4x4() -> ProblemManyToOne:
        """
        ========================================================================
         Generate a 4x4 Many-to-One problem.
        ========================================================================
        """
        graph = GenGraphPath.gen_4x4()
        starts = [graph[1, 2], graph[3, 3], graph[0, 3]]
        goal = graph[0, 2]
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)

    @staticmethod
    def for_experiments(graph: Graph,
                        n_starts: int,
                        epochs: int = 100,
                        ) -> ProblemManyToOne | None:
        """
        ========================================================================
         Generate a Many-to-One problem for experiments.
        ========================================================================
        """
        counter = 0
        while counter < epochs:
            counter += 1
            start_1, goal = graph.sample(size=2)
            cands_starts = graph.nodes_within_distance(node=start_1,
                                                       dist_max=10)
            if goal in cands_starts:
                cands_starts.remove(goal)
            # There are not enough relevant starts in this distance.
            if len(cands_starts) < n_starts - 1:
                continue
            starts = cands_starts.sample(size=n_starts-1)
            starts.append(start_1)
            return ProblemManyToOne(graph=graph, starts=starts, goal=goal)
        return None
