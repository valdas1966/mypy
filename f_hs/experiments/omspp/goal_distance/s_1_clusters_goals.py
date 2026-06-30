"""
===============================================================================
 goal_distance step s_1 -- sample the GOAL pool: sizeable ClusterDiamond
 regions (steps=20, min_cells=200), one CSV row per candidate goal region.

 Thin wrapper over the shared sampler `f_hs.experiments.u_cluster_pool`
 (GOAL pool = same sampler as s_0 with steps>=1, min_cells=k). Mirrors the
 parent OMSPP s_1 but writes to the goal_distance sub-folder.

 Each region must hold >= k cells AT THE SMALLEST radius the downstream
 sweep rebuilds (max_steps=20), so it is sampled at steps=20,
 min_cells=200 -- the centers it yields are guaranteed to support k=200
 goals at every max_steps in {20..60} (the region only grows). s_2 keeps
 only the region CENTER (the radius is re-grown per max_steps in s_3).

   in:  Experiments/Grids/grids.pkl       (name -> GridMap bundle)
   out: Experiments/OMSPP/goal_distance/i_1_clusters_goals.csv
   n=200, seed=0; max_tries=10_000 -- sparse mazes need many attempts to
   expand a 200-cell diamond from a random center.
===============================================================================
"""
import logging

from f_log import setup_log

from f_hs.experiments.u_cluster_pool import generate_pool_csv


setup_log(sink='console', level=logging.INFO)


if __name__ == '__main__':
    # GOAL pool: regions of >= 200 cells at steps=20 -- guarantees k=200
    # is drawable at every max_steps the sweep rebuilds. n=200 for band
    # coverage; seed=0 reproducible (cascades downstream -- see s_0 note).
    generate_pool_csv(
        path_drive_grids_pkl='Experiments/Grids/grids.pkl',
        path_drive_csv=(
            'Experiments/OMSPP/goal_distance/i_1_clusters_goals.csv'),
        steps=20,
        min_cells=200,
        n=200,
        seed=0,
        max_tries=10_000)
    logging.getLogger(__name__).info('--- done ---')
