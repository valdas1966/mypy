from f_utils import u_tester
from f_html.c_element import Element


class TestElement:

    def __init__(self):
        u_tester.print_start(__file__)
        TestElement.__tester_str()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_str():
        # Content-Only
        ele = Element(content='P1')
        str_true = 'P1'
        p0 = str(ele) == str_true
        # Empty Tag
        ele = Element(tag='br', is_empty=True)
        str_true = '<br>'
        p1 = str(ele) == str_true
        # Non-Empty but Simple Tag
        ele_html = Element(tag='html')
        str_true = '<html>\n</html>'
        p2 = str(ele_html) == str_true
        # Tag with Attributes
        ele = Element(tag='html', attributes={'lang': 'en'})
        str_true = '<html lang="en">\n</html>'
        p3 = str(ele) == str_true
        # Tag with Content
        ele_p1 = Element(tag='p', content='P1')
        str_true = '<p>\n\tP1\n</p>'
        p4 = str(ele_p1) == str_true
        # Nested Tag
        ele_body = Element(tag='body')
        ele_body.nest(ele_p1)
        str_true = '<body>\n\t<p>\n\t\tP1\n\t</p>\n</body>'
        p5 = str(ele_body) == str_true
        # Multi-Nested Tag
        ele_p2 = Element(tag='p', content='P2')
        ele_body.nest(ele_p2)
        str_true = '<body>\n\t<p>\n\t\tP1\n\t</p>\n\t<p>\n\t\tP2\n\t</p>\n</body>'
        p6 = str(ele_body) == str_true
        # Super-Nested Tag
        ele_html.nest(ele_body)
        str_true = '<html>\n\t<body>\n\t\t<p>\n\t\t\tP1\n\t\t</p>\n\t\t<p>\n\t\t\tP2\n\t\t</p>\n\t</body>\n</html>'
        p7 = str(ele_html) == str_true
        u_tester.run(p0, p1, p2, p3, p4, p5, p6, p7)


if __name__ == '__main__':
    TestElement()