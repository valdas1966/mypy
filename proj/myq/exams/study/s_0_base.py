from proj.myq.exams.i_0_base import ExamBase
from proj.myq.gsheets.english.i_1_phrases import SheetPhrases


questions = SheetPhrases().to_questions()
exam = ExamBase(qs=questions)
print(len(exam))
print(exam[0])