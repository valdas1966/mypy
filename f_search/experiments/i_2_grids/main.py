from f_log.utils import set_debug, one_line
from f_psl.os.u_folder import UFolder


set_debug(True)


@one_line
def get_filepaths_of_maps(path: str) -> list[str]:
    return UFolder.filepaths(path=path, recursive=True)


filepaths = get_filepaths_of_maps(path='f:\\paper\\i_0_maps')
