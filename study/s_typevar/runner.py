from study.s_typevar.main import Main
from study.s_typevar.created_base import CreatedBase
from study.s_typevar.created_a import CreatedA
from study.s_typevar.created_b import CreatedB


created_a = CreatedA()
main_a = Main[CreatedA](created=created_a)
main_a.created.f_a()

created_b = CreatedB()
main_b = Main(created=created_b)
created_b.f_b() # Valid