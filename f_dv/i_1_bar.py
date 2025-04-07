import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from f_color.u_color import RGB, UColor
from f_dv.i_0_chart import Chart


class Bar(Chart):
    """
    ============================================================================
     Bar Chart Class.
    ============================================================================
    """

    def __init__(self,
                 labels: list[str],
                 values: list[int],
                 name_labels: str = str(),
                 name_values: str = str(),
                 is_pct: bool = False,
                 rgbs: list[RGB] = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._labels = labels
        self._values = values
        self._name_labels = name_labels
        self._name_values = name_values
        self._is_pct = is_pct
        if not rgbs:
            rgbs = UColor.to_gradients(RGB('my_cyan'), RGB('black'), len(labels))
        self._rgbs = rgbs
        Chart.__init__(self, name=name)

    def _set_chart(self) -> None:
        """
        ========================================================================
         Set Bar Chart Parameters.
        ========================================================================
        """
        plt.tight_layout()

        # Convert RGB objects to matplotlib color tuples
        colors = [rgb.to_tuple() for rgb in self._rgbs]

        # Create the bar chart with the gradient colors
        bars = plt.bar(self._labels, self._values, color=colors)

        # Add labels and values on top of the bars, in bold
        for bar in bars:
            height = bar.get_height()
            label = f'{int(height)}%' if self._is_pct else f'{height}'
            # Decide label position and alignment
            y = height if height >= 0 else height - 0.05 * abs(max(self._values))
            va = 'bottom' if height >= 0 else 'top'
            plt.text(bar.get_x() + bar.get_width() / 2, y,
                     label, ha='center', va=va, fontweight='bold')

        
        plt.xlabel(xlabel=self._name_labels, fontweight='bold')
        plt.ylabel(ylabel=self._name_values, fontweight='bold')
        plt.xticks(self._labels, fontweight='bold')
        plt.yticks(plt.yticks()[0], fontweight='bold')

        # If is_pct is True, format the y-axis labels as percentages
        if self._is_pct:
            def to_percent(y, _):
                return f'{int(y)}%'
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

        """
        # Increase the white area between the highest bar and the top border
        max_height = max(self._values)
        plt.ylim(top=max_height * 2)
        """
