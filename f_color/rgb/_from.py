from f_color.rgb.main import RGB


class From:
    """
    ============================================================================
     Construction methods for RGB from external formats.
    ============================================================================
    """

    @staticmethod
    def ints(r: int,
             g: int,
             b: int) -> RGB:
        """
        ========================================================================
         Convert integer values (0-255) to an RGB-object.
        ========================================================================
        """
        return RGB(r=r / 255, g=g / 255, b=b / 255)

    @staticmethod
    def hex(hex_str: str) -> RGB:
        """
        ========================================================================
         Convert a hex-string to an RGB-object.
        ========================================================================
        """
        hex_str = hex_str.lstrip('#')
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return From.ints(r=r, g=g, b=b)
