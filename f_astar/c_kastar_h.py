from c_astar_h import AStar_H
import u_grid
import u_set

class KAStar_H:
    """
    ===========================================================================
     Description: KA* with Heuristic Improvements.
    ===========================================================================
    """
    
    def __init__(self, grid, start, goals):
       self.grid = grid
       self.start = start
       self.goals = goals
       
       self.counter_h = 0
       self.paths = dict()
       self.opened = set()
       self.closed = set()
       self.has_solution = True
       
       
    def run(self):
       for goal in self._sorted_goals():
           self._update_opened(goal)
           self.counter_h += len(self.opened)
           astar = AStar_H(self.grid, self.start, goal, self.opened, self.closed)
           self.counter_h += len(astar.closed) - len(self.closed)
           self.counter_h += len(astar.opened._opened) - len(self.opened)
           if not astar.best:
               self.has_solution = False
               break
           self.paths[goal] = astar.get_path()
           self.opened = astar.opened.get_nodes()
           self.closed.update(astar.closed)
           

    def get_path(self, goal):
        return self.paths[goal]
       
        
    def _sorted_goals(self):
        """
        =======================================================================
         Description: Return Sorted List of Goals by min distance from Start.
        =======================================================================
         Return: list of int (Sorted List of Goals Id by min distance).
        =======================================================================
        """
        dic = dict()
        for goal in self.goals:
            dic[goal] = u_grid.manhattan_distance(self.grid, self.start, goal)
            self.counter_h += 1
        return [k for k, v in sorted(dic.items(), key=lambda item: item[1])]
    
    
    def _update_opened(self, goal):
        """
        =======================================================================
         Description: Update Opened with new heuristic (new goal).
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. goal : int (New Goal Id).
        =======================================================================
        """
        for node in self.opened:
            node.h = u_grid.manhattan_distance(self.grid, node.idd, goal)
            node.f = node.g + node.h    
    
    
"""
===============================================================================
===============================================================================
============          Tester          =========================================
===============================================================================
===============================================================================
"""
from pathlib import Path
path_parent = str(Path(Path(__file__).parent).parent)

import sys
sys.path.append(path_parent + '\\f__utils')
import u_tester

def tester():
    
    def tester_sorted_goals():
        
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {3,2,5,8}
        kastar_h = KAStar_H(grid, start, goals)
        goals_test = kastar_h._sorted_goals()
        goals_true = [3,2,5,8]
        p0 = goals_test == goals_true
        
        u_tester.run([p0])
        
        
    def tester_update_opened():
        
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {2}
        kastar_h = KAStar_H(grid, start, goals)
        goal_new = 8
        kastar_h._update_opened(goal_new)
        p0 = True
        for node in kastar_h.opened:
            p0 = node.h == u_grid.manhattan_distance(grid,node.idd,goal_new)
            if not p0: break
        
        u_tester.run([p0])
        
        
    def tester_run():
        
        import random
        from c_kastar import KAStar
        from c_node import Node
        
        for i in range(1000):
            
            grid = u_grid.gen_obstacles_grid(10,30)
            idds = u_grid.get_valid_idds(grid)
            random.shuffle(idds)
            start = idds[0]
            goals = idds[1:4]
            kastar = KAStar(grid, start, goals)
            kastar.run()
            kastar_h = KAStar_H(grid, start, goals)
            kastar_h.run()
            if not kastar_h.has_solution: continue
        
            p0 = True
            f_max = 0
            for goal in goals:
                node_goal = Node(goal)
                node_goal = u_set.get(kastar_h.closed,node_goal)
                f_max = max(f_max,node_goal.f)
            for node in kastar_h.closed:
                if node.f > f_max:
                    p0 = False
                    break
                
            p1 = True
            for goal in goals:
                p1 = len(kastar.get_path(goal)) == len(kastar_h.get_path(goal))
                if not p1: break
            
            if not p0 or not p1:
                break

        u_tester.run([p0,p1])
        
        
    u_tester.print_start(__file__)
    tester_sorted_goals()
    tester_update_opened()
    tester_run()
    u_tester.print_finish(__file__)
    

if __name__ == '__main__':
    tester()
    
 