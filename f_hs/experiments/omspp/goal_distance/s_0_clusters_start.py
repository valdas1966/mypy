"""
===============================================================================
 goal_distance step s_0 -- sample the START pool: single-cell candidates
 (steps=0, min_cells=1), one CSV row per candidate start cell.

 Thin wrapper over the shared sampler `f_hs.experiments.u_cluster_pool`
 (the START pool is the (steps=0, min_cells=1) special case). Mirrors the
 parent OMSPP s_0, but writes to the goal_distance sub-folder so the
 sub-experiment owns its own pools -- the parent k-sweep pools are never
 touched.

 These start cells are paired with the s_1 goal regions in s_2 to populate
 the min_dist distance bands (the deterministic-ray s_2 is retired -- the
 geometry is now sampled from real pools and binned by distance).

   in:  Experiments/Grids/grids.pkl       (name -> GridMap bundle)
   out: Experiments/OMSPP/goal_distance/i_0_clusters_start.csv
   n=200, seed=0 (reproducible pool).
===============================================================================
"""
import logging

from f_log import setup_log

from f_hs.experiments.u_cluster_pool import generate_pool_csv


setup_log(sink='console', level=logging.INFO)


if __name__ == '__main__':
    # START pool: single cells. n=200 (larger than the parent's 100) so
    # the s_2 distance bands -- especially the far 400/500 bands -- have
    # enough candidate pairs to fill the replicates. seed=0 makes the pool
    # reproducible; re-running regenerates it and cascades to the
    # downstream i_2 pairs / i_3 problems (re-run only to regenerate).
    generate_pool_csv(
        path_drive_grids_pkl='Experiments/Grids/grids.pkl',
        path_drive_csv=(
            'Experiments/OMSPP/goal_distance/i_0_clusters_start.csv'),
        steps=0,
        min_cells=1,
        n=200,
        seed=0)
    logging.getLogger(__name__).info('--- done ---')
