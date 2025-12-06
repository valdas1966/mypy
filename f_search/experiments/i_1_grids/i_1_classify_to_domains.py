from f_search.experiments.data.i_0_filepaths_maps import FilepathsMaps
from f_search.experiments.data.i_1_domain_filepaths import DomainFilepaths
from f_psl.os.u_path import UPath
from f_core.processes.process import Process


class ClassifyToDomains(Process[FilepathsMaps, DomainFilepaths]):
    """
    ============================================================================
     Classify the filepaths to domains.
    ============================================================================
    """
    
    def __init__(self, input: FilepathsMaps) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================    
        """
        name = 'Classify To Domains'
        Process.__init__(self, input=input, verbose=True, name=name)

    def _run(self) -> None:
        """
        ========================================================================
         Classify the filepaths to domains.
        ========================================================================
        """
        domain_filepaths = DomainFilepaths()
        for filepath in self._input:
            domain = UPath.last_folder(filepath)
            domain_filepaths[domain].append(filepath)
        self._output = domain_filepaths
        