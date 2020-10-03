from f_utils import u_tester
from f_html.c_element import Element
from f_html import gen_tag


class TestGenTag:

    def __init__(self):
        u_tester.print_start(__file__)
        TestGenTag.__tester_comment()
        TestGenTag.__tester_doctype()
        TestGenTag.__tester_html()
        TestGenTag.__tester_head()
        TestGenTag.__tester_h()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_comment():
        ele = gen_tag.comment('comment')
        p0 = str(ele) == '<!-- comment -->'
        u_tester.run(p0)

    @staticmethod
    def __tester_doctype():
        ele = gen_tag.doctype()
        p0 = str(ele) == '<!DOCTYPE html>'
        u_tester.run(p0)

    @staticmethod
    def __tester_html():
        ele = gen_tag.html()
        p0 = str(ele) == '<html lang="en">\n</html>'
        u_tester.run(p0)

    @staticmethod
    def __tester_head():
        ele = gen_tag.head()
        p0 = str(ele) == '<head>\n</head>'
        ele = gen_tag.head(title='Title')
        p1 = str(ele) == '<head>\n\t<title>\n\t\tTitle\n\t</title>\n</head>'
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_h():
        ele_h = gen_tag.h(1)
        p0 = str(ele_h) == '<h1>\n</h1>'
        ele_text = Element(content='This is Header')
        ele_h.nest(ele_text)
        p1 = str(ele_h) == '<h1>\n\tThis is Header\n</h1>'
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestGenTag()
