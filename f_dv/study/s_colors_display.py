import matplotlib.pyplot as plt
import numpy as np

def display_colors(rgb_colors: list):
    """
    Display a list of RGB colors on the screen with RGB values on top.

    Parameters:
    rgb_colors (list): List of RGB tuples (each tuple has three float values between 0 and 1).
    """
    num_colors = len(rgb_colors)
    cols = 10  # Number of columns
    rows = num_colors // cols + (num_colors % cols > 0)

    fig, axes = plt.subplots(rows, cols, figsize=(12, rows * 0.6))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)

    for ax, color in zip(axes.flat, rgb_colors):
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=color))
        rgb_text = f"({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})"
        ax.text(0.5, 0.5, rgb_text, ha='center', va='center', fontsize=8, fontweight='bold', color='white' if sum(color)/3 < 0.5 else 'black')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    for ax in axes.flat[num_colors:]:
        ax.axis('off')

    plt.show()

# Example usage
rgb_colors = [(0/256, 26/256, 51/256)]

display_colors(rgb_colors)
