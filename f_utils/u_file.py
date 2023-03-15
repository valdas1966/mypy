import os
import sys
import shutil
import fileinput
import datetime
from f_utils import u_str
from f_utils import u_set


def is_exists(path):
    """
    ============================================================================
     Description: Return True if the file is exist.
    ============================================================================
     Arguemtns:
    ----------------------------------------------------------------------------
        1. path : str (Path to the File).
    ============================================================================
    """
    if path:
        return os.path.isfile(path)
    return False


def read(path: str) -> str:
    """
    =======================================================================
     Description: Return the file as string.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path : str (Path to File for reading).
    =======================================================================
     Return: str (String-Representation of the File).
    =======================================================================
    """
    file = open(path, 'r')
    text = file.read()
    file.close()
    return text


def write(path, text):
    """
    =======================================================================
     Description: Write text into File.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path : str (Path to File to Write).
        2. text : str (Text to Write).
    =======================================================================
    """
    file = open(path, 'w')
    file.write(text)
    file.close()


def write_lines(path, lines):
    """
    ============================================================================
     Description: Write Lines into Txt-File.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str
        2. lines : list of str
    ============================================================================
    """
    file = open(path, 'w')
    file.write('\n'.join(lines))
    file.close()


def append(path, text):
    """
        =======================================================================
         Description: Write text into File.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. path : str (Path to File to Append).
            2. text : str (Text to Append).
        ========================================================================
        """
    file = open(path, 'a')
    file.write(text)
    file.close()


def delete(paths: 'str | sequence') -> 'list[str]':
    """
    ============================================================================
     Description: Delete a File (by FilePath).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. paths : str or set of str.
    ============================================================================
     Return: List of Error-Messages (if any).
    ============================================================================
    """
    if type(paths) in {list, tuple}:
        paths = set(paths)
    paths = u_set.generalize(paths)
    errors = list()
    for path in paths:
        try:
            os.remove(path)
        except Exception as e:
            errors.append(str(e))
    return errors


def to_lines(path: str) -> 'list[str]':
    """"
    ============================================================================
     Description: Transpose Lines from a given Text-File into a List of str.
    ============================================================================
    """
    text = read(path)
    return text.split('\n')


def filepaths(path_dir, extensions=set()):
    """
    =======================================================================
     Description: Return Full-FilePaths of Files in the Directory with
                    the specified extensions (ex: 'txt').
                  If extensions is empty -> Return all FilePaths.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path_dir : str (Path to Directory to Inspect).
        2. extensions : str or set (str if one extensions, set if many).
                        The extensions should be like: 'txt', 'py' and etc.
    =======================================================================
     Return: list of str (List of Full-FilePaths).
    =======================================================================
    """
    extensions = u_set.generalize(extensions)
    extensions = {'.' + e for e in extensions}
    li = list()
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            if u_str.endswith(file, extensions):
                filepath = os.path.join(root, file)
                li.append(filepath)
    return li


def get_files_names(path):
    """
    ===========================================================================
     Description: Return List of Files Names in the Path.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (Path where to search).
    ===========================================================================
     Return: list of str (List of Files Names).
    ===========================================================================
    """
    names = list()
    for name in os.listdir(path):
        full_path = path + '\\' + name
        if os.path.isfile(full_path):
            names.append(name)
    return names


def copy(path_src, path_dest):
    """
    ===========================================================================
     Description: Copy file from src to dest.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_src : str (Path to Source File).
        2. path_dest : str (Path where to move the file).
    ===========================================================================
    """
    shutil.copyfile(path_src, path_dest)
    
    
def copy_files(path_src, path_dest):
    """
    ===========================================================================
     Description: Copy all Files from Source Dir to Destination Dir.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_src : str (Path to Source Directory).
        2. path_dest : str (Path to Destination Directory).
    ===========================================================================
    """
    names = get_files_names(path_src)
    for name in names:
        path_src = u_str.get_path(path_src,name)
        path_dest = u_str.get_path(path_dest,name)
        copy(path_src, path_dest)
    
    
def replace_in_file(path, tuples):
    """
    ===========================================================================
     Description: Replace string in File.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path  : str (Path of File to change).
        2. tuples : list of tuples (Every Tuple contains what_replace and
                        with_replace, e.g ('a','o')).
    ===========================================================================
    """
    for t in tuples:
        what_replace = t[0]
        with_replace = t[1]
        for line in fileinput.input(path, inplace=1):                    
            sys.stdout.write(line.replace(what_replace, with_replace))
            

def replace_lines(path: str, d: dict[str: str]) -> None:
    """
    ============================================================================
     Description: Replace Lines in the File by a given Dictionary.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Path to the File)
        2. d : dict {what -> into}
    ============================================================================
    """
    lines_old = to_lines(path)
    lines_new = list()
    for line in lines_old:
        if line in d:
            lines_new.append(d[line])
        else:
            lines_new.append(line)
    write_lines(path, lines_new)


def get_filename(path, with_domain=True):
    """
    ===========================================================================
     Description: Extract FileName from the Path (with or without domain).
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path : str (FullPath of the FileName).
        2. with_domain : bool (Domain is for example .txt or .py).
    ===========================================================================
     Return: str (FileName extracted from the FullPath).
    ===========================================================================
    """  
    vals = path.split('\\')
    filename = vals[-1]
    if not with_domain:
        vals = filename.split('.')
        filename = '.'.join(vals[:-1])
    return filename


def cosine_similarity(path_1, path_2):
    """
    ===========================================================================
     Description: Return Cosine Similarity between two text files.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_1 : str (Path to the first File).
        2. path_2 : str (Path to the second File).
    ===========================================================================
     Return: float (Cosine Similarity between the two files).
    ===========================================================================
    """
    # str_1 = to_str(path_1)
    # str_2 = to_str(path_2)
    # return u_text_mining.cosine_similarity(str_1, str_2)
    pass


def datetime_created(filepath):
    """
    ============================================================================
     Description: Return DateTime when the File was Created.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. filepath : str (Path to the File).
    ============================================================================
     Return: DateTime.
    ============================================================================
    """
    t = os.path.getctime(filepath)
    return datetime.datetime.fromtimestamp(t)


def replace_filename(path, filename):
    """
    ============================================================================
     Description: Get full filepath and return it with replaced filename.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Full FilePath).
        2. filename : str (FileName to Replace).
    ============================================================================
     Return: str (FilePath with replaced FileName).
    ============================================================================
    """
    return '\\'.join(path.split('\\')[:-1]) + '\\' + filename

