__all__ = [
    'Auth',
    'OAuth',
    'BigQuery',
    'Drive',
    'Gemini',
    'Spread',
]


def __getattr__(name: str):
    _lazy = {
        'Auth': 'f_google.creds.auth',
        'OAuth': 'f_google.creds.oauth',
        'BigQuery': 'f_google.services.bigquery',
        'Drive': 'f_google.services.drive',
        'Gemini': 'f_google.services.gemini',
        'Spread': 'f_google.services.sheets',
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
