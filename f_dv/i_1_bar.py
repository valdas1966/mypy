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
        self._labels = [str(label) for label in labels]
        self._values = values
        self._name_labels = name_labels
        self._name_values = name_values
        self._is_pct = is_pct
        if not rgbs:
            rgbs = UColor.to_gradients(RGB('MY_CYAN'), RGB('black'), len(labels))
        self._rgbs = rgbs
        Chart.__init__(self, name=name)

    def _set_size(self) -> None:
        """
        ========================================================================
        Dynamically set chart size based on number of bars.
        ========================================================================
        """
        # Estimate width based on number of labels (bars)
        bar_count = len(self._labels)
        width = max(2, bar_count * 1)  # adjust multiplier as needed
        height = self._HEIGHT  # keep height fixed
        plt.figure(figsize=(width, height))

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
        bars = plt.bar(self._labels, self._values, color=colors, width=0.5)

        # Add labels and values on top of the bars, in bold
        for bar in bars:
            height = bar.get_height()
            if height != height:
                height = 0
            label = f'{int(height)}%' if self._is_pct else f'{height}'
            # Decide label position and alignment
            y = height if height >= 0 else height - 0.05 * abs(max(self._values))
            va = 'bottom' if height >= 0 else 'top'
            plt.text(bar.get_x() + bar.get_width() / 2, y,
                     label, ha='center', va=va, fontweight='bold', fontsize=16)

        plt.xlabel(xlabel=self._name_labels, fontweight='bold', fontsize=16)
        plt.ylabel(ylabel=self._name_values, fontweight='bold', fontsize=16)
        plt.xticks(self._labels, fontweight='bold', fontsize=16)
        plt.yticks(plt.yticks()[0], fontweight='bold', fontsize=16)
        
        # If is_pct is True, format the y-axis labels as percentages
        if self._is_pct:
            def to_percent(y, _):
                return f'{int(y)}%'
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

        plt.gca().set_facecolor('#F2F2F2')

        max_height = max(self._values)
        plt.ylim(top=max_height * 1.15)  # adds 15% extra headroom

