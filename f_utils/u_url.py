import urllib.request
from f_utils import u_file


def get(url: str, path_dest: str) -> None:
    """
    ============================================================================
     Description: Get Request into FileName. Throw Exception on invalid url or
                    path_dest.
    ============================================================================
    """
    urllib.request.urlretrieve(url, path_dest)
    if not u_file.is_exists(path_dest):
        raise Exception(f'{url} was not downloaded to {path_dest}')
