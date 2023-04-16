from typing import Any, Callable, Hashable, Type, TypeVar, Union, cast

Injectable = Any
T = TypeVar("T", bound=Injectable)
Binding = Union[Type[Injectable], Hashable]
Constructor = Callable[[], Injectable]


class Lidi:
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
        elif singleton:
            self.__bindings[cls] = instance_or_callable
        else:
            self.__bindings[cls] = lambda: instance_or_callable

    def resolve(self, cls: Type[T]) -> T:
        binding = self.__bindings[cls]
        if callable(binding):
            return cast(T, binding())
        return cast(T, binding)


__all__ = ("Lidi",)
