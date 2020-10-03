from f_utils import u_file
from f_utils import u_dir


def encode_py(path_py, path_csv):
    """
    =======================================================================
     Description: Encode Python-File into Csv-File with Hex-Encoding.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path_py : str (Path to Python-File to Encode).
        2. path_csv : str (Path to encoded Csv-File).
    =======================================================================
    """
    text_py = u_file.read(path_py)
    text_hex = bytearray(text_py.encode('utf-8')).hex()
    csv_hex = str()
    for i, ch in enumerate(text_hex):
        csv_hex += ch
        if not i:
            continue
        if not (i+1) % 10:
            csv_hex += ','
        if not (i+1) % 100:
            csv_hex += '\n'
    u_file.write(csv_hex, path_csv)


def decode_py(path_csv, path_py):
    """
    =======================================================================
     Description: Decode Text-File with Hex-Encoding into Python-File.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path_txt : str (Path to encoded Text-File).
        2. path_py : str (Path to Python-File to Decode).
    =======================================================================
    """
    csv_hex = u_file.read(path_csv)
    text_hex = csv_hex.replace(',', '').replace('\n', '')
    text_py = bytearray.fromhex(text_hex).decode('utf-8')
    u_file.write(text_py, path_py)


def encode_mypy(path_src, path_dst):
    """
    =======================================================================
     Description: Encode MyPy Directory.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path_src : str (Path to MyPy Directory).
        2. path_dst : str (Path where to store the encoded Directory.
    =======================================================================
    """
    u_dir.copy(path_src, path_dst)
    paths_py = set(u_file.filepaths(path_dst, extensions='py'))
    paths_all = set(u_file.filepaths(path_dst))
    paths_delete = paths_all - paths_py
    u_file.delete(paths_delete)
    for path_py in paths_py:
        path_csv = path_py[:-2] + 'csv'
        encode_py(path_py, path_csv)
        u_file.delete(path_py)


def decode_mypy(path_src, path_dst):
    u_dir.copy(path_src, path_dst)
    for path_csv in u_file.get_paths_by_extension(path_dst, 'csv'):
        path_py = path_csv[:-3] + 'py'
        decode_py(path_csv, path_py)
        u_file.delete(path_csv)
