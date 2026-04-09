__all__ = ['NodeKey', 'Key', 'NodeParent']


def __getattr__(name: str):
    _lazy = {
        'NodeKey': 'f_graph.nodes.i_0_key',
        'Key': 'f_graph.nodes.i_0_key',
        'NodeParent': 'f_graph.nodes.i_1_parent',
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
