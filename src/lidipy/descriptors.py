from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Type

from lidipy.types import T

if TYPE_CHECKING:
    from lidipy import Lidi  # pragma: no cover


class ClassAttributeDescriptor(Generic[T]):

    def __init__(self, cls: Type[T], container: Lidi) -> None:
        self.__cls = cls
        self.__container = container

    def __get__(self, instance: Any, owner: Any) -> T:
        return self.__container.resolve(self.__cls)
