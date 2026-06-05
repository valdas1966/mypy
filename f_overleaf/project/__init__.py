from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_overleaf.project.main import ProjectOverLeaf

ULazy.install(globals(), {'ProjectOverLeaf': 'f_overleaf.project.main:ProjectOverLeaf'})
