from f_ds.groups.group import Group


class GenGroup:

    @staticmethod
    def gen_3_items() -> Group:
        """
        ========================================================================
        
        ========================================================================
        """
        return Group(data=range(3, 6))
    
    @staticmethod
    def five() -> Group:
        """
        ========================================================================
         Generate a group of 5 numbers from 1 to 5.
        ========================================================================
        """
        return Group(data=range(1, 6))

