from __future__ import annotations

from abc import ABC, abstractmethod
from collections import UserList
from typing import Iterable


class RangeAdaptor[InputT, OutputT](ABC):
    """Base contract for callable transformations over iterable values.

    Adaptors can be called directly or placed on the right side of ``|``.
    The reflected operator lets built-in iterables such as ``list``, ``str``,
    and ``range`` start a pipeline even though they cannot be modified.
    """

    def __ror__(self, iterable: Iterable[InputT]) -> OutputT:
        return self(iterable)

    @abstractmethod
    def __call__(self, iterable: Iterable[InputT]) -> OutputT:
        raise NotImplementedError


class RangeGenerator(ABC):
    """Marker base class for objects that construct :class:`Range` values."""

    pass


class Range[T](UserList[T]):
    """A list-backed, typed container used as the library's pipeline value.

    ``Range`` is eager: constructing or applying an adaptor stores the result
    immediately. It supports normal list operations and can pipe into any
    compatible :class:`RangeAdaptor`.
    """

    def __init__(self, *args: T) -> None:
        super().__init__(args)

    def __repr__(self) -> str:
        return f"Range({', '.join(repr(x) for x in self.data)})"

    def __str__(self) -> str:
        return f"[{', '.join(str(x) for x in self.data)}]"

    def __or__[OutputT](self, adaptor: RangeAdaptor[T, OutputT]) -> OutputT:
        return adaptor(self)

    def __len__(self) -> int:
        return len(self.data)

    def is_empty(self) -> bool:
        return len(self.data) == 0
