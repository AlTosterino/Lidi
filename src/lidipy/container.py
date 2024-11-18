"""Lightweight Dependency Injection (Lidi) framework.

This module provides a simple dependency injection framework for managing
object dependencies within an application.
"""

from typing import Any, Callable, Type, cast

from lidipy.descriptors import ClassAttributeDescriptor
from lidipy.exceptions import BindingMissing

__all__ = ("Lidi",)

from lidipy.types import Binding, Constructor, Injectable, T


class Lidi:
    """Lidi - Lightweight Dependency Injector."""

    __slots__ = ("__bindings",)

    def __init__(self) -> None:
        self.__bindings: dict[Any, Any] = {}

    def bind(
        self,
        cls: Binding,
        instance_or_callable: Injectable | Constructor,
        singleton: bool = False,
    ) -> None:
        """Binds a class or interface to an instance or a callable.

        Args:
            cls (Binding): The class or interface to bind.
            instance_or_callable (Injectable | Constructor):
                The instance or callable to bind to the class or interface.
            singleton (bool, optional):
                Indicates whether the binding should be a singleton.
                Defaults to False.

        Returns:
            None

        Raises:
            None

        Example:
            >>> lidi = Lidi()
            >>> lidi.bind(IService, ConcreteService)
            >>> lidi.bind(ILogger, lambda: Logger())
            >>> lidi.bind(IDatabase, DatabaseConnection(), singleton=True)

        """
        is_callable = callable(instance_or_callable)
        if singleton and is_callable:
            self.__bindings[cls] = instance_or_callable()
        elif is_callable:
            self.__bindings[cls] = instance_or_callable
        else:
            self.__bindings[cls] = lambda: instance_or_callable

    def resolve(self, cls: Type[T]) -> T:
        """Resolve a class or interface to its bound instance or callable.

        Args:
            cls (Type[T]): The class or interface to resolve.

        Returns:
            T: The instance or callable bound to the class or interface.

        Raises:
            BindingMissing: If no binding is found for the specified class or interface.

        Example:
            >>> lidi = Lidi()
            >>> lidi.bind(IService, ConcreteService)
            >>> service = lidi.resolve(IService)

        """
        binding = self.__get_binding(cls=cls)
        if callable(binding):
            return cast(T, binding())
        return binding

    def resolve_defer(self, cls: Type[T]) -> Callable[[], T]:
        """Resolve a class or interface to a deferred callable.

        Args:
            cls (Type[T]): The class or interface to resolve.

        Returns:
            Callable[[], T]: A callable that, when invoked, resolves the class or interface.

        Example:
            >>> lidi = Lidi()
            >>> service = lidi.bind(IService, ConcreteService)
            >>> deferred_service = lidi.resolve_defer(IService) # Not resolved
            >>> service = deferred_service() # Resolved

        """
        return lambda: self.resolve(cls=cls)

    def resolve_attr(self, cls: Type[T]) -> T:
        """Resolve a class or interface to as a class attribute.

        Args:
            cls (Type[T]): The class or interface to resolve.

        Returns:
            T: The instance or callable bound to the class or interface.

        Raises:
            BindingMissing: If no binding is found for the specified class or interface.

        Example:
            >>> lidi = Lidi()
            >>> class A(): service = lidi.resolve_attr(IService)
            >>> lidi.bind(IService, ConcreteService)
            >>> service = A().service # Resolved

        """
        return cast(T, ClassAttributeDescriptor(cls=cls, container=self))

    def __get_binding(self, cls: Type[T]) -> T:
        """Retrieve the binding for a given class or interface.

        Args:
            cls (Type[T]): The class or interface to retrieve the binding for.

        Returns:
            T: The bound instance or callable.

        Raises:
            BindingMissing: If no binding is found for the specified class or interface.

        """
        try:
            return cast(T, self.__bindings[cls])
        except KeyError as e:
            msg = f"Binding missing for type: {cls.__name__}"
            raise BindingMissing(msg) from e
