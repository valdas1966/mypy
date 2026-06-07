from typing import TYPE_CHECKING

from f_core.imports import ULazy

# Static-analysis only. TYPE_CHECKING is False at runtime, so these imports
# never execute — lazy loading via ULazy below is fully preserved. They exist
# so `from f_gui.elements import Window` resolves in IDEs / mypy / pyright
# (with real autocomplete + go-to-definition) instead of "unresolved reference".
if TYPE_CHECKING:
    from f_gui.elements.i_0_element import Element
    from f_gui.elements.i_1_container import Container
    from f_gui.elements.i_1_label import Label
    from f_gui.elements.i_1_line import Line
    from f_gui.elements.i_2_window import Window

ULazy.install(globals(), {
    'Element': 'f_gui.elements.i_0_element:Element',
    'Container': 'f_gui.elements.i_1_container:Container',
    'Label': 'f_gui.elements.i_1_label:Label',
    'Line': 'f_gui.elements.i_1_line:Line',
    'Window': 'f_gui.elements.i_2_window:Window',
})
