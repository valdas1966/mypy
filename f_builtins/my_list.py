
class MyList(list):

    def replace_items(self, d: dict) -> None:
        """
        ========================================================================
         Description: Replace Items by a given Dictionary {what: into}.
        ========================================================================
        """
        for i, item in enumerate(self):
            if item in d:
                self[i] = d[item]


