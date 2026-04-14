from f_google.services.sheets import Spread
from f_quiz.question.main import Question
from f_quiz.question_options.main import QuestionOptions
from f_quiz.question_visual.main import QuestionVisual
from f_quiz.question_yes_no.main import QuestionYesNo


def load(sheet_name: str = 'Hebrew') -> list[Question]:
    """
    ========================================================================
     Load Questions from the Google Sheet.
     First row is used as column headers.
    ========================================================================
    """
    spread = Spread.Factory.questions()
    sheet = spread[sheet_name]
    last = sheet.last_row()
    if last <= 1:
        return []
    return [Question(text=row[0], answer=row[1])
            for row in [sheet[i] for i in range(1, last)]]


def load_options(sheet_name: str = 'Options') -> list[QuestionOptions]:
    """
    ========================================================================
     Load QuestionOptions from the Google Sheet.
     Columns: Question, Correct, Wrong.
    ========================================================================
    """
    spread = Spread.Factory.questions()
    sheet = spread[sheet_name]
    last = sheet.last_row()
    if last <= 1:
        return []
    return [QuestionOptions(text=row[1], answer=row[2], wrong=row[3])
            for row in [sheet[i] for i in range(1, last)]]


def load_yes_no(sheet_name: str = 'YesNo') -> list[QuestionYesNo]:
    """
    ========================================================================
     Load QuestionYesNo from the Google Sheet.
     Columns: Question, Answer (Yes/No).
    ========================================================================
    """
    spread = Spread.Factory.questions()
    sheet = spread[sheet_name]
    last = sheet.last_row()
    if last <= 1:
        return []
    return [QuestionYesNo(text=row[0], answer=row[1])
            for row in [sheet[i] for i in range(1, last)]]


def load_visual(sheet_name: str = 'Visual') -> list[QuestionVisual]:
    """
    ========================================================================
     Load QuestionVisual from the Google Sheet.
     Columns: Id, Topic, SvgPath, MaskedLabel, Correct, Wrong.
    ========================================================================
    """
    spread = Spread.Factory.questions()
    sheet = spread[sheet_name]
    last = sheet.last_row()
    if last <= 1:
        return []
    return [QuestionVisual(topic=row[1],
                           svg_path=row[2],
                           masked_label=row[3],
                           answer=row[4],
                           wrong=row[5])
            for row in [sheet[i] for i in range(1, last)]]
