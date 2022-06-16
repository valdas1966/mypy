from f_db.c_sqlite import SQLite


class LoggerDB:

    def __init__(self,
                 dir_logger: str,
                 tname: str = 'main',
                 cols: list = list()):
        assert type(dir_logger) == str, type(dir_logger)
        assert type(tname) == str, type(tname)
        assert type(cols) == list, type(cols)
        path_db = f'{dir_logger}\\logger.db'
        self.tname = tname
        self.cols = cols
        self._sql = SQLite(path_db)
        ans, msg = self._sql.open()
        if not ans:
            print(msg)
            print(path_db)
        self._create_table()

    def write(self, vals: list) -> None:
        assert type(vals) == list, type(vals)
        assert len(vals) == len(self.cols), f'{len(vals)}, {len(self.cols)}'
        ans, msg = self._sql.insert(tname=self.tname, values=vals,
                                    cols=self.cols)
        if not ans:
            print(msg)

    def close(self) -> None:
        self._sql.close()

    def _create_table(self):
        cols, msg = self._sql.cols(self.tname)
        if cols:
            if cols[1:] == self.cols:
                return
            else:
                self._sql.drop(self.tname)
        cols = ['created datetime default current_timestamp']
        cols += [f'{col} text' for col in self.cols]
        self._sql.create(self.tname, cols)
