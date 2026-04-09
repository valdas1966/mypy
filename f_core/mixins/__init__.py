__all__ = [
    'Sizable',
    'Dictable',
    'Equatable',
    'Comparable',
    'Validatable',
    'ValidatableMutable',
    'HasKey',
    'HasName',
    'HasRowCol',
    'HasRowsCols',
]


def __getattr__(name: str):
    _lazy = {
        'Sizable': 'f_core.mixins.sizable',
        'Dictable': 'f_core.mixins.dictable',
        'Equatable': 'f_core.mixins.equatable',
        'Comparable': 'f_core.mixins.comparable',
        'Validatable': 'f_core.mixins.validatable',
        'ValidatableMutable': 'f_core.mixins.validatable_mutable',
        'HasKey': 'f_core.mixins.has',
        'HasName': 'f_core.mixins.has',
        'HasRowCol': 'f_core.mixins.has',
        'HasRowsCols': 'f_core.mixins.has',
    }
    if name in _lazy:
        from importlib import import_module
        mod = import_module(_lazy[name])
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
