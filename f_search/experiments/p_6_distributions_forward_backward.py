from f_psl.pandas.csv import UCsv
from f_log import setup_log, get_log
import logging

setup_log(sink='console', level=logging.DEBUG)
log = get_log(__name__)


def dist(path_input: str,
         path_output: str,
         col_group: str,
         cols_value: list[str],
         agg: str = 'mean') -> None:
    """
    ========================================================================
     Generate a single distribution CSV.
    ========================================================================
    """
    log.debug(f'dist -> {path_output}')
    UCsv.group(path_input=path_input,
                path_output=path_output,
                col_a=col_group,
                col_b=cols_value,
                agg=agg)


"""
===============================================================================
 Main - Generate distribution CSVs from analytics.
 Each distribution is a separate function call with its own params.
-------------------------------------------------------------------------------
 Input:  analytics.csv (output of p_5_analytics_forward)
 Output: dist_<name>.csv for each distribution.
===============================================================================
"""

folder = 'f:\\temp\\2026\\03\\forward vs backward'
path_input = f'{folder}\\results.csv'


def elapsed_by_k() -> None:
    dist(path_input=path_input,
         path_output=f'{folder}\\dist_elapsed_by_k.csv',
         col_group='k',
         cols_value=['explored_forward', 'explored_backward',
                     'elapsed_dij', 'elapsed_rep'])


def explored_by_k() -> None:
    dist(path_input=path_input,
         path_output=f'{folder}\\dist_explored_by_k.csv',
         col_group='k',
         cols_value=['explored_agg', 'explored_inc',
                     'explored_dij', 'explored_rep'])


def main() -> None:
    log.info('main started')
    elapsed_by_k()
    explored_by_k()
    log.info('main finished')


main()
