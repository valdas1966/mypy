from proj.myq.generators.exam import GenExam
from proj.myq.managers.exam.i_0_gui import ManagerExamGui


exam = GenExam.english.phrases(cnt=10)
man = ManagerExamGui(exam=exam)
man.run()
