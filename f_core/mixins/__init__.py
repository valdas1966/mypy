from typing import TYPE_CHECKING
from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.mixins.sizable import Sizable
    from f_core.mixins.dictable import Dictable
    from f_core.mixins.tupleable import Tupleable
    from f_core.mixins.hashable import Hashable
    from f_core.mixins.equatable import Equatable
    from f_core.mixins.comparable import Comparable
    from f_core.mixins.validatable import Validatable
    from f_core.mixins.validatable_mutable import ValidatableMutable
    from f_core.mixins.has import HasKey
    from f_core.mixins.has import HasName
    from f_core.mixins.has import HasRowCol
    from f_core.mixins.has import HasRowsCols

ULazy.install(globals(), {
    'Sizable': 'f_core.mixins.sizable:Sizable',
    'Dictable': 'f_core.mixins.dictable:Dictable',
    'Tupleable': 'f_core.mixins.tupleable:Tupleable',
    'Equatable': 'f_core.mixins.equatable:Equatable',
    'Comparable': 'f_core.mixins.comparable:Comparable',
    'Hashable': 'f_core.mixins.hashable:Hashable',
    'Validatable': 'f_core.mixins.validatable:Validatable',
    'ValidatableMutable': 'f_core.mixins.validatable_mutable:ValidatableMutable',
    'HasKey': 'f_core.mixins.has:HasKey',
    'HasName': 'f_core.mixins.has:HasName',
    'HasRowCol': 'f_core.mixins.has:HasRowCol',
    'HasRowsCols': 'f_core.mixins.has:HasRowsCols',
})
