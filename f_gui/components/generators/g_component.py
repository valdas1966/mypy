from f_gui.components.component import Component
from f_gui.geometry.generators.g_geometry import GenGeometry


class GenComponent:

    @staticmethod
    def full() -> Component:
        """
        ========================================================================
         Generate a full-screen component.
        ========================================================================
        """
        geometry = GenGeometry.full()
        return Component(key='full', geometry=geometry)