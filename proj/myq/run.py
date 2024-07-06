from proj.myq.generators.exam import GenExam
from proj.myq.managers.exam.i_0_text import ManagerExamText


exam = GenExam.english.phrases(cnt=10)
man = ManagerExamText(exam=exam)
man.run()
