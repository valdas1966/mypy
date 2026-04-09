__all__ = ['WidgetQuestion', 'WidgetAnswer', 'WidgetStatus']


def __getattr__(name: str):
    _lazy = {
        'WidgetQuestion': 'f_quiz.exam_gui.widgets.question',
        'WidgetAnswer': 'f_quiz.exam_gui.widgets.answer',
        'WidgetStatus': 'f_quiz.exam_gui.widgets.status',
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
