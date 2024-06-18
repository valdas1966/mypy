import matplotlib.pyplot as plt
from f_abstract.mixins.nameable import Nameable
from f_color.u_color import RGB, UColor


class Bar(Nameable):
    """
    ============================================================================
     Bar Chart Class.
    ============================================================================
    """

    _WIDTH: int = 12
    _HEIGHT: int = 8
    _DPI: int = 1200
    _SIZE_NAME: int = 16

    def __init__(self,
                 labels: list[str],
                 values: list[int],
                 name_labels: str = str(),
                 name_values: str = str(),
                 rgbs: list[RGB] = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        self._labels = labels
        self._values = values
        self._name_labels = name_labels
        self._name_values = name_values
        if not rgbs:
            rgbs = UColor.to_gradients(RGB('my_cyan'), RGB('black'), len(labels))
        self._rgbs = rgbs
        self._set_params()

    def show(self) -> None:
        """
        ========================================================================
         Show the Bar Chart on the Screen.
        ========================================================================
        """
        plt.tight_layout()
        plt.show()

    def _set_params(self) -> None:
        """
        ========================================================================
         Run Private-Methods.
        ========================================================================
        """
        self._set_size()
        self._set_dpi()
        self._set_title()
        self._set_bar()

    def _set_size(self) -> None:
        """
        ========================================================================
         Set Bar Chart Size.
        ========================================================================
        """
        plt.figure(figsize=(self._WIDTH, self._HEIGHT))

    def _set_dpi(self) -> None:
        """
        ========================================================================
         Set Bar Chart DPI (Dots Per Image).
        ========================================================================
        """
        plt.gcf().set_dpi(val=self._DPI)

    def _set_title(self) -> None:
        """
        ========================================================================
         Set Bar Chart Title.
        ========================================================================
        """
        if self.name:
            plt.title(label=self.name,
                      fontweight='bold',
                      fontsize=self._SIZE_NAME)

    def _set_bar(self) -> None:
        """
        ========================================================================
         Set Bar Chart Parameters.
        ========================================================================
        """
        # Convert RGB objects to matplotlib color tuples
        colors = [rgb.to_tuple() for rgb in self._rgbs]

        # Create the bar chart with the gradient colors
        bars = plt.bar(self._labels, self._values, color=colors)

        # Add labels and values on top of the bars, in bold
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     f"{height}", ha='center', va='bottom', fontweight='bold')
        plt.xlabel(xlabel=self._name_labels, fontweight='bold')
        plt.ylabel(ylabel=self._name_values, fontweight='bold')
        plt.xticks(self._labels, fontweight='bold')
        plt.yticks(plt.yticks()[0], fontweight='bold')
