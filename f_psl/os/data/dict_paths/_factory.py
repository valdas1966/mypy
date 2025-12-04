from f_psl.os.data.dict_paths.main import DictPaths, ListPaths


class Factory:
    """
    ============================================================================
     Factory for creating DictPaths objects.
    ============================================================================
    """
    
    @staticmethod
    def ab() -> DictPaths:
        """
        ========================================================================
         Return a DictPaths {'a': ListPaths(['a']), 'b': ListPaths(['b'])}
        ========================================================================
        """
        d = DictPaths()
        paths = ListPaths.Factory.ab()
        for path in paths:
            d[path].append(path)
        return d