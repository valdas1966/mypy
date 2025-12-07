from f_log.utils import logger, set_debug, log_1,  log_2
from f_ds.grids import GridMap as Grid
from f_psl.os.u_folder import UFolder
from f_psl.os.u_path import UPath
from f_utils import u_pickle
from collections import defaultdict


@log_1
def to_filepaths(folder: str) -> list[str]:
    return UFolder.filepaths(path=folder, recursive=True)


@log_1
def to_domain_filepaths(filepaths: list[str]) -> dict[str, list[str]]:
    domain_filepaths: dict[str, list[str]] = defaultdict(list)
    for filepath in filepaths:
        domain = UPath.last_folder(filepath)
        domain_filepaths[domain].append(filepath)
    return dict(domain_filepaths)


@log_1
def to_domain_grids(domain_filepaths: dict[str, list[str]]) -> dict[str, list[Grid]]:
    return {
        domain: [Grid.From.file_map(fp) for fp in filepaths]
        for domain, filepaths in domain_filepaths.items()
    }


@log_1
def to_pickle(domain_grids: dict[str, list[Grid]], pickle_grids: str) -> None:
    u_pickle.dump(obj=domain_grids, path=pickle_grids)


@log_2
def maps_to_grids(folder_maps: str, pickle_grids: str) -> None:
    filepaths = to_filepaths(folder=folder_maps)
    domain_filepaths = to_domain_filepaths(filepaths=filepaths)
    domain_grids = to_domain_grids(domain_filepaths=domain_filepaths)
    to_pickle(domain_grids=domain_grids, pickle_grids=pickle_grids)


set_debug(True)
folder_maps = 'f:\\paper\\i_0_maps'
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'

maps_to_grids(folder_maps=folder_maps, pickle_grids=pickle_grids)
