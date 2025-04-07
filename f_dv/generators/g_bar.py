from f_dv.i_1_bar import Bar


class GBar:
    """
    ============================================================================
     Bar Chart Generator Class.
    ============================================================================
    """

    @staticmethod
    def hand() -> Bar:
        """
        ========================================================================
         Generate Bar Chart.
        ========================================================================
        """
        labels = [1, 2, 3, 4, 5]
        values = [1, 2, 3, 4, 5]
        name_labels = 'Labels'
        name_values = 'Values'
        title = 'Bar Chart'
        return Bar(labels=labels,
                   values=values,
                   name_labels=name_labels,
                   name_values=name_values,
                   name=title)


bar = GBar.hand()
bar.show()