from f_grid import u_grid


def get_farthest(grid, start, goals):
    """
    ============================================================================
     Description: Return the farthest Goal from the Start.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : Grid.
        2. start : int (Node's Id).
        3. goals : set of int (Set of Node's Id).
    ============================================================================
     Return: int (The Id of the farthest Goal).
    ============================================================================
    """
    distance_max = 0
    goal_farthest = None
    for goal in goals:
        distance = u_grid.manhattan_distance(grid, start, goal)
        if distance > distance_max:
            distance_max = distance
            goal_farthest = goal
    return goal_farthest
