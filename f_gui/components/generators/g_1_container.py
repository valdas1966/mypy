from f_gui.components.i_1_container import Container, Position


class GenContainer:
    """
    =======================================================================
     Generator-Class for Containers.    
    =======================================================================
    """

    @staticmethod
    def two_childs() -> Container:
        """
        =======================================================================
         Generate a Container with two childs.
        =======================================================================
        """
        container = Container()
        pos_left = Position(relative=(10, 10, 35, 80))
        left = Container(name='Left', position=pos_left)
        container.add_child(left)
        pos_right = Position(relative=(10, 55, 35, 80))
        right = Container(name='Right', position=pos_right)
        container.add_child(right)
        return container
