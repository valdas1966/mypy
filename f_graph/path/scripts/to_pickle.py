from f_graph.path.generators.g_graph_map import GenGraphMap
from f_utils import u_pickle


def graphs_maps(path_maps: str,
                path_pickle: str,
                verbose: bool = False) -> None:
    """
    ========================================================================
     Convert List[GraphMap] to pickle.
    ========================================================================
    """
    graphs = GenGraphMap.maps_in_folder(path=path_maps, verbose=verbose)
    u_pickle.dump(obj=graphs, path=path_pickle)


graphs_maps(path_maps='d:\\temp\\boundary\\maps',
            path_pickle='d:\\temp\\boundary\\maps.pkl',
            verbose=True)
