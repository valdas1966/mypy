import inspect

def called_method():
    """
    ===========================================================================
     Description: Return the name of the Called Method.
    ===========================================================================
     Return: str (Name of the Called Method).
    ===========================================================================
    """
    return inspect.stack()[2].function


