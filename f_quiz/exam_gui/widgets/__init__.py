from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_quiz.exam_gui.widgets.question import WidgetQuestion
    from f_quiz.exam_gui.widgets.answer import WidgetAnswer
    from f_quiz.exam_gui.widgets.status import WidgetStatus

ULazy.install(globals(), {
    'WidgetQuestion': 'f_quiz.exam_gui.widgets.question:WidgetQuestion',
    'WidgetAnswer': 'f_quiz.exam_gui.widgets.answer:WidgetAnswer',
    'WidgetStatus': 'f_quiz.exam_gui.widgets.status:WidgetStatus',
})
