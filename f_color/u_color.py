import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from f_color.rgb import RGB


class UColor:
    """
    ============================================================================
     Utility class for color visualization.
    ============================================================================
    """

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
        rect_height = max(min_rect_height, 10.0 / num_colors)
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        for i, rgb in enumerate(rgbs):
            color_tuple = rgb.to.tuple()
            y_position = -i * rect_height
            rect = Rectangle((0, y_position), rect_width, rect_height,
                             facecolor=color_tuple, edgecolor='black')
            ax.add_patch(rect)
            ax.text(rect_width / 2, y_position + rect_height / 2,
                    str(rgb),
                    verticalalignment='center',
                    horizontalalignment='center',
                    fontsize=12, fontweight='bold',
                    color=('white' if sum(color_tuple) / 3 < 0.5
                           else 'black'))
        ax.set_xlim(0, rect_width)
        ax.set_ylim(-num_colors * rect_height, rect_height)
        ax.axis('off')
        plt.show()

