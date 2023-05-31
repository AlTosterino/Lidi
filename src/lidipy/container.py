from typing import Any, Callable, Hashable, Type, TypeVar, Union, cast

from lidipy.exceptions import BindingMissing

__all__ = ("Lidi",)

Injectable = Any
T = TypeVar("T", bound=Injectable)
Binding = Union[Type[Injectable], Hashable]
Constructor = Callable[[], Injectable]


class Lidi:
    """
    Lidi - LIghtweight Dependency Injector
    """

    __slots__ = ("__bindings",)

    def __init__(self) -> None:
        self.__bindings: dict[Any, Any] = {}

    def bind(
        self,
        cls: Binding,
        instance_or_callable: Injectable | Constructor,
        singleton: bool = False,
    ) -> None:
        is_callable = callable(instance_or_callable)
        if singleton and is_callable:
            self.__bindings[cls] = instance_or_callable()
        elif is_callable:
            self.__bindings[cls] = instance_or_callable
        else:
            self.__bindings[cls] = lambda: instance_or_callable

    def resolve(self, cls: Type[T]) -> T:
        binding = self.__get_binding(cls=cls)
        if callable(binding):
            return cast(T, binding())
        return binding

    def resolve_defer(self, cls: Type[T]) -> Callable[[], T]:
        return lambda: self.resolve(cls=cls)

    def __get_binding(self, cls: Type[T]) -> T:
        try:
            return cast(T, self.__bindings[cls])
        except KeyError:
            msg = f"Binding missing for type: {cls.__name__}"
            raise BindingMissing(msg)
