from f_dv.i_1_bar_grouped import BarGrouped, RGB


class GBarGrouped:

    @staticmethod
    def traffic_light() -> BarGrouped:
        """
        ========================================================================
        
        ========================================================================
        """
        labels = ['Red', 'Yellow', 'Green']
        grouped_values = [[10, 30, 60], [20, 40, 40], [30, 30, 40]]
        group_names = ['Group 1', 'Group 2', 'Group 3']
        group_colors = [RGB.from_int(r=255, g=0, b=0),
                        RGB.from_int(r=255, g=255, b=0),
                        RGB.from_int(r=0, g=255, b=0)]
        name_labels = 'Traffic Light'
        name_values = 'Percentage'
        chart = BarGrouped(labels=labels,
                           grouped_values=grouped_values,
                           group_names=group_names,
                           group_colors=group_colors,
                           name_labels=name_labels,
                           name_values=name_values)
        return chart


bar = GBarGrouped.traffic_light()
bar.show()