from f_utils import u_py


def get_protected_atts(self):
    atts = [att for att in dir(self) if u_py.is_protected(att)]
    d = {att: getattr(self, att) for att in atts}
    d = {att: val for att, val in d.items() if not callable(val)}
    return d
