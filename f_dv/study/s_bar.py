from f_dv.i_1_bar import Bar, RGB


def study_1() -> None:
    """
    ========================================================================
     Study Bar Chart.
    ========================================================================
    """
    vals = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    x = [str(x) for x in range(len(vals))]
    y = vals
    bar = Bar(x=x, y=y)
    bar.show()


study_1()
