from proj.myq.generators.exam import GenExam
from proj.myq.managers.exam.i_0_gui import ManagerExamGui


gen = GenExam()
exam = gen.english.combine(cnt_phrases=10, cnt_definitions=10)
man = ManagerExamGui(exam=exam)
