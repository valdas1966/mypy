from f_ds.groups.group import Group


class GenGroup:

    @staticmethod
    def gen_3_items() -> Group:
        """
        ========================================================================
        
        ========================================================================
        """
        return Group(data=range(3, 6))
