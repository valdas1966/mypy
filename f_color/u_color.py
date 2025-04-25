import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from f_color.rgb import RGB


class UColor:

    @staticmethod
    def show(rgbs: list[RGB]) -> None:
        """
        ========================================================================
         Display list list of RGB colors as rectangles with their STR-REPR.
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
         Generate list List of n-RGB forming list gradient from rgb_a to rgb_b.
        ========================================================================
        """
        def interpolate(start: float, end: float, factor: float) -> float:
            return start + (end - start) * factor
        # Ensure n is at least 2 to create a gradient
        if n == 1:
            return [rgb_a]

        gradient = []
        for i in range(n):
            factor = i / (n - 1)  # Calculate the interpolation factor
            r = interpolate(rgb_a.r, rgb_b.r, factor)
            g = interpolate(rgb_a.g, rgb_b.g, factor)
            b = interpolate(rgb_a.b, rgb_b.b, factor)
            gradient.append(RGB(r=r, g=g, b=b))

        return gradient

