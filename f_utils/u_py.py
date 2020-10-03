import re


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
