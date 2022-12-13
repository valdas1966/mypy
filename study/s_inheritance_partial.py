class Init_1:
    def f_1(self):
        print(1)


class Init_2(Init_1):
    def f_2(self):
        print(2)


class Globs_1(Init_1):
    def f_3(self):
        print(3)

class Globs_2(Init_2, Globs_1):
    pass


g = Globs_2()
g.f_1()
g.f_2()
g.f_3()
