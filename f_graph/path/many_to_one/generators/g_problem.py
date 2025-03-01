from f_graph.path.many_to_one.problem import ProblemManyToOne, Node
from f_graph.path.generators.g_graph import GenGraphPath, Graph


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
                        percentile_min: int,
                        percentile_max: int,
                        distance_starts: int = 10,
                        ) -> ProblemManyToOne:
        """
        ========================================================================
         Generate a Many-to-One problem for experiments.
        ========================================================================
        """
        starts: list[Node] = None
        goal: Node = None
        while True:
            start_1 = graph.sample(size=1)[0]
            candidate_goals = graph.nodes_within_percentile(node=start_1,
                                                            percentile_min=percentile_min,
                                                            percentile_max=percentile_max)
            # print(f'Candidate Goals: {len(candidate_goals)}')
            if not candidate_goals:
                continue
            goal = candidate_goals.sample(size=1)[0]
            candidates_starts = graph.nodes_within_distance(node=start_1,
                                                            distance_max=distance_starts)
            if goal in candidates_starts:
                candidates_starts.remove(goal)
            # print(f'Candidate Starts: {len(candidates_starts)}')
            if len(candidates_starts) < n_starts - 1:
                continue
            starts = candidates_starts.sample(size=n_starts-1)
            starts.append(start_1)
            break
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)
