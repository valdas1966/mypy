from f_gui.elements.i_1_connector.main import Connector, Routing
from f_gui.elements.i_1_container.main import Container
from f_ds.geometry.bounds import Bounds


class Factory:
    """
    ========================================================================
     Factory for Connector objects.
    ========================================================================
     Each preset builds two small Containers (a top-left source and a
     bottom-right destination) and a Connector between them, so the path
     can be inspected / rendered without wiring a full tree.
    ========================================================================
    """

    @staticmethod
    def _src() -> Container:
        """
        ========================================================================
         A small top-left source Container.
        ========================================================================
        """
        return Container(bounds=Bounds(top=20, left=10, bottom=40, right=30),
                         name='Src')

    @staticmethod
    def _dst() -> Container:
        """
        ========================================================================
         A small bottom-right destination Container.
        ========================================================================
        """
        return Container(bounds=Bounds(top=60, left=70, bottom=80, right=90),
                         name='Dst')

    @staticmethod
    def direct() -> Connector:
        """
        ========================================================================
         A straight (DIRECT) arrow connecting two Containers.
        ========================================================================
        """
        return Connector(src=Factory._src(), dst=Factory._dst())

    @staticmethod
    def orthogonal() -> Connector:
        """
        ========================================================================
         A 90-degree elbow (ORTHOGONAL) arrow connecting two Containers.
        ========================================================================
        """
        return Connector(src=Factory._src(), dst=Factory._dst(),
                         routing=Routing.ORTHOGONAL)
