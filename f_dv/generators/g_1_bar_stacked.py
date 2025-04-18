from f_dv.i_1_bar_stacked import BarStacked, RGB


class GBarStacked:
    """
    ============================================================================
     Generator for BarStacked charts.
    ============================================================================
    """

    @staticmethod
    def traffic_light() -> BarStacked:
        """
        ========================================================================
         Generate a traffic light chart.
        ========================================================================
        """
        x = ['Group 1', 'Group 2', 'Group 3']
        y = [[10, 20, 70], [30, 25, 45], [20, 30, 50]]
        z = 135
        d_stack = {'Red': RGB('LIGHT_RED'),
                   'Yellow': RGB('LIGHT_YELLOW'),
                   'Green': RGB('LIGHT_GREEN')}
        chart = BarStacked(x=x,
                           y=y,
                           d_stack=d_stack,
                           is_pct=True)
        return chart


bar = GBarStacked.traffic_light()
bar.show()
