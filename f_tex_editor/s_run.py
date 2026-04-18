"""
================================================================================
 Launcher: start the f_tex_editor on localhost:5000.
 Open http://127.0.0.1:5000/?path=/tmp/untitled.tex in a browser.
================================================================================
"""

import os
import shutil
import sys
from pathlib import Path

from f_tex_editor import TexEditor


def _preflight(editor: TexEditor) -> None:
    """
    ============================================================================
     Print resolved engine + env diagnostics so engine-not-found problems
     are visible before the user hits Ctrl+S.
    ============================================================================
    """
    engine = editor.tex.engine
    resolved = shutil.which(cmd=engine) or (
        engine if Path(engine).is_file() else None
    )
    print('-' * 72)
    print(f'  f_tex_editor')
    print(f'  python     : {sys.executable}')
    print(f'  HOME       : {os.environ.get("HOME")}')
    print(f'  CONDA_PREFIX: {os.environ.get("CONDA_PREFIX")}')
    print(f'  engine     : {engine}')
    print(f'  resolved   : {resolved}')
    if resolved is None:
        print('  WARNING: engine not found on PATH or in known locations.')
        print('           compile will fail with "Engine binary not found".')
        print('           Either install tectonic, activate the conda env,')
        print('           or launch with a PATH that includes tectonic.')
    print('-' * 72)


if __name__ == '__main__':
    editor = TexEditor.Factory.a()
    _preflight(editor=editor)
    editor.run()
