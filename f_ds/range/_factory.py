from f_ds.range.main import Range


class Factory:
    """
    ============================================================================
     Factory for Range.
    ============================================================================
    """

    @staticmethod
    def without_header(rows: int = 3, cols: int = 3) -> Range:
        """
        ====================================================================
         Generate a Range with numbered values.
        ====================================================================
        """
        data = [[f'r{r}c{c}' for c in range(cols)]
                for r in range(rows)]
        return Range(data=data)

    @staticmethod
    def with_header() -> Range:
        """
        ====================================================================
         Generate a Range with a header row.
        ====================================================================
        """
        return Range(data=[['Name', 'Age', 'City'],
                           ['Alice', '30', 'NY'],
                           ['Bob', '25', 'LA']])
