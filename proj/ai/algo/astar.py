from proj.ai.model.point import Point
from proj.ai.model.point_node import Node
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.model.opened import Opened


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
            1. grid : GridBlcoks
            2. start : Point
            3. goal : Point
        ========================================================================
        """
        assert type(grid) == GridBlocks, f'type(grid)={type(grid)}'
        assert type(start) == Point, f'type(start)={type(start)}'
        assert type(goal) == Point, f'type(goal)={type(goal)}'
        assert grid.is_valid_point(start), f'start={start}, grid.shape=(' \
                                           f'{grid.rows,grid.cols}), ' \
                                           f'grid.is_block(start)=' \
                                           f'{grid.is_block(start)}'
        assert grid.is_valid_point(start), f'start={goal}, grid.shape=(' \
                                           f'{grid.rows, grid.cols}), ' \
                                           f'grid.is_block(goal)=' \
                                           f'{grid.is_block(goal)}'
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
            else:
                self.opened.push(child)
            g_new = self.best.g + child.w
            if child.g <= g_new:
                continue
            self.__update_node(child, self.best, g_new)
            

grid = GridBlocks(rows=5)
start = Point(0, 0)
goal = Point(1, 1)
astar = AStar(grid, start, goal)
astar.run()