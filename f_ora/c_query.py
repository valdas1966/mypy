class Query:

    def __init__(self):
        """
        ===================================================================
         Description: Constructor.
        ===================================================================
        """
        self.Select = str()
        self.From = str()
        self.On = str()
        self.Where = str()
        self.Groupby = str()
        self.Having = str()
        self.Orderby = str()

    def __str__(self):
        """
        ===================================================================
         Description: Return string-representation of the Query.
        ===================================================================
         Return: str (String-Representation of the Query).
        ===================================================================
        """
        self._set_on()
        self._set_where()
        self._set_groupby()
        self._set_having()
        self._set_orderby()
        adds = self.On + self.Where + self.Groupby + self.Having + self.Orderby
        query = 'select {0} from {1}{2}'
        return query.format(self.Select, self.From, adds)


    def _set_on(self):
        if self.On and not self.On.startswith(' '):
            self.On = ' on {0}'.format(self.On)

    def _set_where(self):
        if self.Where and not self.Where.startswith(' '):
            self.Where = ' where {0}'.format(self.Where)

    def _set_groupby(self):
        res = ' group by '
        funcs = ['min', 'max', 'count', 'avg']
        count_aggregate_functions = 0
        count_single_cols = 0
        cols = self.Select.replace('select', '').strip().split(',')
        for col in cols:
            col = col.strip()
            if any(f in col for f in funcs):
                count_aggregate_functions += 1
            else:
                col = col.split()[0]
                if count_single_cols:
                    res += ', ' + col
                else:
                    res += col
                count_single_cols += 1
        if count_aggregate_functions and count_single_cols:
            self.Groupby = res

    def _set_having(self):
        if self.Having and not self.Having.startswith(' '):
            self.Having = ' having {0}'.format(self.Having)

    def _set_orderby(self):
        if self.Orderby:
            if not self.Orderby.startswith(' '):
                self.Orderby = ' order by {0}'.format(self.Orderby)
        else:
            self.Orderby = ' order by 1'
