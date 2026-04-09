__all__ = [
    'Element',
    'Container',
    'Label',
    'Window',
]


def __getattr__(name: str):
    _lazy = {
        'Element': 'f_gui.elements.i_0_element',
        'Container': 'f_gui.elements.i_1_container',
        'Label': 'f_gui.elements.i_1_label',
        'Window': 'f_gui.elements.i_2_window',
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
