from f_log.utils import set_debug, log_1,  log_2
from f_ds.grids import GridMap as Grid
from f_psl.os.u_folder import UFolder
from f_psl.os.u_path import UPath
from f_utils import u_pickle
from collections import defaultdict


@log_1
def to_filepaths(folder: str) -> list[str]:
    """
    ========================================================================
     Return List of FilePaths in the given Path.
    ========================================================================
    """
    return UFolder.filepaths(path=folder, recursive=True)


@log_1
def to_domain_filepaths(filepaths: list[str]) -> dict[str, list[str]]:
    """
    ========================================================================
     Convert {filepaths} to {domain: filepaths}
    ========================================================================
    """
    domain_filepaths: dict[str, list[str]] = defaultdict(list)
    for filepath in filepaths:
        domain = UPath.last_folder(filepath)
        domain_filepaths[domain].append(filepath)
    return dict(domain_filepaths)


@log_2
def to_domain_grids(domain_filepaths: dict[str, list[str]]) -> dict[str, list[Grid]]:
    """
    ========================================================================
     Convert {domain: filepaths} to {domain: grids}
    ========================================================================
    """
    total = sum(len(filepaths) for filepaths in domain_filepaths.values())
    i = 1
    d: dict[str, list[Grid]] = defaultdict(list)
    for domain, filepaths in domain_filepaths.items():
        for filepath in filepaths:
            grid = filepath_to_grid(domain=domain,
                                    filepath=filepath,
                                    i=i,
                                    total=total)
            d[domain].append(grid)
            i += 1
    return d

@log_1
def filepath_to_grid(domain: str, filepath: str, i: int, total: int) -> Grid:
    """
    ========================================================================
     Convert a filepath to a grid.
    ========================================================================
    """
    name = UPath.filename(path=filepath, with_domain=False)
    return Grid.From.file_map(path=filepath, name=name)

@log_2
def to_pickle(domain_grids: dict[str, list[Grid]], pickle_grids: str) -> None:
    """
    ========================================================================
     Pickle the {domain: grids} to the given path.
    ========================================================================
    """
    u_pickle.dump(obj=domain_grids, path=pickle_grids)


@log_2
def maps_to_grids(folder_maps: str, pickle_grids: str) -> None:
    """
    ========================================================================
     Convert the maps in the given folder to grids and pickle them.
    ========================================================================
    """
    filepaths = to_filepaths(folder=folder_maps)
    domain_filepaths = to_domain_filepaths(filepaths=filepaths)
    domain_grids = to_domain_grids(domain_filepaths=domain_filepaths)
    to_pickle(domain_grids=domain_grids, pickle_grids=pickle_grids)



"""
===============================================================================
 Main Function
-------------------------------------------------------------------------------
 Input: Path to folder of maps and Path where to pickle the grids.
 Output: Pickle the {domain: grids} to the given path.
===============================================================================
"""

set_debug(True)
folder_maps = 'f:\\paper\\i_0_maps'
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'

maps_to_grids(folder_maps=folder_maps,
              pickle_grids=pickle_grids)
