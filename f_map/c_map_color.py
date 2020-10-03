class MapColor:

    CATS = {'EMPTY': 0, 'BLOCK': -1, 'GOAL_NEAR': 1, 'GOAL_FAR': 2, 'START': 3,
            'LOOKUP': 4, 'FORWARD': 5, 'BACKWARD': 6}

    def __init__(self, map):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. map : f_map.c_map
        ========================================================================
        """
        self.map = map
        self.__set_empty()

    def set_group(self, group, cat):
        """
        ========================================================================
         Description: Set Enum to the Group of Nodes by their Category.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. group : set of Nodes.
            2. cat : str (Category of Nodes).
        ========================================================================
        """
        for node in group:
            val = self.CATS[cat]
            idd = node.idd
            self.map.set_value(val, idd)

    def set_start_goals(self, start, goal_near, goal_far):
        """
        ========================================================================
         Description: Set Enum CATS for Start and Goals Nodes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. start : int (Start Node's Idd).
            2. goal_near : int (Goal Near Node's Idd).
            3. goal_far : int (Goal Far Node's Idd),
        ========================================================================
        """
        self.map.set_value(self.CATS['START'], idd=start)
        self.map.set_value(self.CATS['GOAL_NEAR'], idd=goal_near)
        self.map.set_value(self.CATS['GOAL_FAR'], idd=goal_far)

    def __set_empty(self):
        """
        ========================================================================
         Description: Set not blocked Nodes to be EMPTY.
        ========================================================================
        """
        for row in range(self.map.rows):
            for col in range(self.map.cols):
                if self.map.grid[row][col] > self.CATS['EMPTY']:
                    self.map.grid[row][col] = self.CATS['EMPTY']
