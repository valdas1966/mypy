import collections
import u_grid

class BFS:
    """
    ===========================================================================
     Description: Breadth-First Search for Grid.
    ===========================================================================
    """
    
    def __init__(self, grid, start, goal):
        opened = collections.deque([start])
        closed = set()
        while opened:
            idd = opened.popleft()
            for child in u_grid.get_children(grid,idd=idd) - closed:
                closed.add(child)
                opened.append(child)



queue = collections.deque()
queue.append(1)
queue.append(2)
print(queue)   
print(queue.popleft())
print(queue)     