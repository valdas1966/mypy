from f_pptx.c_myp import MyPresentation
from f_canvas.c_canvas import Canvas
from f_const import u_rgb

repo = 'd:\\temp\\pptx\\'
path_in = repo + 'temp.pptx'
path_out = repo + 'temp_out.pptx'

p = MyPresentation(path_in)
slide = Canvas()
coor = slide.get_coor((30, 10, 60, 20))
inches = p.to_inches(coor)
p.add_text('title', 'Title', font_size=24, font_rgb=u_rgb.BLACK, inches=inches)
p.save(path_out)