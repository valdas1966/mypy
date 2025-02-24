from f_graph.path.graph_map import GraphMap
from f_file.generators.g_map_grid import GenMapGrid
from f_utils.psl.os.folder import Folder
from f_utils import u_datetime, u_pickle


class GenGraphMap:
    """
    ============================================================================
     Generate GraphMap.
    ============================================================================
    """

    @staticmethod
    def test() -> GraphMap:
        """
        ========================================================================
         Generate a test GraphMap.
        ========================================================================
        """
        path = 'd:\\temp\\map_grid.txt'
        GenMapGrid.map_grid(path=path)
        return GraphMap(path=path)
    
    @staticmethod
    def maps_in_folder(path: str, verbose: bool = False) -> list[GraphMap]:
        """
        ========================================================================
         Generate a map grid GraphMap.
        ========================================================================
        """
        folder = Folder(path=path)
        filepaths = folder.filepaths(recursive=True)
        maps = list()
        for i, filepath in enumerate(filepaths):
            graph = GraphMap(path=filepath)
            if verbose:
                print(u_datetime.now(),
                      f'[{i+1}/{len(filepaths)}]',
                      graph.domain,
                      graph.name,
                      len(graph.nodes()))
            maps.append(graph)
        return maps

    @staticmethod
    def from_pickle(path: str) -> list[GraphMap]:
        """
        ========================================================================
         Generate a list of GraphMap objects from a pickle file.
        ========================================================================
        """
        return u_pickle.load(path=path)
