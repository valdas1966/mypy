from f_core.mixins.has_name import HasName
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class HeatMap(HasName):
    """
    ============================================================================
     Heat Map Chart Class.
    ============================================================================
    """

    _WIDTH: int = 8
    _HEIGHT: int = 6 
    _DPI: int = 600
    _SIZE_TITLE: int = 16

    def __init__(self,
                 pivot: pd.DataFrame,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        self._pivot = pivot
        self._fill_missing_columns()
        self._set_params()

    def show(self) -> None:
        """
        ========================================================================
         Show the Heat Map on the Screen.
        ========================================================================
        """
        plt.tight_layout()
        plt.show()

    def _fill_missing_columns(self) -> None:
        """
        ========================================================================
        Fill missing x columns with zeros to ensure continuous range.
        ========================================================================
        """
        x_min = self._pivot.columns.min()
        x_max = self._pivot.columns.max()
        all_x = range(x_min, x_max + 1)
        
        # Add missing columns with NaN values
        for x in all_x:
            if x not in self._pivot.columns:
                self._pivot[x] = np.nan
                
        # Sort columns numerically
        self._pivot = self._pivot.reindex(sorted(self._pivot.columns), axis=1)

    def _set_params(self) -> None:
        """
        ========================================================================
         Run Private-Methods.
        ========================================================================
        """
        self._set_size()
        self._set_dpi()
        self._set_title()
        self._set_heatmap()

    def _set_size(self) -> None:
        """
        ========================================================================
         Set Heat Map Size.
        ========================================================================
        """
        plt.figure(figsize=(self._WIDTH, self._HEIGHT))

    def _set_dpi(self) -> None:
        """
        ========================================================================
         Set Heat Map DPI (Dots Per Image).
        ========================================================================
        """
        plt.gcf().set_dpi(val=self._DPI)

    def _set_title(self) -> None:
        """
        ========================================================================
         Set Heat Map Title.
        ========================================================================
        """
        if self.name:
            plt.title(label=self.name,
                     fontweight='bold',
                     fontsize=self._SIZE_TITLE)

    def _set_heatmap(self) -> None:
        """
        ========================================================================
         Set Heat Map Parameters.
        ========================================================================
        """
        # Create heatmap using imshow
        heatmap = plt.imshow(self._pivot,
                             cmap='RdYlGn_r',  # Red to Green colormap (reversed)
                             aspect='auto')
        
        # Add colorbar
        plt.colorbar(heatmap, label='Volume')

        # Set labels
        plt.xlabel('X', fontweight='bold')
        plt.ylabel('Y', fontweight='bold')

        # Set ticks
        plt.xticks(range(len(self._pivot.columns)), 
                   self._pivot.columns, 
                   fontweight='bold')
        plt.yticks(range(len(self._pivot.index)), 
                   self._pivot.index, 
                   fontweight='bold')

        # Add volume labels to each cell
        for i in range(len(self._pivot.index)):
            for j in range(len(self._pivot.columns)):
                value = self._pivot.iloc[i, j]
                plt.text(j, i, f'{value:.0f}', 
                         ha='center', va='center',
                         color='black', fontweight='bold')
