import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def get_brightness(color):
    # Calculate the perceived brightness of the color using the luminance formula
    r, g, b = mcolors.to_rgb(color)
    return 0.299 * r + 0.587 * g + 0.114 * b

def visualize_colors():
    color_names = list(mcolors.CSS4_COLORS.keys())
    color_values = [mcolors.to_rgb(color) for color in color_names]

    # Sort colors by brightness
    sorted_colors = sorted(zip(color_names, color_values), key=lambda x: get_brightness(x[1]), reverse=True)
    color_names, color_values = zip(*sorted_colors)

    num_colors = len(color_names)
    cols = 10  # Number of columns
    rows = num_colors // cols + (num_colors % cols > 0)

    fig, axes = plt.subplots(rows, cols, figsize=(12, rows * 0.6))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)

    for ax, name, value in zip(axes.flat, color_names, color_values):
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=value))
        ax.text(0.5, 1.05, name, ha='center', va='bottom', fontsize=8, fontweight='bold', transform=ax.transAxes)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    for ax in axes.flat[num_colors:]:
        ax.axis('off')

    plt.show()

visualize_colors()
