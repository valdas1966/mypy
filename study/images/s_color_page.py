import cv2
import numpy as np


def generate_coloring_page(path_in, path_out):
    # Step 1: Read the input image
    img = cv2.imread(path_in)

    # Step 2: Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply a bilateral filter to reduce noise but keep edges sharp
    blurred = cv2.bilateralFilter(gray, 9, 75, 75)

    # Step 4: Use Canny edge detection to find outlines
    edges = cv2.Canny(blurred, 50, 150)

    # Step 5: Thicken the edges using dilation (makes it easier for kids to color)
    kernel = np.ones((2, 2), np.uint8)
    thick_edges = cv2.dilate(edges, kernel, iterations=1)

    # Step 6: Invert the colors (white background, black lines)
    inverted = cv2.bitwise_not(thick_edges)

    # Step 7: Save the final coloring page image
    cv2.imwrite(path_out, inverted)


# Example usage
generate_coloring_page("D:/temp/image.png",
                       "D:/temp/coloring_page_clean.png")

