from f_log.utils import set_debug, log_1
from f_psl.os.u_folder import UFolder


set_debug(True)


class MapsToGrids:
    """
    ============================================================================
    Convert Maps (from a given path) to Grids.
    ============================================================================
    """
    
    def __init__(self, path: str) -> None:
        """
        ========================================================================
         Initialize the MapsToGrids object.
        ========================================================================
        """
        filepaths = self.get_filepaths_of_maps(path=path)


    @log_1
    def get_filepaths_of_maps(self, path: str) -> list[str]:
        """
        ========================================================================
        Return List of FilePaths of Maps in the given Path.
        ========================================================================
        """
        return UFolder.filepaths(path=path, recursive=True)


path = 'f:\\paper\\i_0_maps'
MapsToGrids(path=path)
