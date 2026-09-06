from __future__ import annotations

from abc import ABC, abstractmethod
from collections import UserList
from typing import Callable, Iterable, SupportsIndex, overload


class RangeAdaptor[InputT, OutputT](ABC):
    """Base contract for callable transformations over iterable values.

    Adaptors can be called directly or placed on the right side of ``|``.
    The reflected operator lets built-in iterables such as ``list``, ``str``,
    and ``range`` start a pipeline even though they cannot be modified.
    """

    def __ror__(self, iterable: Iterable[InputT]) -> OutputT:
        return self(iterable)

    def __or__[NextOutputT](
        self, adaptor: Callable[[OutputT], NextOutputT], /
    ) -> RangeAdaptor[InputT, NextOutputT]:
        return _ComposedRangeAdaptor(self, adaptor)

    @abstractmethod
    def __call__(self, iterable: Iterable[InputT]) -> OutputT:
        raise NotImplementedError


class _ComposedRangeAdaptor[InputT, MiddleT, OutputT](RangeAdaptor[InputT, OutputT]):
    def __init__(
        self,
        first: Callable[[Iterable[InputT]], MiddleT],
        second: Callable[[MiddleT], OutputT],
    ) -> None:
        self.first = first
        self.second = second

    def __call__(self, iterable: Iterable[InputT]) -> OutputT:
        return self.second(self.first(iterable))


class RangeGenerator(ABC):
    """Marker base class for objects that construct :class:`Range` values."""


class Range[T](UserList[T]):
    """A list-backed, typed container used as the library's pipeline value.

    ``Range`` is eager: constructing or applying an adaptor stores the result
    immediately. Construction uses positional values, so ``Range(1, 2, 3)``
    contains three elements. Standard list-like operations preserve ``Range``
    as the result type.
    """

    def __init__(self, *args: T) -> None:
        super().__init__(args)

    def __repr__(self) -> str:
        return f"Range({', '.join(repr(x) for x in self.data)})"

    def __str__(self) -> str:
        return str(self.data)

    def __or__[OutputT](self, adaptor: Callable[[Iterable[T]], OutputT], /) -> OutputT:
        return adaptor(self)

    @overload
    def __getitem__(self, index: SupportsIndex) -> T: ...

    @overload
    def __getitem__(self, index: slice[SupportsIndex | None]) -> Range[T]: ...

    def __getitem__(
        self, index: SupportsIndex | slice[SupportsIndex | None]
    ) -> T | Range[T]:
        if isinstance(index, slice):
            return Range(*self.data[index])
        return self.data[index]

    def __add__(self, other: Iterable[T]) -> Range[T]:
        return Range(*self.data, *other)

    def __radd__(self, other: Iterable[T]) -> Range[T]:
        return Range(*other, *self.data)

    def __mul__(self, count: int) -> Range[T]:
        return Range(*(self.data * count))

    def __rmul__(self, count: int) -> Range[T]:
        return self * count

    def copy(self) -> Range[T]:
        """Return a shallow ``Range`` copy without nesting the source range."""
        return Range(*self.data)

    def is_empty(self) -> bool:
        """Return ``True`` when the range has no elements."""
        return not self.data
