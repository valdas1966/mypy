from proj.myq.managers.exam.i_0_gui import ManagerExamGui
from proj.myq.exam.u_0_base import UtilsExamBase as u_exam_base
from proj.myq.exam.u_1_random import UtilsExamRandom as u_exam_random


exam = u_exam_random.english(cnt=15)
# exam = u_exam_base.stam()
man = ManagerExamGui(exam=exam)
