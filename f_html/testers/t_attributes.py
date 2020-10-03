from f_utils import u_tester
from f_html.c_attributes import Attributes


class TestAttributes:

    def __init__(self):
        u_tester.print_start(__file__)
        TestAttributes.__tester_str()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_str():
        # Simple Empty Attribute
        atts = Attributes({'required': None})
        p0 = str(atts) == ' required'
        # Simple Full Attribute
        atts = Attributes({'width': 30})
        p1 = str(atts) == ' width="30"'
        # Composed Empty Attributes
        atts = Attributes({'required': None, 'checked': None})
        p2 = str(atts) == ' required checked'
        # Composed Full Attributes
        atts = Attributes({'width': 30, 'height': 50})
        p3 = str(atts) == ' width="30" height="50"'
        # Composed Full and Empty Attributes
        atts = Attributes({'width': 30, 'required': None})
        p4 = str(atts) == ' width="30" required'
        u_tester.run(p0, p1, p2, p3, p4)


if __name__ == '__main__':
    TestAttributes()
