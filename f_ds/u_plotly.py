import plotly.express as px


def bar(df, col_x, col_y, title):
    """
    ============================================================================
     Description: Plot Plotly Interactive Bar
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame.
        2. col_x : str (Column Name of X-Axis).
        3. col_y : str (Column Name for Y-Axis).
        4. title : str (Title of the Bar).
    ============================================================================
    """
    fig = px.bar(df, x=col_x, y=col_y, hover_data=[col_x, col_y], color=col_y,
                 height=400, title=title)
    fig.show()
