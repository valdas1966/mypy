from f_search.experiments.i_2_grids.i_0_get_filepaths_of_maps import GetFilepathsOfMaps as P0
from f_search.experiments.i_2_grids.i_1_classify_to_domains import ClassifyToDomains as P1
from f_core.processes.process import Process


class PathMapsToDictDomainGrids(Process[str, None]):

    def __init__(self, input: str) -> None:
        name = 'Path-Maps To Dict-Domain-Grids'
        Process.__init__(self, input=input, verbose=True, name=name)

    def _run(self) -> None:
        """
        ========================================================================
         Run the Process.
        ========================================================================
        """
        # Received Path => FilePaths of all Maps in this Path
        filepaths = P0(input=self._input).run()
        # FilePaths => Dict[domain: FilePaths]
        domain_filepaths = P1(input=filepaths).run()

path = 'f:\\paper\\i_0_maps'
p = PathMapsToDictDomainGrids(input=path)
p.run()