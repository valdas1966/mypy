from f_astar.c_node import Node
from f_astar.c_opened import Opened
from f_grid import u_grid
from f_utils import u_set


class AStarLookup:
    """
    ===========================================================================
     Description: AStar with Lookup-Dict (Perfect Heuristic for some Nodes).
    ===========================================================================
     Methods:
    ---------------------------------------------------------------------------
        1. run()
            Run the algorithm.

        2. get_path() -> List of Points
            Return the Optimal Path from Start to Goal as list of node's id.
    ===========================================================================
    """

    def __init__(self, grid, start, goal, lookup=dict()):
        """
        ===================================================================
         Description: A* Algorithm.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. grid : Grid.
            2. start : int (Start's Id).
            3. goal : int (Goal's Id).
            4. lookup : dict (Point -> int).
        ===================================================================
        """  
        self.start = start
        self.goal = goal
        self.grid = grid
        self.is_found = False
        self.len_optimal = 0

        self.best = Node(start)
        self.best.g = 0

        self.lookup = lookup
        self.closed = set()                     
        self.opened = Opened()
        self.opened.push(self.best)

    def run(self):
        """
        =======================================================================
         Description: Run A* Algorithm.
        =======================================================================
        """
        while not self.is_found and not self.opened.is_empty():
            self.next_move()

    def next_move(self, node_lookup=None):
        """
        ========================================================================
         Description: Run next move of the Algorithm.
        ========================================================================
         Argument:
        ------------------------------------------------------------------------
            1. node_lookup : Node Lookup (from another direction).
        ========================================================================
        """
        if node_lookup:
            self.lookup[node_lookup.idd] = node_lookup.g
        self.best = self.opened.pop()
        while self.best.idd in self.lookup and self.best.h < self.lookup[self.best.idd]:
            self.best.h = self.lookup[self.best.idd]
            self.best.f = self.best.g + self.best.h
            self.opened.push(self.best)
            self.best = self.opened.pop()
        if self.best.idd in self.lookup:
            self.len_optimal = self.best.g + self.lookup[self.best.idd]
            self.is_found = True
            return
        self.closed.add(self.best)
        if self.best.idd == self.goal:
            self.is_found = True
            self.len_optimal = self.best.g
            return
        self._expand()

    def get_path(self):
        if not self.is_found:
            return list()
        if self.best.idd == self.goal:
            node = self.best
            path = [node.idd]
            while node.idd != self.start:
                node = node.father
                path.append(node.idd)
            path.reverse()
            return path
        else:
            node = self.best
            path_1 = [node.idd]
            while node.idd != self.start:
                node = node.father
                path_1.append(node.idd)
            path_1.reverse()
            node = u_set.get(self.closed_lookup, self.best)
            path_2 = list()
            while node.idd != self.goal:
                node = node.father
                path_2.append(node.idd)
            path_2.reverse()
            return path_1 + path_2

    def _expand(self):   
        """
        =======================================================================
         Description: Expand the Best Node's Children.
        =======================================================================
        """     
        row, col = u_grid.to_row_col(self.grid, self.best.idd)
        idds = u_grid.get_neighbors(self.grid, row, col)
        children = {Node(x) for x in idds} - self.closed      
        for child in sorted(children):
            if self.opened.contains(child):
                child = self.opened.get(child)
            else:
                self.opened.push(child)
            g_new = self.best.g + child.w
            if g_new < child.g:
                self._update_node(child, self.best, g_new)

    def _update_node(self, node, father, g):
        """
        =======================================================================
         Description: Update Node.
        =======================================================================
         Attributes:
        -----------------------------------------------------------------------
            1. node : Node (node to update)
            2. father : Node
            3. g : int
        =======================================================================
        """
        node.father = father
        node.g = g
        if node.idd in self.lookup:
            node.h = self.lookup[node.idd]
        else:
            node.h = u_grid.distance(self.grid, node.idd, self.goal)
        node.f = node.g + node.h
