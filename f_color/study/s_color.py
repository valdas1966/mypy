from f_color.u_color import UColor
from f_color.rgb import RGB


def show_custom():
    rgbs = [RGB('green'), RGB(r=0, g=1, b=0), RGB('my_cyan'), RGB('white')]
    UColor.show(rgbs=rgbs)


def show_gradient():
    rgb_a = RGB('my_cyan')
    rgb_b = RGB('black')
    rgbs = UColor.to_gradients(rgb_a, rgb_b, 10)
    UColor.show(rgbs)


def print_colors():
    rgb_a = RGB('my_cyan')
    rgb_b = RGB('black')
    rgbs = UColor.to_gradients(rgb_a, rgb_b, 10)
    for rgb in rgbs:
        print(rgb)


# show_custom()
# show_gradient()
print_colors()
