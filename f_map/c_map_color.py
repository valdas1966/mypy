
class MapColor:

    cats = {'EMPTY': 0, 'BLOCK': -1, 'GOAL_NEAR': 1, 'GOAL_FAR': 2, 'START': 3,
            'LOOKUP': 4, 'FORWARD': 5, 'BACKWARD': 6, 'MUTUAL': 7}

    def __init__(self, map, start_goals, forward, backward):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. map : Map
            2. start_goals : dict {'start', 'goal_near', 'goal_far'}
            3. forward : dict {'closed_near', 'closed_far'}
            4. backward : set
        ========================================================================
        """
        self.map = map
        self.map.zfill()
        idds_lookup = {node.idd for node in forward['closed_near']}
        idds_forward = {node.idd for node in forward['closed_far']}
        idds_backward = {node.idd for node in backward}
        idds_mutual = set.intersection(idds_forward, idds_backward)
        idds_forward = idds_forward - idds_mutual
        idds_backward = idds_backward - idds_mutual
        self.__set_idds(idds_forward, 'FORWARD')
        self.__set_idds(idds_backward, 'BACKWARD')
        self.__set_idds(idds_mutual, 'MUTUAL')
        self.__set_idds(idds_lookup, 'LOOKUP')
        self.__set_start_goals(start_goals)

    def draw(self, xl, row_start, col_start):
        for i in range(self.map.rows):
            for j in range(self.map.cols):
                row = row_start + i
                column = col_start + j
                value = str()
                cat = self.map.grid[i][j]
                if cat == self.cats['START']:
                    value = 'S'
                elif cat == self.cats['GOAL_NEAR']:
                    value = 'G1'
                elif cat == self.cats['GOAL_FAR']:
                    value = 'G2'
                xl.write_value(row, column, value)
                color = 'WHITE'
                if cat == self.cats['LOOKUP']:
                    color = 'TRANSPARENT'
                elif cat == self.cats['FORWARD']:
                    color = 'YELLOW'
                elif cat == self.cats['BACKWARD']:
                    color = 'GREEN'
                elif cat == self.cats['MUTUAL']:
                    color = 'RED'
                elif cat == self.cats['BLOCK']:
                    color = 'BLACK'
                xl.fill_cell(row, column, color)

    def __set_start_goals(self, start_goals):
        """
        ========================================================================
         Description: Set Start and Goals nodes in forward and backward maps.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. start_goals : dict
        ========================================================================
        """
        start = start_goals['start']
        goal_near = start_goals['goal_near']
        goal_far = start_goals['goal_far']
        self.map_forward.set_value(idd=start, value=self.cats['START'])
        self.map_forward.set_value(idd=goal_near, value=self.cats['GOAL_NEAR'])
        self.map_forward.set_value(idd=goal_far, value=self.cats['GOAL_FAR'])
        self.map_backward.set_value(idd=start, value=self.cats['START'])
        self.map_backward.set_value(idd=goal_near, value=self.cats['GOAL_NEAR'])
        self.map_backward.set_value(idd=goal_far, value=self.cats['GOAL_FAR'])

    def __set_idds(self, idds, cat):
        for idd in idds:
            self.map.set_value(idd=idd, value=self.cats[cat])

