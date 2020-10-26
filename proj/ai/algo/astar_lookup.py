from proj.ai.model.point import Point
from proj.ai.model.point_node import Node
from proj.ai.algo.astar import AStar


class AStarLookup(AStar):

    def __init__(self, grid, start, goal, lookup):
        super().__init__(grid, start, goal)
        self.lookup = lookup

    def run(self):
        """
        ========================================================================
         Description: While the Search is not finished and the Opened is not
                        empty - Run the next move of the A* algorithm.
        ========================================================================
        """
        self.best = Node(self.start)
        self.best.update(father_cand=None, goal=self.goal)
        self.opened.push(self.best)
        while not self.opened.is_empty() and not self.is_found:
            self.next_move()

    def next_move(self):
        """
        ========================================================================
         Description: Run the next move of the Algorithm.
        ========================================================================
        """
        self.best = self.opened.pop()
        self.closed.add(self.best)
        self.__expand()
        if self.best == self.goal or self.best in self.lookup:
            self.is_found = True

    def __expand(self):
        """
        =======================================================================
         Description: Expand the Best.
        =======================================================================
        """
        points_neighbors = self.grid.neighbors(self.best)
        children = {point for point in points_neighbors} - self.closed
        for child in sorted(children):
            if self.opened.contains(child):
                child = self.opened.get(child)
            else:
                child = Node(child)
                if child in self.lookup:
                    child.set_h(self.lookup[child])
                self.opened.push(child)
            child.update(father_cand=self.best, goal=self.goal)
