from importlib import import_module


class ULazy:
    """
    ============================================================================
     Static utilities for PEP 562 lazy package aggregation.
    ============================================================================
     Replaces the hand-rolled ``__getattr__`` block duplicated across
     every aggregator ``__init__.py``. A single ``module:attr`` spec
     unifies the two historical forms:
       * ``'UList': 'f_psl.builtins.list:UList'`` -> import the module,
          return the symbol ``UList``.
       * ``'u_dir': 'f_psl.os.u_dir'``           -> no colon, return the
          module itself.
       * ``'CellBase': '.i_0_base:CellBase'``    -> relative path,
          resolved against the calling package.
    ============================================================================
    """

    @staticmethod
    def install(g: dict, specs: dict[str, str]) -> None:
        """
        ========================================================================
         Install lazy ``__getattr__`` / ``__all__`` / ``__dir__`` into the
          calling package's globals ``g``.
        ========================================================================
         * ``g``     : the package's ``globals()``.
         * ``specs`` : public-name -> ``'module'`` or ``'module:attr'``.
         Resolved values are cached into ``g`` so each spec imports once.
        ========================================================================
        """
        def __getattr__(name: str):
            spec = specs.get(name)
            if spec is None:
                raise AttributeError(
                    f"module {g['__name__']!r} has no "
                    f"attribute {name!r}"
                )
            # 'module:attr' -> symbol; 'module' -> module itself
            mod_path, _, attr = spec.partition(':')
            # Relative spec ('.sub') resolves against this package
            pkg = (g.get('__package__') or g.get('__name__')) \
                if mod_path.startswith('.') else None
            mod = import_module(mod_path, pkg)
            val = getattr(mod, attr) if attr else mod
            # Cache so PEP 562 __getattr__ fires only once per spec
            g[name] = val
            return val

        g['__getattr__'] = __getattr__
        g['__all__'] = list(specs)
        g['__dir__'] = lambda: list(specs)
