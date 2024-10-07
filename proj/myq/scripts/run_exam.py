from proj.myq.generators.exam import GenExam
from proj.myq.managers.exam.i_0_gui import ManagerExamGui


def run_english():
    gen = GenExam()
    exam = gen.english.combine(cnt_phrases=10, cnt_definitions=10)
    ManagerExamGui(exam=exam)


def run_cs():
    gen = GenExam()
    exam = gen.cs.base()
    ManagerExamGui(exam=exam)


run_cs()
