from f_astar.c_node import Node
from f_astar.c_opened import Opened
from f_grid import u_grid
from f_utils import u_set


class AStar:
    """
    ============================================================================
     Description: AStar
    ============================================================================
    """

    def __init__(self, grid, start, goal):
        """
        ========================================================================
         Description: A* Algorithm.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. start : Point
            3. goal : Point
        ========================================================================
        """  
        self.start = start
        self.goal = goal
        self.grid = grid
        self.is_found = False
        self.closed = set()                     
        self.opened = Opened()
        self.best = Node(start)
        self.opened.push(self.best)

    def run(self):
        """
        ========================================================================
         Description: While the Search is not finished and the Opened is not
                        empty - Run the next move of the A* algorithm.
        ========================================================================
        """
        while not self.opened.is_empty() and not self.is_found:
            self.next_move()

    def next_move(self):
        """
        ========================================================================
         Description:
        ------------------------------------------------------------------------
            1. Best <- Opened.Pop()
            2. Closed.Add(Best)
            3. If Best == Goal:
                3.1 Is_Found = True
            4. Otherwise:
                4.1 Expand Best
        ========================================================================
        """
        self.best = self.opened.pop()
        self.closed.add(self.best)
        if self.best.point == self.goal:
            self.is_found = True
        else:
            self.__expand()

    def get_path(self):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Return: list of int (List of Points).
        =======================================================================
        """
        if not self.is_found:
            return list()
        node = self.best
        path = [node.point]
        while node.point != self.start:
            node = node.father
            path.append(node.point)
        path.reverse()
        return path

    def __expand(self):
        """
        =======================================================================
         Description: Expand the Best.
        =======================================================================
        """
        row, col = u_grid.to_row_col(self.grid, self.best.idd)
        idds = u_grid.get_neighbors(self.grid, row, col)
        children = {Node(x) for x in idds} - self.closed      
        for child in sorted(children):
            if self.opened.contains(child):
                child = self.opened.get(child)
            g_new = self.best.g + child.w
            if child.g <= g_new:
                continue
            self._update_node(child,self.best,g_new)
            if not self.opened.contains(child):
                self.opened.push(child)
            
    def __update_node(self, node, father, g):
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
        node.h = u_grid.distance(self.grid, node.idd, self.goal)
        node.f = node.g + node.h
