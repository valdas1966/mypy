from proj.ai.model.point import Point
from proj.ai.model.point_node import Node
from proj.ai.algo.astar import AStar
from proj.ai.logic.grid_blocks_ghf import LogicGridBlocksGHF as lgb


class AStarLookup(AStar):
    """
    ============================================================================
     Description: A* Algorithm with Lookup Nodes (Perfect Heuristic to Goal).
    ============================================================================
    """

    def __init__(self, grid, start, goal, lookup=dict()):
        """
        ========================================================================
         Description: Init A* Algorithm
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. start : Point
            3. goal : Point
            4. lookup : Dict {point -> int (True-Distance to Goal)}
        ========================================================================
        """
        assert type(lookup) == dict
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
        # print(self.start, self.goal, self.best)
        self.closed.add(self.best)
        self.__expand()
        if self.best == self.goal:
            self.is_found = True
        if self.best in self.lookup:
            self.is_found = True
            self.closed.remove(self.best)

    def lookup_start(self):
        """
        ========================================================================
         Description: Return Lookup (Dict) of True-Distance to the Start
                        from the Nodes in the Closed-Set (by their G-Value).
        ========================================================================
         Return: Dict {Point -> int (True-Distance to the Start}
        ========================================================================
        """
        lookup = dict()
        for node in self.closed:
            lookup[Point(node.x, node.y)] = node.g
        return lookup

    def lookup_goal(self):
        """
        ========================================================================
         Description: Return Lookup (Dict) of True-Distance to the Goal from
                        the Nodes in the Optimal Path.
        ========================================================================
         Return: Dict {Point -> int (True-Distance to the Goal}
        ========================================================================
        """
        optimal_nodes = list()
        node = self.best
        while node != self.start:
            optimal_nodes.append(node)
            node = node.father
        optimal_nodes.append(self.start)
        return lgb.true_distance(self.grid, self.goal, optimal_nodes)

    def __expand(self):
        """
        =======================================================================
         Description: Expand the Best.
        =======================================================================
        """
        points_neighbors = self.grid.neighbors(self.best)
        children = {point for point in points_neighbors} - self.closed
        for child in sorted(children):
            # Add Child into Opened if it is not there
            if self.opened.contains(child):
                child = self.opened.get(child)
            else:
                child = Node(child)
                self.opened.push(child)
            # Update Child if needed
            child.update(father_cand=self.best, goal=self.goal)
            # If Child in Lookup -> Set it's H-Value to be the True-Distance
            if child in self.lookup:
                child.set_h(self.lookup[child])
