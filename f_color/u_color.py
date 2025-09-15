import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from f_math.u_interpolation import UInterpolation
from f_color.rgb import RGB


class UColor:

    @staticmethod
    def show(rgbs: list[RGB]) -> None:
        """
        ========================================================================
         Display list of RGB colors as rectangles with their STR-REPR.
        ========================================================================
        """
        rect_width: float = 9.0
        min_rect_height: float = 0.5
        num_colors = len(rgbs)
        rect_height = max(min_rect_height,
                          10.0 / num_colors)  # Calculate height dynamically

        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        for i, rgb in enumerate(rgbs):
            color_tuple = rgb.to_tuple()
            y_position = -i * rect_height  # Calculate the y position of the rectangle
            rect = Rectangle((0, y_position), rect_width, rect_height,
                             facecolor=color_tuple, edgecolor='black')
            ax.add_patch(rect)
            ax.text(rect_width / 2, y_position + rect_height / 2, str(rgb),
                    verticalalignment='center', horizontalalignment='center',
                    fontsize=12, fontweight='bold',
                    color='white' if sum(color_tuple) / 3 < 0.5 else 'black')

        ax.set_xlim(0, rect_width)
        ax.set_ylim(-num_colors * rect_height,
                    rect_height)  # Adjust y-axis limits to ensure all rectangles are visible
        ax.axis('off')
        plt.show()

    @staticmethod
    def to_gradients(rgb_a: RGB,
                     rgb_b: RGB,
                     n: int) -> list[RGB]:
        """
        ========================================================================
         Generate a list of n-RGB forming a gradient from RGB-A to RGB-B.
        ========================================================================
        """

        # Ensure n is at least 2 to create a gradient
        if n == 1:
            return [rgb_a]

        gradient: list[RGB] = list()
        for i in range(n):
            t = i / (n - 1)  # Calculate the interpolation factor
            r = UInterpolation.linear(a=rgb_a.r, b=rgb_b.r, t=t)
            g = UInterpolation.linear(a=rgb_a.g, b=rgb_b.g, t=t)
            b = UInterpolation.linear(a=rgb_a.b, b=rgb_b.b, t=t)
            gradient.append(RGB(r=r, g=g, b=b))

        return gradient

