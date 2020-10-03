import sys
sys.path.append('D:\\MyPy')
sys.path.append('G:\\MyPy')

from f_astar.c_node import Node
from f_astar.c_opened import Opened
from f_grid import u_grid
from f_utils import u_set


class AStar:
    """
    ===========================================================================
     Description: AStar
    ===========================================================================
     Methods:
    ---------------------------------------------------------------------------
        1. get_path() -> list of int (List of Node'd Id, Optimal Path to Goal).
    ===========================================================================
    """

    def __init__(self, grid, start, goal):
        """
        ===================================================================
         Description: A* Algorithm.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. grid : Grid.
            2. start : int (Start's Id).
            3. goal : int (Goal's Id).
        ===================================================================
        """  
        self.start = start
        self.goal = goal
        self.grid = grid

        self.f_goal = 0
        self.best = Node(start)
        self._update_node(node=self.best, father=None, g=0)
        
        self.closed = set()                     
        self.opened = Opened()
        self.opened.push(self.best)

    def run(self, goal_new=None):
        """
        =======================================================================
         Description: Run A* Algorithm.
        =======================================================================
        """
        if goal_new:
            self.goal = goal_new
            if Node(self.goal) in self.closed:
                self.best = u_set.get(self.closed, Node(self.goal))
                return
            for node in self.opened.get_nodes():
                self._update_node(node=node, father=node.father, g=node.g)

        while not (self.opened.is_empty()):
            self.best = self.opened.pop()
            self.closed.add(self.best)
            self._expand()
            if self.best.idd == self.goal:
                self.f_goal = self.best.f
                return
        self.best = None

    def get_path(self):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Return: list of int (List of Nodes Idds or Empty List on No-Solution).
        =======================================================================
        """
        node = self.best
        if not node:
            return list()
        path = [node.idd]
        while node.idd != self.start:
            node = node.father
            path.append(node.idd)
        path.reverse()
        return path
            
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
            g_new = self.best.g + child.w
            if child.g <= g_new:
                continue
            self._update_node(child,self.best,g_new)
            if not self.opened.contains(child):
                self.opened.push(child)
            
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
        node.h = u_grid.distance(self.grid, node.idd, self.goal)
        node.f = node.g + node.h
