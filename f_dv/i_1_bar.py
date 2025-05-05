import math
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from f_color.factories.f_rgb import FactoryRGB, RGB
from f_dv.i_0_chart import Chart


class Bar(Chart):
    """
    ============================================================================
     Bar Chart Class.
    ============================================================================
    """

    def __init__(self,
                 x: list[str],  # X-Axis Labels
                 y: list[int],  # Y-Axis Values
                 name_x: str = str(),  # X-Axis Name
                 name_y: str = str(),  # Y-Axis Name
                 is_y_pct: bool = False,  # Is Y-Axis holds percentages
                 rgb_bars: list[RGB] = None,  # RGBs to color the bars  
                 name: str = None) -> None:  # Name of the chart
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._x = x
        self._y = y
        self._name_x = name_x
        self._name_y = name_y
        self._is_y_pct = is_y_pct
        self._rgb_bars = rgb_bars if rgb_bars else self._set_rgb_bars_traffic()
        Chart.__init__(self, name=name)

    def _set_rgb_bars_gradient(self) -> list[RGB]:
        """
        ========================================================================
         Set the RGBs for the bars.
        ========================================================================
        """
        # Get the min and max values of the y-axis
        y_min, y_max = min(self._y), max(self._y)
        # Set the range of the y-axis (by avoiding divide-by-zero)
        range_y = y_max - y_min if y_max != y_min else 1.0

        # Start and Finish RGBs
        rgb_a, rgb_b = RGB(name='GREEN'), RGB(name='RED')
        # Gradient RGBs Map (0-99 sequential RGBs)
        gradient: list[RGB] = FactoryRGB.gradient(a=rgb_a, b=rgb_b, n=100)
        
        # Initialize the list of RGBs to return
        rgbs: list[RGB] = list()
        # Assign color to each bar based on normalized value
        for val in self._y:
            if math.isnan(val):
                rgbs.append(RGB(r=0, g=0, b=0))  # Placeholder color, will be skipped in rendering
                continue
            # Normalize the Y-Value to [0,1] based on Range-Y 
            normalized = (val - y_min) / range_y
            # Get the index of the color in the gradient
            # The multiplication by 99 and not by 100:
            #  because the gradient is 0-99 (100 values)
            index = int(normalized * 99)
            # Get the color from the gradient
            rgb = gradient[index]
            # Add the color to the list
            rgbs.append(rgb)

        # Return the list of the Bars RGBs
        return rgbs
    
    def _set_rgb_bars_traffic(self) -> list[RGB]:
        """
        ========================================================================
         Set the RGBs for the bars.
        ========================================================================
        """
        # Get the min and max values of the y-axis
        y_min, y_max = min(self._y), max(self._y)
        # Set the range of the y-axis (by avoiding divide-by-zero)
        y_range = y_max - y_min
        if not y_range:
            y_range = 1

        # Gradient Stops' RGBs
        stops = [RGB(name='MATTE_GREEN'),
                 RGB(name='MATTE_YELLOW'),
                 RGB(name='MATTE_RED')]
        # Gradient size
        n = 20

        # Create the gradient
        gradient = FactoryRGB.gradient_multi(stops=stops, n=n)

        # Initialize the list of RGBs to return
        rgbs: list[RGB] = list()
        # Assign color to each bar based on normalized value
        for val in self._y:
            # If the value is NaN, add a placeholder color
            if math.isnan(val):
                # Placeholder color, will be skipped in rendering
                rgbs.append(RGB(r=0, g=0, b=0))  
                continue
            # Get the index of the color in the gradient
            normalized_pct = (val - y_min) / y_range * 100
            index = min(int(normalized_pct // (100 / n)), n - 1)
            # Get the color from the gradient
            rgb = gradient[index]
            # Add the color to the list
            rgbs.append(rgb)

        # Return the list of the Bars RGBs
        return rgbs


    def _set_size(self) -> None:
        """
        ========================================================================
        Dynamically set chart size based on number of bars.
        ========================================================================
        """
        # Estimate width based on number of labels (bars)
        bar_count = len(self._x)
        # adjust width of the chart
        width = max(2, bar_count * 1)
        # keep height fixed  
        height = self._HEIGHT
        # Set the figure size
        plt.figure(figsize=(width, height))

    def _set_chart(self) -> None:
        """
        ========================================================================
         Set Bar Chart Parameters.
        ========================================================================
        """
        # Set the chart parameters tightly (relatively to the bars)
        # Without this line -> the chart will be unnecessarily wide
        plt.tight_layout()
        
        # Convert RGB objects to matplotlib color tuples
        colors = [rgb.to_tuple() for rgb in self._rgb_bars]
        
        # Create the bar chart with the gradient colors
        bars = plt.bar(self._x, self._y, color=colors, width=0.5)

        # Add labels and values on top of the bars, in bold
        for bar in bars:
            height = bar.get_height()
            if height != height:
                height = 0
            label = f'{int(height)}%' if self._is_y_pct else f'{height}'
            # Decide label position and alignment
            y = height if height >= 0 else height - 0.05 * abs(max(self._y))
            va = 'bottom' if height >= 0 else 'top'
            plt.text(bar.get_x() + bar.get_width() / 2, y,
                     label, ha='center', va=va, fontweight='bold',
                     fontsize=16, color='white')

        plt.xlabel(xlabel=self._name_x, fontweight='bold', fontsize=16)
        plt.ylabel(ylabel=self._name_y, fontweight='bold', fontsize=16)
        plt.xticks(self._x, fontweight='bold', fontsize=16)
        plt.yticks(plt.yticks()[0], fontweight='bold', fontsize=16)
        
        # If is_y_pct is True, format the y-axis labels as percentages
        if self._is_y_pct:
            def to_percent(y, _):
                return f'{int(y)}%'
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

        # Set the background color of the chart
        plt.gca().set_facecolor('#2C2C2C')

        # Set the y-axis limit to 15% extra headroom
        max_height = max(self._y)
        plt.ylim(top=max_height * 1.15)
