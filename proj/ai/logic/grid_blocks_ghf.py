from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.model.point import Point
from proj.ai.model.point_node import Node
from f_utils import u_set
import collections


class LogicGridBlocksGHF:

    @staticmethod
    def to_dict_h(grid, goal):
        """
        ========================================================================
         Description: Return Dictionary of Heuristic Values per each Point
                        (heuristic distance to the Goal).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. goal : Point
        ========================================================================
         Return: dict {Point -> int (Heuristic Distance to the Goal)}.
        ========================================================================
        """
        assert type(grid) == GridBlocks, f'type(grid)={type(grid)}'
        assert type(goal) == Point, f'type(goal)={type(goal)}'
        assert grid.is_valid_point(goal), f'is_valid_point(goal)=' \
                                          f'{grid.is_valid_point(goal)}'
        dict_h = dict()
        for point in grid.points():
            dict_h[point] = point.distance(goal)
        return dict_h

    @staticmethod
    def to_dict_g(grid, start):
        """
        ========================================================================
         Description: Return Dictionary of G-Value for each Point
                        (true distance from the Start).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : GridBlocks
            2. start : Point
        ========================================================================
         Return: Dict {Point -> int (G-Value, True distance from the Start)}.
        ========================================================================
        """
        assert type(grid) == GridBlocks, f'type(grid)={type(grid)}'
        assert type(start) == Point, f'type(goal)={type(start)}'
        assert grid.is_valid_point(start), f'is_valid_point(start)=' \
                                           f'{grid.is_valid_point(start)}'
        opened = collections.deque([(start, 0)])
        closed = dict()
        while opened:
            point, g = opened.popleft()
            closed[point] = g
            children = set(grid.neighbors(point)) - closed.keys()
            for child in children:
                opened.append((child, g + 1))
        return closed

    @staticmethod
    def to_dict_f(grid, start, goal):
        """
        ========================================================================
         Description: Return Dict of F-Values for each Point (F = G + H).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : GridBlocks
            2. start : Point
            3. goal : Point
        ========================================================================
         Return: Dict of F-Values of each Point {Point -> int (F-Value)}.
        ========================================================================
        """
        assert type(grid) == GridBlocks, f'type(grid)={type(grid)}'
        assert type(start) == Point, f'type(goal)={type(start)}'
        assert type(goal) == Point, f'type(goal)={type(goal)}'
        assert grid.is_valid_point(start), f'is_valid_point(start)=' \
                                           f'{grid.is_valid_point(start)}'
        assert grid.is_valid_point(goal), f'is_valid_point(goal)=' \
                                          f'{grid.is_valid_point(goal)}'
        dict_g = LogicGridBlocksGHF.to_dict_g(grid, start)
        dict_h = LogicGridBlocksGHF.to_dict_h(grid, goal)
        dict_f = dict()
        for point in dict_g.keys():
            dict_f[point] = dict_g[point] + dict_h[point]
        return dict_f

    @staticmethod
    def to_nodes(grid, start, goal):
        """
        ========================================================================
         Description: Return Sorted List of Nodes (with G, H and F values).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : GridBlocks
            2. start : Point
            3. goal : Point
        ========================================================================
         Return: Sorted List of Nodes (with, G, H and F values).
        ========================================================================
        """
        assert type(grid) == GridBlocks, f'type(grid)={type(grid)}'
        assert type(start) == Point, f'type(goal)={type(start)}'
        assert type(goal) == Point, f'type(goal)={type(goal)}'
        assert grid.is_valid_point(start), f'is_valid_point(start)=' \
                                           f'{grid.is_valid_point(start)}'
        assert grid.is_valid_point(goal), f'is_valid_point(goal)=' \
                                          f'{grid.is_valid_point(goal)}'
        dict_g = LogicGridBlocksGHF.to_dict_g(grid, start)
        nodes = list()
        for point, g in dict_g.items():
            node = Node(point=point, goal=goal)
            node.g = g
            node.f = node.g + node.h
            nodes.append(node)
        return sorted(nodes)

    @staticmethod
    def to_nodes_below_f(grid, start, goal):
        """
        ========================================================================
         Description: Return Sorted List of Nodes with F-Values less than
                        F-Value of the Goal.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : GridBlocks
            2. start : Point
            3. goal : Point
        ========================================================================
         Return: Sorted List of Nodes with F-Values less than of the Goal.
        ========================================================================
        """
        assert type(grid) == GridBlocks, f'type(grid)={type(grid)}'
        assert type(start) == Point, f'type(goal)={type(start)}'
        assert type(goal) == Point, f'type(goal)={type(goal)}'
        assert grid.is_valid_point(start), f'is_valid_point(start)=' \
                                           f'{grid.is_valid_point(start)}'
        assert grid.is_valid_point(goal), f'is_valid_point(goal)=' \
                                          f'{grid.is_valid_point(goal)}'
        nodes = LogicGridBlocksGHF.to_nodes(grid, start, goal)
        goal = u_set.get(set(nodes), goal)
        nodes_f = set()
        for node in nodes:
            if node.f < goal.f:
                nodes_f.add(node)
            else:
                break
        return nodes_f