import re
from f_utils import u_file
from f_utils import u_hex


def get_funcs(path):
    """
    ============================================================================
     Description: Return Function Names from Python File.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Path to Python File).
    ============================================================================
     Return: list of str (List of Function Names)
    ============================================================================
    """
    funcs = list()
    file = open(path, 'r')
    for line in file:
        founded = re.findall('\ndef \w*\(', line)
        if len(founded) == 1:
            func = founded[0].strip()
            func = func.replace('def ', '')
            func = func.replace('(', '')
            funcs.append(func)
    file.close()
    return funcs


def change_import(path_dir, old, new, verbose=True):
    """
    ============================================================================
     Description: Change Imports (Modules) in all Python-Files in the Folder.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path_dir : str (Path to Folder with Python-Files).
        2. old : str (Old Module).
        3. new : str (New Module).
        4. verbose : bool (To Print the FilePaths after Update).
    ============================================================================
    """
    filepaths = u_file.filepaths(path_dir, extensions='py')
    for filepath in filepaths:
        u_file.replace_in_file(filepath, [(old, new)])
        if verbose:
            print(filepath)


from f_utils import u_dir


def temp_1():
    li_py = u_file.filepaths(dir_hex, 'py')
    for path_py in li_py:
        path_hex = path_py.replace('.py', '.txt')
        u_hex.file_to_hex(path_py, path_hex)
        u_file.delete(path_py)
        print(path_py, path_hex)


dir_mypy = 'd:\\mypy'
dir_hex = 'd:\\hex\\'
u_dir.copy(dir_mypy, dir_hex)
temp_1()