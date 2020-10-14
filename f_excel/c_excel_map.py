from f_excel.c_excel import Excel


class ExcelMap(Excel):

    def set_block(self, row, column):
        """
        ========================================================================
         Description: S
        :param row:
        :param column:
        :return:
        """
        self.set_value(row, column, value=str())
        self.set_color_back(row, column, color='BLACK')
        self.set_border(row, column, style='thick')

    def set_blocks(self, rf, rl, cf, cl):
        for row in range(rf, rl+1):
            for column in range(cf, cl+1):
                self.set_block(row, column)