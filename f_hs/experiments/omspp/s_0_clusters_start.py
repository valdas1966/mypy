"""
===============================================================================
 OMSPP step s_0 -- sample the START pool: single-cell candidates
 (steps=0, min_cells=1), one CSV row per candidate start cell.

 Thin wrapper over the shared sampler `f_hs.experiments.u_cluster_pool`.
 The START pool is just the (steps=0, min_cells=1) special case of the
 general cluster-pool sampler; s_1 reuses the same sampler for the GOAL
 pool with (steps>=1, min_cells=k).

   in:  Experiments/Grids/grids.pkl       (name -> GridMap bundle)
   out: Experiments/OMSPP/i_0_clusters_start.csv
   n=100, seed=0 (reproducible pool).
===============================================================================
"""
import logging

from f_log import setup_log

from f_hs.experiments.u_cluster_pool import generate_pool_csv


setup_log(sink='console', level=logging.INFO)


if __name__ == '__main__':
    # START pool: single cells. seed=0 makes the pool reproducible --
    # NOTE: re-running regenerates the pool and would cascade to the
    # downstream i_2 pairs / i_3 problems, which are pinned to the
    # current Drive artifact. Re-run only to deliberately regenerate.
    generate_pool_csv(
        path_drive_grids_pkl='Experiments/Grids/grids.pkl',
        path_drive_csv='Experiments/OMSPP/i_0_clusters_start.csv',
        steps=0,
        min_cells=1,
        n=100,
        seed=0)
    logging.getLogger(__name__).info('--- done ---')
