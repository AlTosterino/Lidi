from typing import Any, Callable, Hashable, Type, TypeVar, Union

Injectable = Any
T = TypeVar("T", bound=Injectable)
Binding = Union[Type[Injectable], Hashable]
Constructor = Callable[[], Injectable]
