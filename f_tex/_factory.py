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
         surfaces cleanly. Covers Linux / macOS / Windows install layouts
         (conda's Unix `bin/`, conda's Windows `Library/bin/`, Homebrew,
         scoop, chocolatey).
        ========================================================================
        """
        # 1) On PATH (conda env activated, or system-wide install).
        #    shutil.which already tries .exe suffix on Windows.
        found = shutil.which(cmd='tectonic')
        if found:
            return found
        # 2) Common install locations per platform.
        home = Path.home()
        candidates = [
            # Unix conda
            home / 'miniforge3' / 'bin' / 'tectonic',
            home / 'miniconda3' / 'bin' / 'tectonic',
            home / 'anaconda3' / 'bin' / 'tectonic',
            # macOS system
            Path('/opt/homebrew/bin/tectonic'),
            Path('/usr/local/bin/tectonic'),
            # Windows conda (binaries land in Library/bin, not bin)
            home / 'miniforge3' / 'Library' / 'bin' / 'tectonic.exe',
            home / 'miniconda3' / 'Library' / 'bin' / 'tectonic.exe',
            home / 'anaconda3' / 'Library' / 'bin' / 'tectonic.exe',
            # Windows scoop / chocolatey
            home / 'scoop' / 'shims' / 'tectonic.exe',
            Path('C:/ProgramData/chocolatey/bin/tectonic.exe'),
        ]
        for c in candidates:
            if c.is_file():
                return str(c)
        # 3) Let Tex raise its own "engine binary not found" error.
        return 'tectonic'
