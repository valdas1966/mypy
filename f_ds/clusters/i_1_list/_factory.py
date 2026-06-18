from f_ds.clusters.i_1_list.main import ClusterList


class Factory:
    """
    ============================================================================
     Factory-Class for ClusterList.
    ============================================================================
    """

    @staticmethod
    def a() -> ClusterList:
        """
        ========================================================================
         Canonical small ClusterList: members [1, 2, 3], name 'K',
         representative 1.
        ========================================================================
        """
        return ClusterList(members=[1, 2, 3], name='K', representative=1)

    @staticmethod
    def b() -> ClusterList:
        """
        ========================================================================
         A second ClusterList with no representative: members [4, 5].
        ========================================================================
        """
        return ClusterList(members=[4, 5], name='L')
