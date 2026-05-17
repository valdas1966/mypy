from f_core.imports import ULazy

ULazy.install(globals(), {
    'WidgetQuestion': 'f_quiz.exam_gui.widgets.question:WidgetQuestion',
    'WidgetAnswer': 'f_quiz.exam_gui.widgets.answer:WidgetAnswer',
    'WidgetStatus': 'f_quiz.exam_gui.widgets.status:WidgetStatus',
})
