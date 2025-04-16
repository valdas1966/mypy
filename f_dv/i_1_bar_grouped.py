from f_dv.i_0_chart import Chart
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
from f_color.u_color import RGB


class BarGrouped(Chart):
    """
    ============================================================================
     Grouped Bar Chart Class — for multiple values per category.
    ============================================================================
    """

    def __init__(self,
                 labels: list[str],
                 grouped_values: list[list[int]],
                 group_names: list[str],
                 group_colors: list[RGB],
                 name_labels: str = '',
                 name_values: str = '',
                 is_pct: bool = False,
                 name: str = None) -> None:
        """
        ========================================================================
         labels: categories on x-axis (e.g., ['A', 'B', 'C'])
         grouped_values: list of value-lists per label (e.g., [[1,2,3], [4,5,6]])
         group_names: names for each group (e.g., ['greater', 'equal', 'less'])
         group_colors: list of RGB colors per group
        ========================================================================
        """
        self._labels = labels
        self._grouped_values = grouped_values
        self._group_names = group_names
        self._group_colors = [rgb.to_tuple() for rgb in group_colors]
        self._name_labels = name_labels
        self._name_values = name_values
        self._is_pct = is_pct
        Chart.__init__(self, name=name)

    def _set_chart(self) -> None:
        import numpy as np
        plt.tight_layout()

        num_groups = len(self._group_names)
        num_bars = len(self._labels)
        bar_width = 0.8 / num_groups
        x = np.arange(num_bars)

        # Draw each group of bars
        for i in range(num_groups):
            values = [group[i] for group in self._grouped_values]
            bars = plt.bar(x + i * bar_width, values,
                           width=bar_width,
                           label=self._group_names[i],
                           color=self._group_colors[i])

            for bar in bars:
                height = bar.get_height()
                label = f'{int(height)}%' if self._is_pct else f'{height}'
                y = height if height >= 0 else height - 0.05 * abs(max(values))
                va = 'bottom' if height >= 0 else 'top'
                plt.text(bar.get_x() + bar.get_width() / 2, y,
                         label, ha='center', va=va, fontweight='bold')

        plt.xlabel(self._name_labels, fontweight='bold')
        plt.ylabel(self._name_values, fontweight='bold')
        plt.xticks(x + bar_width * (num_groups - 1) / 2, self._labels, fontweight='bold')
        plt.yticks(plt.yticks()[0], fontweight='bold')

        if self._is_pct:
            plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y)}%'))

        plt.legend(fontsize=10, loc='best')
