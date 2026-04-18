import shutil
from pathlib import Path

from f_tex.main import Tex


class Factory:
    """
    ============================================================================
     Factory for Tex Compiler.
    ============================================================================
    """

    @staticmethod
    def a() -> Tex:
        """
        ========================================================================
         Return the default Tex compiler (tectonic engine).
         Resolves tectonic's absolute path so the compiler works even
         when launched from a shell without conda's bin/ on PATH
         (e.g. IDE run configs, Windows terminals, bare WSL shells).
        ========================================================================
        """
        return Tex(engine=Factory._resolve_tectonic())

    @staticmethod
    def _resolve_tectonic() -> str:
        """
        ========================================================================
         Find tectonic's absolute path; fall back to the bare name if no
         candidate is found so f_tex's own "engine not found" error still
         surfaces cleanly.
        ========================================================================
        """
        # 1) On PATH (conda env activated, or system-wide install)
        found = shutil.which(cmd='tectonic')
        if found:
            return found
        # 2) Common conda / anaconda install locations
        candidates = [
            Path.home() / 'miniforge3' / 'bin' / 'tectonic',
            Path.home() / 'miniconda3' / 'bin' / 'tectonic',
            Path.home() / 'anaconda3' / 'bin' / 'tectonic',
            Path('/opt/homebrew/bin/tectonic'),
            Path('/usr/local/bin/tectonic'),
        ]
        for c in candidates:
            if c.is_file():
                return str(c)
        # 3) Let Tex raise its own "engine binary not found" error
        return 'tectonic'
