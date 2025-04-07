import matplotlib.pyplot as plt
from f_dv.i_1_bar import Bar
import math


class BarMulti:

    def __init__(self, bars: list[Bar]) -> None:
        self._bars = bars
        self._rows = 1
        self._cols = 1

    def show(self) -> None:
        figsize = Bar.
        fig, axs = plt.subplots(1, len(self._bars), )

    def _set_layout(self) -> None:
        """
        ========================================================================
         Calculate the layout of SubPlots based on the number of bars.
        ========================================================================
        """
        cnt = len(self._bars)
        if cnt > 8:
            self._rows = 3
        elif cnt > 2:
            self._rows = 2
        self._cols = math.ceil(cnt / self._rows)
