from f_color.rgb import RGB
import numpy as np


class FactoryRGB:
    """
    ============================================================================
     Factory-Class for RGB-Colors.
    ============================================================================
    """

    @staticmethod
    def from_ints(# Red-Value (0-255)
                  r: int,  # Red-Value (0-255)
                  # Green-Value (0-255)
                  g: int,
                  # Blue-Value (0-255)
                  b: int) -> RGB:
        """
        ========================================================================
         Convert an integer-tuple (0-255) to an RGB-object.
        ========================================================================
         Example: FactoryRGB.from_ints(r=255, g=0, b=0) -> RGB(1, 0, 0)
        ========================================================================
        """
        # Convert integers to floats.
        r = r / 255
        g = g / 255
        b = b / 255
        # Return the RGB.
        return RGB(r=r, g=g, b=b)
    
    @staticmethod
    def from_hex(hex: str) -> RGB:
        """
        ========================================================================
         Convert a hex-string to an RGB-object.
        ========================================================================
         Example: FactoryRGB.from_hex('#FF0000') -> RGB(1, 0, 0)
        ========================================================================
        """
        # Remove the '#' from the hex-color.
        hex = hex.lstrip('#')
        # Convert the hex-color to RGB.
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)
        # Return the RGB.
        return FactoryRGB.from_ints(r=r, g=g, b=b)
    

    @staticmethod
    def gradient(# First color in the gradient
                 a: RGB,
                 # Last color in the gradient
                 b: RGB,
                 # Number of steps
                 n: int) -> list[RGB]:
        """
        ========================================================================
         Generate a list of n-RGB forming a gradient from RGB-A to RGB-B.
         Useful for creating a gradient list[RGB] between two given RGB.
        ========================================================================
         Input:
        ------------------------------------------------------------------------
            FactoryRGB.gradient(a=RGB('BLACK'), b=RGB('WHITE'), n=3)
        ------------------------------------------------------------------------    
         Output:
        ------------------------------------------------------------------------
            [RGB(0, 0, 0), RGB(0.5, 0.5, 0.5), RGB(1, 1, 1)]
        ========================================================================
        """
        # If n is 1, return a list with the first color.
        if n == 1:
            return [a]
        # If n is 2, return a list with the first and last colors.
        elif n == 2:
            return [a, b]
        
        # Calculate the gradient values for each color.
        reds: list[float] = np.linspace(start=a.r, stop=b.r, num=n)
        greens: list[float] = np.linspace(start=a.g, stop=b.g, num=n)
        blues: list[float] = np.linspace(start=a.b, stop=b.b, num=n)

        # Return the gradient list.
        return [RGB(r=r, g=g, b=b)
                for r, g, b
                in zip(reds, greens, blues)]

    @staticmethod
    def gradient_multi(stops: list[RGB], n: int) -> list[RGB]:
        """
        ============================================================================
         Create a smooth gradient over multiple RGB stops (e.g., Green → Yellow → Red),
         ensuring exactly `n` total colors, without duplicate overlaps.
        ============================================================================
        """
        if n <= 1 or len(stops) < 2:
            return stops[:1]

        n_segments = len(stops) - 1

        # Total colors needed = n
        # Each segment will generate seg_n colors (inclusive), and we remove 1 color
        # from each segment after the first to avoid overlap.
        # So we initially plan for (n + (segments - 1)) colors, then subtract overlaps
        base_steps = n + (n_segments - 1)
        steps_per_segment = base_steps // n_segments
        remainder = base_steps % n_segments

        rgbs: list[RGB] = []

        for i in range(n_segments):
            # Add remainder to the first few segments
            seg_n = steps_per_segment + (1 if i < remainder else 0)
            start, end = stops[i], stops[i + 1]
            segment_colors = FactoryRGB.gradient(start, end, seg_n)

            # Skip first color of every segment after the first to avoid duplicates
            if i != 0:
                segment_colors = segment_colors[1:]

            rgbs.extend(segment_colors)

        return rgbs[:n]  # Trim in case of any rounding issues

    @staticmethod
    def random(n: int) -> list[RGB]:
        """
        ========================================================================
         Generate a list of n-random RGB-colors.
        ========================================================================
        """
        r = np.random.rand(n)
        g = np.random.rand(n)
        b = np.random.rand(n)
        return [RGB(r=r, g=g, b=b)
                for r, g, b
                in zip(r, g, b)]
