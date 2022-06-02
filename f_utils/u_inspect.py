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


def called_func(back: int = 1):
    stack = inspect.stack()[back]
    return f'{stack.filename}.{stack.function}()'


def trace() -> str:
    ans = str()
    stack = inspect.stack()
    for i in range(len(stack)-1, 0, -1):
        ans += f'{stack[i].filename} -> {stack[i].function}\n'
    return ans


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


def check(var: any,
          name: str,
          obj: any,
          nullable: bool = False) -> None:
    if nullable:
        assert any(type(var) == type(obj), var is None),\
            gen_msg(line=f'type({name}={type(var)} and not {type(obj)}',
                    value=f'{name}={var}', e='DataType Error')
    else:
        assert type(var) == type(obj), \
            gen_msg(line=f'type({name}={type(var)} and not {type(obj)}',
                    value=f'{name}={var}', e='DataType Error')


def emsg(d: dict = dict()) -> str:
    ans = f'\n{"="*50}\n'
    ans += f'{called_func(back=2)}\n{"-"*50}\n'
    for name, val in d.items():
        ans += f'{name} = '
        if len(val.__str__()) <= 100:
            ans += str(val)
        else:
            ans += '?'
        ans += f', {type(val)}\n'
    return ans


"""
def f1():
    x = 5
    try:
        f2()
    except Exception as e:
        msg = emsg({'x': x})
        raise Exception(f'{msg}\n{e.args}')

def f2():
    y = 8
    try:
        1 / 0
    except Exception as e:
        msg = emsg({'y': y})
        raise Exception(f'{msg}\n{e.args}')


try:
    f1()
except Exception as e:
    print(e.args)
"""