from f_grid import u_grid
from f_grid import u_gen_grid
from f_utils import u_dict
from f_map.c_point import Point
from f_const.directions import Directions
import random


class Map:
    """
    ============================================================================
     Description: Represents 2D Grid Map.
    ============================================================================
    """

    def __init__(self, grid=None, rows=None, cols=None, path=None,
                 obstacles=None):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid of the Map.
        ========================================================================
        """
        if grid is not None:
            self.grid = grid
        elif path:
            self.grid = u_gen_grid.from_map(path)
        else:
            self.grid = u_gen_grid.random(rows, cols, obstacles)
        self.shape = self.grid.shape
        self.rows = self.grid.shape[0]
        self.cols = self.grid.shape[1]

    def set_value(self, val, idd=None, row=None, col=None):
        """
        ========================================================================
         Description: Set Value in Map.Grid by Idd or by Row and Col.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. val : obj (Value to Set).
            2. idd : int (Node's Idd).
            3. row : int (Node's Row).
            4. col : int (Node's Col).
        ========================================================================
        """
        if idd is not None:
            row, col = self.to_row_col(idd)
        self.grid[row][col] = val

    def offsets(self, idd_1, idd_2=None):
        """
        ========================================================================
         Description: Return the offsets of the Node.
        ------------------------------------------------------------------------
            1. If there are one Node -> Return offsets from the axises.
                                        (up, right, down, left)
            2. If there are two Nodes -> Return offsets from the each one.
                                         (top, left)
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. idd_1 : int (Node's Id).
            2. idd_2 : int (Node's Id).
        ========================================================================
         Return: tuple (int, int, int, int) or (int, int).
        ========================================================================
        """
        row_1, col_1 = self.to_row_col(idd_1)
        if idd_2 is None:
            up = row_1
            right = self.cols - col_1 - 1
            down = self.rows - row_1 - 1
            left = col_1
            return up, right, down, left
        row_2, col_2 = self.to_row_col(idd_2)
        top = row_1 - row_2
        left = col_1 - col_2
        return top, left

    def to_row_col(self, idd):
        """
        ========================================================================
         Description: Return Tuple of the Node's Row and Col (row, col).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. idd : int (Node's Id).
        ========================================================================
         Return: tuple (int, int).
        ========================================================================
        """
        return u_grid.to_row_col(self.grid, idd)

    def to_point(self, idd):
        """
        ========================================================================
         Description: Return Point-Representation of the Node.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. idd : int (Node's Idd).
        ========================================================================
         Return: Point.
        ========================================================================
        """
        row, col = self.to_row_col(idd)
        x = self.grid.shape[0] - row - 1
        y = col
        return Point(x, y)

    def valid_idds(self):
        """
        ========================================================================
         Description: Return Set of Valid Idds of the Map.
        ========================================================================
         Return: set of int.
        ========================================================================
        """
        return set(u_grid.get_valid_idds(self.grid))

    def distance(self, idd_1, idd_2):
        """
        ========================================================================
         Description: Return Manhattan-Distance between two Nodes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. idd_1 : int (Node's Id).
            2. idd_2 : int (Node's Id).
        ========================================================================
         Return: int (Manhattan-Distance between two Nodes).
        ========================================================================
        """
        return u_grid.distance(self.grid, idd_1, idd_2)

    def get_random_idds(self, n):
        """
        ========================================================================
         Description: Return Set of N random Nodes' Idds from the Map.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. n : int (Number of Random Nodes' Idds to return).
        ========================================================================
         Return: set of int (Set of Random Node's Idds).
        ========================================================================
        """
        idds = list(self.valid_idds())
        random.shuffle(idds)
        return set(idds[:n])

    def dict_f(self, start, goal):
        """
        ========================================================================
         Description: Return Dict of F-Values {Node.idd: Node.f}
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. start : int (Node's Id).
            2. goal : int (Node's Id).
        ========================================================================
         Return: dict of int {int: int}.
        ========================================================================
        """
        dict_g = u_grid.to_dict_g(self.grid, start)
        dict_h = u_grid.to_dict_h(self.grid, goal)
        return u_dict.sum(dict_g, dict_h)

    def nearest(self, node_1, nodes):
        """
        ========================================================================
         Description: Return the nearest node to the node_1.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. node_1 : int (Source Node Idd).
            2. nodes : set of int (Nodes Idd).
        ========================================================================
         Return: int (The Nearest Node's Idd).
        ========================================================================
        """
        min_h = float('Infinity')
        node_nearest = None
        for node_2 in nodes:
            h = self.distance(node_1, node_2)
            if h < min_h:
                node_nearest = node_2
                min_h = h
        return node_nearest

    def nearest_closed(self, node, closed):
        """
        ============================================================================
         Description: Return the Distances to the Nearest Closed-Node from
                        all directions (up, right, down, left).
        ============================================================================
         Arguments:
        ----------------------------------------------------------------------------
            1: node : int (Node's Id).
            2. closed : set of int.
        ============================================================================
         Return: dict of { Directions: int (min distance) }.
        ============================================================================
        """
        distances = {Directions.UP: float('Infinity'),
                     Directions.RIGHT: float('Infinity'),
                     Directions.DOWN: float('Infinity'),
                     Directions.LEFT: float('Infinity')}
        point_1 = self.to_point(node)
        for node_2 in closed:
            point_2 = self.to_point(node_2)
            direction = Point.compass_direction(point_1, point_2)
            distance = point_1.distance(point_2)
            distances[direction] = min(distances[direction], distance)
        return distances
