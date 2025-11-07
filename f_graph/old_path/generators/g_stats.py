from f_graph.old_path.core.stats import StatsPath as Stats


class GenStatsPath:
    """
    ========================================================================
     Generate stats.
    ========================================================================
    """

    @staticmethod
    def gen_10x20x30() -> Stats:
        """
        ========================================================================
         Generate a 3x3 stats.
        ========================================================================
        """
        return Stats(elapsed=10, generated=20, explored=30)
    