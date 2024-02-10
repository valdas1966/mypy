from f_google.big_query.abc.command import Command


class Insert(Command):

    def rows(self, tname: str, li_rows: list[dict]) -> str:
        table = self._client.get_table(tname)
        errors = self._client.insert_rows_json(table, li_rows)