from f_pptx.c_myp import MyPresentation
from f_canvas.c_canvas import Canvas
from f_const import u_rgb

repo = 'd:\\temp\\pptx\\'
path_in = repo + 'temp.pptx'
path_out = repo + 'temp_out.pptx'

p = MyPresentation(path_in)
slide = Canvas()
# Params A
params_a = p.Params()
coor_a = slide.get_coor((0.3, 0.1, 0.6, 0.5))
params_a.inches = p.to_inches(coor_a)
params_a.name = 'list'
params_a.text = 'A'
params_a.back_color = u_rgb.RED
params_a.transparency = 0.25
p.add_text(params_a)
# Params B
params_b = p.Params()
coor_b = slide.get_coor((0.5, 0.4, 0.3, 0.5))
params_b.inches = p.to_inches(coor_b)
params_b.name = 'b'
params_b.text = 'B'
params_b.back_color = u_rgb.BLUE
p.add_text(params_b)
# General
p.map_shapes_names(['list', 'b'])
p.organize_front(['list', 'b'])
p.save(path_out)