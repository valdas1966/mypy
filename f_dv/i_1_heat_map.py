from f_dv.i_0_chart import Chart
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np


class HeatMap(Chart):
    """
    ============================================================================
     Heat Map Chart Class.
    ============================================================================
    """

    def __init__(self,
                 pivot: pd.DataFrame,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._pivot = pivot
        Chart.__init__(self, name=name)

    def _set_chart(self) -> None:
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
                
        plt.tight_layout()
