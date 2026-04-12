from __future__ import annotations
from typing import TYPE_CHECKING
from PIL import Image, ImageDraw

if TYPE_CHECKING:
    from f_ds.grids.grid.map.main import GridMap
    from f_ds.grids.cell.i_1_map.main import CellMap
    from f_color.rgb.main import RGB

# Constants
_BLACK = (0, 0, 0)
_GRAY = (200, 200, 200)


class To:
    """
    ========================================================================
     Conversion methods for GridMap.
    ========================================================================
    """

    def __init__(self, grid: GridMap) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._grid = grid

    def image(self,
              path: str,
              colors: list[tuple[RGB, set[CellMap]]] = None,
              cell_size: int = 20) -> None:
        """
        ========================================================================
         Save a 2D image of the grid to a file.
         - Invalid cells (obstacles) are BLACK.
         - Valid cells not in any color set are GRAY.
         - Valid cells in a color set are painted with that color.
        ========================================================================
        """
        grid = self._grid
        # Invert: (row, col) -> rgb_tuple for O(1) lookup
        cell_colors: dict[tuple[int, int], tuple[int, int, int]] = {}
        if colors:
            for rgb, cells in colors:
                rgb_tuple = rgb.to.tuple(to_int=True)
                for cell in cells:
                    cell_colors[(cell.row, cell.col)] = rgb_tuple
        # Create image
        width = grid.cols * cell_size
        height = grid.rows * cell_size
        img = Image.new(mode='RGB',
                        size=(width, height),
                        color=_BLACK)
        draw = ImageDraw.Draw(img)
        # Draw cells
        for row in range(grid.rows):
            for col in range(grid.cols):
                cell = grid[row][col]
                if not cell:
                    continue
                x = col * cell_size
                y = row * cell_size
                color = cell_colors.get((row, col), _GRAY)
                draw.rectangle(xy=[x, y,
                                   x + cell_size - 1,
                                   y + cell_size - 1],
                               fill=color)
        img.save(path)
