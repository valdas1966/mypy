from f_astar.c_node import Node
from f_astar.c_opened import Opened
from f_map.c_point import Point


class AStar:
    """
    ============================================================================
     Description: AStar
    ============================================================================
    """

    def __init__(self, map, start, goal):
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
        self.map = map
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
            print(type(self.best), self.best)
            self.__expand()

    def optimal_path(self):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Return: List of Points.
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
        points_neighbors = self.map.neighbors(self.best.point)
        children = {Node(point) for point in points_neighbors} - self.closed
        for child in sorted(children):
            if self.opened.contains(child):
                child = self.opened.get(child)
            g_new = self.best.g + child.w
            if child.g <= g_new:
                continue
            self.__update_node(child, self.best, g_new)
            if not self.opened.contains(child):
                self.opened.push(child)
            
    def __update_node(self, node, father, g):
        """
        =======================================================================
         Description: Update Node (Father and G).
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. node : Node (node to update)
            2. father : Node
            3. g : int
        =======================================================================
        """
        node.father = father
        node.g = g
        node.h = node.point.distance(self.goal)
        node.f = node.g + node.h
