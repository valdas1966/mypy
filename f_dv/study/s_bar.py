from f_dv.i_1_bar import Bar
from f_color.u_color import UColor, RGB


labels = ['A', 'B', 'C', 'D']
values = [3, 5, 8, 10]
labels = ['A', 'B']
values = [8, 10]
rgbs = UColor.to_gradients(rgb_a=RGB('my_cyan'), rgb_b=RGB('black'), n=10)[:2]


bar = Bar(labels,
          values,
          name_labels='Words',
          name_values='Numbers',
          name="My Bar Chart",
          rgbs=rgbs)
bar.show()
