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


def scatter(df, col_x, col_y, col_color, col_size, title):
    """
    ============================================================================
     Description: Plot Interactive Scatter
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame.
        2. col_x : str (Column Name of X-Axis).
        3. col_y : str (Column Name for Y-Axis).
        4. col_color : str (Column Name to decide the bubble color).
        5. col_size : str (Column Name to decide the bubble size).
        6. title : str (Title of the Bar).
    ============================================================================
    """
    fig = px.scatter(df, x=col_x, y=col_y, color=col_color, size=col_size,
                     hover_data=[col_size], title=title)
    fig.show()


def pie(df, col_name, col_val, title):
    """
    ============================================================================
     Description: Plot Interactive Pie.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame
        2. col_name : str
        3. col_val : str
        4. title : str
    ============================================================================
    """
    fig = px.sunburst(df, path=[col_name], values=col_val, title=title)
    fig.show()


def line(df, col_x, col_y, col_color, title):
    """
    ============================================================================
     Description: Plot Interactive Line Chart.
    ============================================================================
    Arguments:
    ----------------------------------------------------------------------------
        1. df : DataFrame.
        2. col_x : str (Column Name of X-Axis).
        3. col_y : str (Column Name for Y-Axis).
        4. col_color : str (Column Name to decide the bubble color).
        5. title : str (Title of the Bar).
    ============================================================================
    """
    fig = px.line(df, x=col_x, y=col_y, color=col_color, title=title)
    fig.show()



