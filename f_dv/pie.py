import matplotlib.pyplot as plt
from f_core.mixins.has_name import HasName


class Pie(HasName):
    """
    ============================================================================
     Pie-Chart Class.
    ============================================================================
    """

    _WIDTH: int = 10
    _HEIGHT: int = 8
    _DPI: int = 1200
    _SIZE_NAME: int = 16

    def __init__(self,
                 labels: list[str],
                 pcts: list[int],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self._labels = labels
        self._pcts = pcts
        self._set_params()

    def show(self) -> None:
        """
        ========================================================================
         Show the Pie-Chart on the Screen.
        ========================================================================
        """
        plt.axis('equal')
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
        self._set_pie()
    def _set_size(self) -> None:
        """
        ========================================================================
         Set Pie-Chart Size.
        ========================================================================
        """
        figsize = (self._WIDTH, self._HEIGHT)
        plt.figure(figsize=figsize)

    def _set_dpi(self) -> None:
        """
        ========================================================================
         Set Pie-Chart DPI (Dots Per Image).
        ========================================================================
        """
        plt.gcf().set_dpi(val=self._DPI)

    def _set_title(self) -> None:
        """
        ========================================================================
         Set Pie-Chart Title.
        ========================================================================
        """
        if self.name:
            plt.title(label=self.name,
                      fontweight='bold',
                      fontsize=self._SIZE_NAME)

    def _set_pie(self) -> None:
        """
        ========================================================================
         Set Pie-Chart Parameters.
        ========================================================================
        """
        plt.pie(self._pcts,
                labels=self._labels,
                startangle=140,
                textprops={'fontweight': 'bold'},
                autopct=lambda pct: f'{int(round(pct)):d}%')
