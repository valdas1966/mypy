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


def gen_msg(line: str,
            value: str,
            e: str) -> str:
    assert type(line) == str, type(line)
    assert type(value) == str, type(value)
    assert type(e) == str, type(e)
    msg = 'Exception Caught!\n'
    msg += f'{trace()}\n'
    msg += f'Line: {line}\n'
    msg += f'Value: {value}\n'
    msg += f'Exception: {e}'
    return msg


def trace() -> str:
    ans = str()
    stack = inspect.stack()
    for i in range(len(stack)-1, 0, -1):
        ans += f'{stack[i].filename} -> {stack[i].function}\n'
    return ans

def a():
    print(len(inspect.stack()))
    print(inspect.stack()[2].function)
    print(inspect.stack()[1].function)
    print(inspect.stack()[0].function)
    print(inspect.stack()[0].filename + ' ' + inspect.stack()[0].function)

def b():
    a()
