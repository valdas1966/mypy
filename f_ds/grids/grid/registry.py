from f_ds.grids import GridMap as Grid
from typing import Callable


class GridRegistry:
    """
    ============================================================================
     Lazy-loading registry with shared cache for GridMap objects.
    ============================================================================
    """

    # Setup once at the start of your experiment
    # GridRegistry.set_loader(lambda name: GridMap.From.file_map(name))

    # Used to load the GridMap from a file
    _loader: Callable[[str], Grid] = None
    # Cache of loaded GridMap objects (to save time and memory on loading the
    #  same grid multiple times)
    _cache: dict[str, Grid] = {}

    @classmethod
    def set_loader(cls, loader: Callable[[str], Grid]) -> None:
        """
        ========================================================================
         1. Set the loader for the GridRegistry.
         2. Used to load the Grid from a file when the grid is not in the cache.
        ========================================================================
        """
        cls._loader = loader

    @classmethod
    def get(cls, name: str) -> Grid:
        """
        ========================================================================
         Get the GridMap from the cache or load it from the loader.
        ========================================================================
        """
        if name not in cls._cache:
            if cls._loader is None:
                raise RuntimeError("GridRegistry loader not set")
            cls._cache[name] = cls._loader(name)
        return cls._cache[name]

    @classmethod
    def evict(cls, name: str) -> None:
        """
        ========================================================================
         Evict the specified GridMap from the cache.
        ========================================================================
        """
        cls._cache.pop(name, None)

    @classmethod
    def clear(cls) -> None:
        """
        ========================================================================
         Clear the cache of loaded GridMaps.
        ========================================================================
        """
        cls._cache.clear()

    @classmethod
    def is_loaded(cls, name: str) -> bool:
        """
        ========================================================================
         Check if the specified GridMap is loaded into the cache.
        ========================================================================
        """
        return name in cls._cache

    @classmethod
    def loaded_names(cls) -> list[str]:
        """
        ========================================================================
         Return the names of the loaded GridMaps.
        ========================================================================
        """
        return list(cls._cache.keys())
