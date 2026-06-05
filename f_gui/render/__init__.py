from typing import TYPE_CHECKING

from f_core.imports import ULazy

# Static-analysis only (see f_gui/elements/__init__.py for the rationale):
# false at runtime so ULazy stays lazy, true for IDEs so the name resolves.
if TYPE_CHECKING:
    from f_gui.render.html import RenderHtml

ULazy.install(globals(), {'RenderHtml': 'f_gui.render.html:RenderHtml'})
