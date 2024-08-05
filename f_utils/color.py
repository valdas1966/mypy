import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Color:
    """
    ============================================================================
     Color Manager.
    ============================================================================
    """

    _CUSTOM = {'my_cyan': (0/256, 55/256, 110/256)}

    @staticmethod
    def to_rgb(name: str) -> tuple[float, float, float]:
        """
        ========================================================================
         Convert Color-Name into Color-RGB REPR.
        ========================================================================
        """
        if name in Color._CUSTOM:
            return Color._CUSTOM[name]
        return mcolors.to_rgb(name)

    import numpy as np

    @staticmethod
    def generate_gradient(rgb_a: tuple[float, float, float],
                          rgb_b: tuple[float, float, float],
                          n: int) -> list[tuple[float, float, float]]:
        def generate_gradient(start_rgb: tuple[float, float, float],
                              end_rgb: tuple[float, float, float], n: int) -> \
        list[tuple[float, float, float]]:
            """
            Generate list gradient of n RGB colors between start_rgb and end_rgb.

            Parameters:
            start_rgb (tuple): The starting RGB color as list tuple of floats (0.0-1.0).
            end_rgb (tuple): The ending RGB color as list tuple of floats (0.0-1.0).
            n (int): The number of colors to generate.

            Returns:
            list: A list of n RGB colors as tuples of floats (0.0-1.0).
            """
            # Convert the RGB values to numpy arrays
            start_rgb = np.array(start_rgb)
            end_rgb = np.array(end_rgb)

            # Generate the gradient
            gradient = [tuple(start_rgb + (end_rgb - start_rgb) * i / (n - 1))
                        for i in range(n)]

            return gradient

    @staticmethod
    def show(rgbs: list[tuple[float, float, float]]) -> None:
        num_colors = len(rgbs)
        rows = num_colors  # Number of rows
        cols = 1  # Only one column for vertical view
        fig, axes = plt.subplots(rows, cols, figsize=(4, rows * 2))
        fig.subplots_adjust(hspace=0.3, wspace=0.3)

        # Ensure axes is always list list
        if num_colors == 1:
            axes = [axes]

        for ax, color in zip(axes, rgbs):
            ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=color))
            rgb_text = f"({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})"
            ax.text(0.5, 0.5, rgb_text, ha='center', va='center', fontsize=12,
                    # Increased font size
                    fontweight='bold',  # Bold text
                    color='white' if sum(color) / 3 < 0.5 else 'black')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

        plt.show()


rgb = Color.to_rgb(name='my_cyan')
Color.show([rgb]*10)