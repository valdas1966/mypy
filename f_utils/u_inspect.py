import inspect
import re


def called_method():
    """
    ===========================================================================
     Description: Return the name of the Called Method.
    ===========================================================================
     Return: str (Name of the Called Method).
    ===========================================================================
    """
    return inspect.stack()[2].function


def called_func(back: int = 1):
    stack = inspect.stack()[back]
    return f'{stack.filename}.{stack.function}()'


def trace() -> str:
    ans = str()
    stack = inspect.stack()
    for i in range(len(stack)-1, 0, -1):
        ans += f'{stack[i].filename} -> {stack[i].function}\n'
    return ans


def get_desc(func) -> str:
    """
    ============================================================================
     Description: Return Description-Text of the given Function.
    ============================================================================
    """
    try:
        source = inspect.getsource(func)
        source = source.replace('\n', ' ')
        s = ' '.join(source.split())
        p = '= Description: (.*) ='
        match = re.search(pattern=p, string=s)
        ret = match.group(1).upper()
        if '=' in ret:
            ret = ret[:ret.find('=')]
        return ret
    except Exception as e:
        return str(e)

