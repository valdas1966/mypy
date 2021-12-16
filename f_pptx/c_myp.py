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
    # namedtuple of shape parameters
    params_shape = None

    def __init__(self, path):
        self.path = path
        self.__init_slide()
        self.__init_params_shape()

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

    def add_text(self, name, text, inches, font_size, font_rgb):
        left, top, width, height = inches
        textbox = self.slide.shapes.add_textbox(left, top, width, height)
        textbox.line.color.rgb = self.to_rgb_color(u_rgb.BLACK)
        textbox.line.width = Inches(0.0416)
        textbox.fill.solid()
        textbox.fill.fore_color.rgb = self.to_rgb_color(u_rgb.GREEN)
        self.shapes[name] = self.slide.shapes[-1]
        tf = textbox.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        parag = tf.paragraphs[0]
        parag.alignment = PP_ALIGN.CENTER
        run = parag.add_run()
        run.text = text
        font = run.font
        font.name = 'Tahoma'
        font.size = Pt(font_size)
        font.color.rgb = self.to_rgb_color(font_rgb)
        font.bold = True

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

    def __init_params_shape(self):
        fields = ('name', 'text', 'font_name', 'font_size', 'font_bold',
                  'forecolor', 'background', 'line_color', 'line_width',
                  'inches')
        defaults = (None, str(), 'Tahoma', '18', True, u_rgb.BLACK,
                    u_rgb.WHITE, u_rgb.BLACK, 0.01, None)
        self.params_shape = namedtuple('Params Shape', fields, defaults)


p = MyPresentation('d:\\test.pptx')