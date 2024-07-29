from proj.myq.managers.exam.i_0_gui import ManagerExamGui
from proj.myq.exam.u_1_random import UtilsExamRandom as u_exam


exam = u_exam.phrases()
man = ManagerExamGui(exam=exam)
