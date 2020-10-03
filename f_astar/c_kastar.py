from f_astar.c_node import Node
from f_astar.c_opened import Opened
from f_grid import u_grid
from f_utils import u_set


class KAStar:

    def __init__(self, grid, start, goals):
        """
        =======================================================================
         Description: KA* Algorithm.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. grid : Grid.
            2. start : int (Start Idd).
            3. goals : set of int (Goal Idd).
        =======================================================================
        """  
        self.start = start
        self.goals = goals
        self.goals_active = set(self.goals)
        self.grid = grid
        self.opened = Opened()
        self.closed = set()
        self.best = Node(start)
        self.counter_h = 0

    def run(self):
        """
        =======================================================================
         Description: Run KA* Algorithm.
        =======================================================================
        """
        self._update_node(self.best, g=0)
        self.opened.push(self.best)
        while self.goals_active and not self.opened.is_empty():
            self.best = self.opened.pop()
            self.closed.add(self.best)
            if self.best.idd in self.goals_active:
                self.goals_active.remove(self.best.idd)
                if not self.goals_active: 
                    return
                self._update_opened()     
            self._expand_best()

    def get_path(self, goal):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. goal : Node
        =======================================================================
         Return: list of Node (Empty List on No-Solution).
        =======================================================================
        """            
        node = u_set.get(self.closed, Node(goal))
        if not node:
            return list()
        path = [node.idd]
        while node.idd != self.start:
            node = node.father
            path.append(node.idd)
        path.reverse()        
        return path

    def _update_opened(self):
        """
        =======================================================================
         Description: Update h of Opened Nodes (after removing active goal).
        =======================================================================
        """
        for node in self.opened.get_nodes():
            node.h = self._get_min_h(node)
            node.f = node.g + node.h

    def _expand_best(self):   
        """
        ===================================================================
         Description: Expand the Best Node's Children.
        ===================================================================
        """     
        row, col = u_grid.to_row_col(self.grid, self.best.idd)
        idds = u_grid.get_neighbors(self.grid, row, col)
        children = {Node(x) for x in idds} - self.closed      
        for child in sorted(children):
            if self.opened.contains(child):
                child = self.opened.get(child)
            g_new = self.best.g + child.w
            # Already in Opened with best g 
            if child.g <= g_new:
                continue
            self._update_node(child, g_new)
            self.opened.push(child)

    def _update_node(self, node, g):
        """
        =======================================================================
         Description: Update Node.
        =======================================================================
         Attributes:
        -----------------------------------------------------------------------
            1. node : Node (Node to update).
            2. g : int
        =======================================================================
        """
        if not node == self.best:
            node.father = self.best
        node.g = g
        node.h = self._get_min_h(node)
        node.f = node.g + node.h

    def _get_min_h(self, node):
        """
        =======================================================================
         Description: Calc h toward the Active Goals and Return the Minimum.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. node : Node
        =======================================================================
         Return: float (Minimum h toward the Active Goals).
        =======================================================================
        """
        h = float('Infinity')
        for goal in self.goals_active:
            h = min(h, self._get_manhattan_distance(node,goal))
        return h

    def _get_manhattan_distance(self, node, goal):
        """
        =======================================================================
         Description: Return Manhattan Distance between Node and Goal.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. node : Node.
            2. goal : int (Goal's Id).
        =======================================================================
         Return: float (Manhattan Distance between Node and Goal).
        =======================================================================
        """
        self.counter_h += 1
        return u_grid.distance(self.grid, node.idd, goal)
