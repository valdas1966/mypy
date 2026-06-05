from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_psl.os import u_dir
    from f_psl.file import u_txt
    from f_psl.pathlib import u_pathlib

ULazy.install(globals(), {
    'u_dir': 'f_psl.os.u_dir',
    'u_txt': 'f_psl.file.u_txt',
    'u_pathlib': 'f_psl.pathlib.u_pathlib',
})
