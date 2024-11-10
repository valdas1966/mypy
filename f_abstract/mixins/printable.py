from abc import ABC, abstractmethod


class Printable(ABC):
    """
    Mixin class for printable objects.

    Provides an interface for defining a string representation (`__str__`) and an
    informative object representation (`__repr__`). Classes that inherit from this
    mixin must implement the `__str__` method.

    Example:
        >>> class MyPrintable(Printable):
        >>>     def __str__(self) -> str:
        >>>         return "MyPrintable Object"
        >>>
        >>> obj = MyPrintable()
        >>> print(obj)
        MyPrintable Object
        >>> repr(obj)
        <MyPrintable: MyPrintable Object>
    """

    @abstractmethod
    def __str__(self) -> str:
        """
        Return the string representation of the object.

        This method must be implemented by any class that inherits from `Printable`.

        Returns:
            str: A string representing the object.

        Example:
            >>> class MyPrintable(Printable):
            >>>     def __str__(self) -> str:
            >>>         return "MyPrintable Object"
            >>>
            >>> obj = MyPrintable()
            >>> print(obj)
            MyPrintable Object
        """
        pass

    def __repr__(self) -> str:
        """
        Return an informative representation of the object.

        Returns:
            str: A string representation of the object in the format <ClassName: str(self)>.

        Example:
            >>> class MyPrintable(Printable):
            >>>     def __str__(self) -> str:
            >>>         return "MyPrintable Object"
            >>>
            >>> obj = MyPrintable()
            >>> repr(obj)
            <MyPrintable: MyPrintable Object>
        """
        return f'<{type(self).__name__}: {str(self)}>'
