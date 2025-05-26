from f_core.mixins.printable import Printable
from f_core.mixins.comparable import Comparable
from f_gui.geometry.generators.g_tlwh import GenTLWH, TLWH


class Position(Printable, Comparable):
    """
    ============================================================================
     1. Component-Class to manage relative and absolute positions.
     2. Position inits with a relative position (optionally with a parent).
     3. The absolute position is updated automatically on parent-change.
    ============================================================================
    """

    def __init__(self,
                 relative: tuple[float, float, float, float] | TLWH = GenTLWH.full(),
                 parent: tuple[float, float, float, float] | TLWH = GenTLWH.full(),
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._absolute: TLWH | None = None
        self._relative = self._init_relative(relative=relative)
        self._parent = self._init_parent(parent=parent)

    @property
    def relative(self) -> TLWH:
        """
        ========================================================================
         Get the object's relative position (top, left, width, height).
        ========================================================================
        """
        return self._relative

    @relative.setter
    def relative(self, val: tuple[float, float, float, float] | TLWH) -> None:
        """
        ========================================================================
         Set the relative position (left, top, width, height).
        ========================================================================
        """
        if isinstance(val, TLWH):
            self._relative = val
        else:
            self._relative = TLWH(*val)

    @property
    def absolute(self) -> TLWH:
        """
        ========================================================================
         Get the absolute position (left, top, width, height).
        ========================================================================
        """
        return self._absolute

    @property
    def parent(self) -> TLWH:
        """
        ========================================================================
         Get the absolute position of the Parent.
        ========================================================================
        """
        return self._parent

    @parent.setter
    def parent(self, val: TLWH) -> None:
        """
        ========================================================================
         Set the parent's absolute position.
        ========================================================================
        """
        self._parent = val
        self._update_absolute()

    def key_comparison(self) -> tuple[float, float, float, float]:
        """
        ========================================================================
         Return the key-comparison of the object.
        ========================================================================
        """
        return self.absolute.to_tuple()

    def _update_absolute(self) -> None:
        """
        ========================================================================
         Update the absolute position based on the parent's dimensions.
        ========================================================================
        """
        top = (self._parent.height * self._relative.top / 100) + self._parent.top
        left = (self._parent.width * self._relative.left / 100) + self._parent.left
        width = (self._parent.width * self._relative.width / 100)
        height = (self._parent.height * self._relative.height / 100)
        self._absolute = TLWH(top, left, width, height)

    def _init_relative(self,
                       relative: tuple[float, float, float, float] | TLWH) -> TLWH:
        """
        ========================================================================
         Inits Relative (TLWH).
        ========================================================================
        """ 
        # If relative is a tuple, convert it to a TLWH object.
        if isinstance(relative, tuple):
            return TLWH(*relative)
        # If relative is already a TLWH object, return it.
        else:
            return relative

    def _init_parent(self,
                     parent: tuple[float, float, float, float] | TLWH) -> TLWH:
        """
        ========================================================================
         Inits Parent (TLWH).
        ========================================================================
        """ 
        # If parent is a tuple, convert it to a TLWH object.
        if isinstance(parent, tuple):
            return TLWH(*parent)
        # If parent is already a TLWH object, return it.
        else:
            return parent
        
    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(0.2, 0.3, 0.4, 0.5) * (0, 0, 80, 80) -> (16, 24, 32, 40)'
        ========================================================================
        """
        return f'{self.relative} X {self.parent} -> {self.absolute}'
