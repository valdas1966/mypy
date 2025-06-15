from f_gui.components.component import Component
from f_gui.layout.generators.g_bounds import GenBounds


class GenComponent:
    """
    ========================================================================
     Generator for a Generic GUI-Component.
    ========================================================================
    """

    @staticmethod
    def window_empty() -> Component:
        """
        ========================================================================
         Generate a empty window component.
        ========================================================================
        """
        geometry = GenBounds.full()
        return Component(name='Window', bounds=geometry)
    
    @staticmethod
    def window_container() -> Component:
        """
        ========================================================================
         Generate a Window with one Container in the center.
        ========================================================================
        """
        win = GenComponent.window_empty()
        geo_con = GenBounds.half()
        con = Component(name='Container', bounds=geo_con)
        con.parent = win
        return win

    @staticmethod
    def window_label() -> Component:
        """
        ========================================================================
         Generate a Window with one Container and one Label in the center.
        ========================================================================
        """
        win = GenComponent.window_container()
        con = win.children['Container']
        geo_label = GenBounds.half()
        label = Component(name='Label', bounds=geo_label)
        label.parent = con
        return win  
