from f_color.rgb.main import RGB
import numpy as np


class Factory:
    """
    ============================================================================
     Factory-Class for RGB presets and generation.
    ============================================================================
    """

    @staticmethod
    def gradient(a: RGB,
                 b: RGB,
                 n: int) -> list[RGB]:
        """
        ========================================================================
         Generate a list of n-RGB forming a gradient from a to b.
        ========================================================================
        """
        if n == 1:
            return [a]
        if n == 2:
            return [a, b]
        reds = np.linspace(start=a.r, stop=b.r, num=n)
        greens = np.linspace(start=a.g, stop=b.g, num=n)
        blues = np.linspace(start=a.b, stop=b.b, num=n)
        return [RGB(r=r, g=g, b=b)
                for r, g, b
                in zip(reds, greens, blues)]

    @staticmethod
    def gradient_multi(stops: list[RGB],
                       n: int) -> list[RGB]:
        """
        ========================================================================
         Create a smooth gradient over multiple RGB stops.
        ========================================================================
        """
        if n <= 1 or len(stops) < 2:
            return stops[:1]
        n_segments = len(stops) - 1
        base_steps = n + (n_segments - 1)
        steps_per_segment = base_steps // n_segments
        remainder = base_steps % n_segments
        rgbs = []
        for i in range(n_segments):
            seg_n = steps_per_segment + (1 if i < remainder else 0)
            segment = Factory.gradient(stops[i], stops[i + 1], seg_n)
            if i != 0:
                segment = segment[1:]
            rgbs.extend(segment)
        return rgbs[:n]

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
        return [RGB(r=ri, g=gi, b=bi)
                for ri, gi, bi
                in zip(r, g, b)]
