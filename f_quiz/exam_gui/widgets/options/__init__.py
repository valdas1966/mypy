from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_quiz.exam_gui.widgets.options.main import WidgetOptions

ULazy.install(globals(), {'WidgetOptions': 'f_quiz.exam_gui.widgets.options.main:WidgetOptions'})
