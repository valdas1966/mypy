from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from collections import namedtuple
from f_utils import u_file
from f_const import u_rgb


class MyPresentation:

    # width of standard pptx slide
    WIDTH = 13.33
    # height of standard pptx slide
    HEIGHT = 7.5
    # pptx.Presentation object
    p = None
    # pptx.Presentation.slide object
    slide = None
    # map user-given name with shape
    shapes = dict()

    def __init__(self, path):
        self.path = path
        self.__init_slide()

    def map(self, li):
        assert type(li) in {tuple, list, set}
        assert len(li) == len(self.slide.shapes)
        for i, name in enumerate(li):
            self.shapes[name] = self.slide.shapes[i]

    def update(self, name, parent, ratios):
        left, top, width, height = parent.get_coor(ratios)
        self.shape[name].left = Inches(self.WIDTH / 100 * left)
        self.shape[name].top = Inches(self.HEIGHT / 100 * top)
        self.shape[name].width = Inches(self.WIDTH / 100 * width)
        self.shape[name].height = Inches(self.HEIGHT / 100 * height)

    def gen_params_shape(self):
        fields = 'name inches text text_font text_size text_is_bold'
        fields += ' text_color line_width line_color back_color'
        defaults = (None, None, str(), 'Tahoma', 18, True, u_rgb.BLACK,
                    0.01, u_rgb.BLACK, u_rgb.WHITE)
        return namedtuple('Params', fields, defaults=defaults)

    def add_text(self, params):
        left, top, width, height = params.inches
        textbox = self.slide.shapes.add_textbox(left, top, width, height)
        textbox.line.color.rgb = self.to_rgb_color(params.line_color)
        textbox.line.width = params.line_width
        textbox.fill.solid()
        textbox.fill.fore_color.rgb = self.to_rgb_color(params.back_color)
        self.shapes[params.name] = self.slide.shapes[-1]
        tf = textbox.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        parag = tf.paragraphs[0]
        parag.alignment = PP_ALIGN.CENTER
        run = parag.add_run()
        run.text = params.text
        font = run.font
        font.name = params.font
        font.size = Pt(params.text_size)
        font.color.rgb = self.to_rgb_color(params.text_color)
        font.bold = params.text_is_bold

    def save(self, path=None):
        if not path:
            path = self.path
        self.p.save(path)

    @classmethod
    def to_inches(cls, coor):
        left = Inches(cls.WIDTH / 100 * coor[0])
        top = Inches(cls.HEIGHT / 100 * coor[1])
        width = Inches(cls.WIDTH / 100 * coor[2])
        height = Inches(cls.HEIGHT / 100 * coor[3])
        return left, top, width, height

    @classmethod
    def to_rgb_color(cls, rgb):
        red, green, blue = rgb
        return RGBColor(red, green, blue)

    def __init_slide(self):
        if u_file.is_exists(self.path):
            self.p = Presentation(self.path)
            self.slide = self.p.slides[0]
        else:
            self.p = Presentation()
            layout_blank = 6
            layout = self.p.slide_layouts[layout_blank]
            self.slide = self.p.slides.add_slide(layout)

    class Params:
        name = None
        inches = None
        text = str()
        font = 'Tahoma'
        text_color = u_rgb.BLACK
        text_size = 18
        text_is_bold = True
        line_width = Inches(0.01)
        line_color = u_rgb.BLACK
        back_color = u_rgb.WHITE

