"""
===============================================================================
 OMSPP step s_1 -- sample the GOAL pool: sizeable ClusterDiamond regions
 (steps=20, min_cells=200), one CSV row per candidate goal region. Each
 region is large enough that k goals can later be drawn from it (s_3).

 Thin wrapper over the shared sampler `f_hs.experiments.u_cluster_pool`.
 GOAL pool and START pool (s_0) are the SAME sampler with different
 (steps, min_cells) -- here a region (steps>=1, min_cells=k) instead of a
 single cell.

   in:  Experiments/Grids/grids.pkl       (name -> GridMap bundle)
   out: Experiments/OMSPP/i_1_clusters_goals.csv
   n=100, seed=0; max_tries=10_000 -- sparse mazes need many attempts to
   expand a 200-cell diamond from a random center.
===============================================================================
"""
import logging

from f_log import setup_log

from f_hs.experiments.u_cluster_pool import generate_pool_csv


setup_log(sink='console', level=logging.INFO)


if __name__ == '__main__':
    # GOAL pool: regions of >= 200 cells. seed=0 makes the pool
    # reproducible -- re-running regenerates it and cascades to the
    # downstream i_2 / i_3 artifacts (see s_0 note).
    generate_pool_csv(
        path_drive_grids_pkl='Experiments/Grids/grids.pkl',
        path_drive_csv='Experiments/OMSPP/i_1_clusters_goals.csv',
        steps=20,
        min_cells=200,
        n=100,
        seed=0,
        max_tries=10_000)
    logging.getLogger(__name__).info('--- done ---')
