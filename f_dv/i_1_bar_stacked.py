import numpy as np
from f_color.rgb import RGB
from f_dv.i_0_chart import Chart
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt


class BarStacked(Chart):
    """
    ============================================================================
     Stacked Bar Chart — one bar per label, divided into segments
       (e.g., green/yellow/red).
    ============================================================================
    """

    def __init__(self,
                 x: list[str],
                 y: list[list[int]],
                 d_stack: dict[str, RGB],
                 name_labels: str = '',
                 name_values: str = '',
                 is_pct: bool = False,
                 name: str = None) -> None:
        """
        ========================================================================
        labels:        ['A', 'B', 'C']
        values:        [[g1,e1,l1], [g2,e2,l2], [g3,e3,l3]]
        d_stack:       {'wins': RGB.RED}
        ========================================================================
        """
        self._x = x
        self._y = y
        self._d_stack = d_stack
        self._is_pct = is_pct
        self._name_labels = name_labels
        self._name_values = name_values
        Chart.__init__(self, name=name)

    def _set_chart(self) -> None:
        """
        ========================================================================
         Set the chart.
        ========================================================================
        """
        plt.tight_layout()

        num_bars = len(self._x)
        x = np.arange(num_bars)

        # Transpose values: stacks[i] = all values for segment i
        values = list(map(list, zip(*self._y)))

        bottom = np.zeros(num_bars)
        bars = []

        for i, label in enumerate(self._d_stack.keys()):
            bar = plt.bar(x,
                          values[i],
                          bottom=bottom,
                          color=self._d_stack[label].to_tuple(),
                          label=label)
            bottom += values[i]
            bars.append(bar)

        # Add value labels inside each segment
        for stack in bars:
            for bar in stack:
                height = bar.get_height()
                if height == 0:
                    continue
                y = bar.get_y() + height / 2
                label = f'{int(height)}%' if self._is_pct else f'{height}'
                plt.text(bar.get_x() + bar.get_width() / 2,
                         y,
                         label,
                         ha='center',
                         va='center',
                         fontsize=9,
                         fontweight='bold')

        plt.xlabel(self._name_labels, fontweight='bold')
        plt.ylabel(self._name_values, fontweight='bold')
        plt.xticks(x, self._x, fontweight='bold')
        plt.yticks(plt.yticks()[0], fontweight='bold')

        if self._is_pct:
            plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y)}%'))
            plt.ylim(top=100)

        plt.legend(
            fontsize=10,
            loc='best',
            facecolor='white',  # white background
            framealpha=1.0  # fully opaque (no transparency)
        )

        plt.gca().set_facecolor('#202020')
