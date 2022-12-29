from f_utils import u_py

class A:
    _a = 1
    def _fa(self):
        pass

class B(A):
    _b = 2

    def _get(self):
        atts = [att for att in dir(self) if u_py.is_protected(att)]
        d = {att: getattr(self, att) for att in atts}
        d = {att: val for att, val in d.items() if not callable(val)}
        print(d)

    def _fb(self):
        pass

b = B()
b._get()
