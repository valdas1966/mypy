from f_core.processes.process import Process
from f_search.experiments.data.i_0_filepaths_maps import FilepathsMaps
from f_psl.os.u_folder import UFolder


class GetFilepathsOfMaps(Process[str, FilepathsMaps]):
    """
    ============================================================================
     Get the filepaths of the maps.
    ============================================================================
    """
    
    def __init__(self, input: str, name: str = 'Get Filepaths Of Maps') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Process.__init__(self, input=input, name=name, verbose=True)

    def _run(self) -> None:
        """
        ========================================================================
         Return the filepaths of the maps.
        ========================================================================
        """
        filepaths = UFolder.filepaths(path=self._input, recursive=True)
        self._output = FilepathsMaps(filepaths=filepaths)
