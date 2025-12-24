from f_log.utils import set_debug, log_1,  log_2
from f_ds.grids import GridMap as Grid
from f_psl.os.u_folder import UFolder
from f_psl.os.u_path import UPath
from f_utils import u_pickle


@log_1
def folder_to_filepaths(folder: str) -> list[str]:
    """
    ========================================================================
     Return List of FilePaths in the given Path.
    ========================================================================
    """
    return UFolder.filepaths(path=folder, recursive=True)

@log_2
def filepaths_to_grids(filepaths: list[str]) -> dict[str, Grid]:
    """
    ========================================================================
     Convert List[FilePath] to List[Grid].
    ========================================================================
    """
    @log_1
    def filepath_to_grid(domain: str,
                         filepath: str,
                         i: int,
                         total: int) -> Grid:
        """
        ========================================================================
        Convert a filepath to a grid.
        ========================================================================
        """
        name = UPath.filename(path=filepath, with_domain=False)
        return Grid.From.file_map(path=filepath, name=name, domain=domain)

    total = len(filepaths)
    grids: dict[str, Grid] = dict()
    for i, filepath in enumerate(filepaths, start=1):
        domain = UPath.last_folder(filepath)
        grid = filepath_to_grid(domain=domain,
                                filepath=filepath,
                                i=i,
                                total=total)
        grids[grid.name] = grid
    return grids

@log_2
def grids_to_pickle(grids: dict[str, Grid], pickle_grids: str) -> None:
    """
    ========================================================================
     Pickle the List[Grid] to the given path.
    ========================================================================
    """
    u_pickle.dump(obj=grids, path=pickle_grids)


"""
===============================================================================
 Main - Convert the maps in the given folder to grids and pickle them.
-------------------------------------------------------------------------------
 Input: Path to folder of maps and Path where to pickle the grids.
 Output: Pickle the dict[Grid.Name, Grid] to the given path.
===============================================================================
"""

set_debug(True)
folder_maps = 'f:\\paper\\i_0_maps'
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'

@log_2
def main(folder_maps: str, pickle_grids: str) -> None:
    """
    ========================================================================
     Convert the maps in the given folder to grids and pickle them.
    ========================================================================
    """
    filepaths = folder_to_filepaths(folder=folder_maps)
    grids = filepaths_to_grids(filepaths=filepaths)
    grids_to_pickle(grids=grids, pickle_grids=pickle_grids)


main(folder_maps=folder_maps,
     pickle_grids=pickle_grids)
