from typing import TYPE_CHECKING

from f_core.imports import ULazy

# Static-analysis only. TYPE_CHECKING is False at runtime, so these imports
# never execute — lazy loading via ULazy below is fully preserved. They exist
# so `from f_gui.style import Stroke` resolves in IDEs / mypy / pyright.
if TYPE_CHECKING:
    from f_gui.style.stroke import LineStyle, Stroke
    from f_gui.style.border import Border

ULazy.install(globals(), {
    'LineStyle': 'f_gui.style.stroke:LineStyle',
    'Stroke': 'f_gui.style.stroke:Stroke',
    'Border': 'f_gui.style.border:Border',
})
