import pickle
import sys
import gc


def load(path):
    """
    =======================================================================
     Description: Load and Return Object from Pickle File.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. path : str (Path to Pickle File).
    =======================================================================
    """
    file = open(path,'rb')
    obj = pickle.load(file)
    file.close()
    return obj


def dump(obj, path):
    """
    =======================================================================
     Description: Dump Object into Pickle File.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. obj : Object to dump.    
        2. path : str (Path to Pickle File).
    =======================================================================
    """
    gc.enable()
    gc.collect()
    sys.setrecursionlimit(10000000)
    file = open(path, 'wb')
    try:
        pickle.dump(obj, file)
    except Exception as e:
        print(str(e))
    finally:
        file.close()
