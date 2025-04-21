from f_core.mixins.has_name import HasName
import matplotlib.pyplot as plt
from abc import abstractmethod


class Chart(HasName):
    """
    ============================================================================
     Chart Class.
    ============================================================================
    """
    
    _WIDTH: int = 4
    _HEIGHT: int = 3
    _DPI: int = 600
    _SIZE_TITLE: int = 16
    
    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)

    def show(self) -> None:
        """
        ========================================================================
         Show the Bar Chart on the Screen.
        ========================================================================
        """
        self._set_params()
        plt.show()

    def save(self, path: str) -> None:
        """
        ========================================================================
         Save the Bar Chart.
        ========================================================================
        """
        plt.clf()
        self._set_params()
        plt.savefig(path, dpi=self._DPI, bbox_inches='tight')
        plt.close()

    def _set_params(self) -> None:
        """
        ========================================================================
         Run Private-Methods.
        ========================================================================
        """
        self._set_size()
        self._set_dpi()
        self._set_title()
        self._set_chart()

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
                      fontsize=self._SIZE_TITLE)

    @abstractmethod
    def _set_chart(self) -> None:
        """
        ========================================================================
         Set Chart.
        ========================================================================
        """
        pass
