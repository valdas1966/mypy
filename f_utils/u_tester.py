from f_utils import u_bool
from f_utils import u_inspect


def run(*predicates):
    """
    ===========================================================================
     Description: Run tester function and print OK or FAILED.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. predicates : list of bool (List of Tester Predicates).
    ===========================================================================
    """
    line = ': {0}'
    first_false = u_bool.first_false(predicates)
    if first_false is None:
        line = 'OK' + line
    else:
        line = 'Failed' + line + ' [' + str(first_false) + ']'
        
    called_method = u_inspect.called_method()
    called_method = called_method.replace('__','')
    len_tester = 7
    fname = called_method[len_tester:]
    print(line.format(fname))
    
    
def print_start(path_module):
    """
    ===========================================================================
     Description: Print Start Tester with the name of the tested Module.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_module : str (Path of the tested Module).
    ===========================================================================
    """
    name = path_module.split('\\')[-1].split('.')[0]
    print('\n{0}\nStart Tester: {1}\n{0}'.format('='*50, name))


def print_finish(path_module):
    """
    ===========================================================================
     Description: Print Finish Tester with the name of the tested Module.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. path_module : str (Path of the tested Module).
    ===========================================================================
    """
    name = path_module.split('\\')[-1].split('.')[0]
    print('{0}\nFinish Tester: {1}\n{0}'.format('='*50, name))
