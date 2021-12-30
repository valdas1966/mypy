from f_pptx.c_myp import MyPresentation
from f_canvas.c_canvas import Canvas
from f_const import u_rgb

repo = 'd:\\temp\\pptx\\'
path_in = repo + 'temp.pptx'
path_out = repo + 'temp_out.pptx'

p = MyPresentation(path_in)
slide = Canvas()
params = p.Params()
coor = slide.get_coor((30, 10, 60, 50))
params.inches = p.to_inches(coor)
params.name = 'a'
params.text = 'A'
params.back_color = u_rgb.RED
p.add_text(params)
p.save(path_out)