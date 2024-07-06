from proj.myq.question.i_1_text import QuestionText as Q
from proj.myq.exam.i_0_base import ExamBase as Exam
from proj.myq.managers.exam.i_0_text import ManagerExamText


q_1 = Q('2+2', '4')
q_2 = Q('1+1', '2')
qs = [q_1, q_2]
exam = Exam(qs=qs)

man = ManagerExamText(exam=exam)
man.run()
