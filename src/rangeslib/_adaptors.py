from __future__ import annotations

from itertools import islice, product
from typing import Callable, Iterable, Protocol, cast

from ._core import Range, RangeAdaptor


class SupportsGetItem(Protocol):
    """Structural requirement for tuple-like indexed elements."""

    def __getitem__(self, index: int, /) -> object: ...


class To[InputT, OutputT](RangeAdaptor[InputT, OutputT]):
    """Convert an iterable with a supplied collection or factory callable."""

    def __init__(self, target_type: Callable[[Iterable[InputT]], OutputT]) -> None:
        self.target_type = target_type

    def __call__(self, iterable: Iterable[InputT]) -> OutputT:
        return self.target_type(iterable)


class Reverse[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Return the input elements in reverse order."""

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*reversed(list(iterable)))


class Filter[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Keep elements for which ``predicate`` returns true."""

    def __init__(self, predicate: Callable[[InputT], bool]) -> None:
        self.predicate = predicate

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*filter(self.predicate, iterable))


class Transform[InputT, OutputT](RangeAdaptor[InputT, Range[OutputT]]):
    """Map each input element to a new value with ``func``."""

    def __init__(self, func: Callable[[InputT], OutputT]) -> None:
        self.func = func

    def __call__(self, iterable: Iterable[InputT]) -> Range[OutputT]:
        return Range(*map(self.func, iterable))


class Take[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Apply Python slice-stop semantics to the input."""

    def __init__(self, n: int) -> None:
        self.n = n

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        if self.n >= 0:
            return Range(*islice(iterable, self.n))
        return Range(*list(iterable)[: self.n])


class TakeWhile[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Keep the initial elements while ``predicate`` remains true."""

    def __init__(self, predicate: Callable[[InputT], bool]) -> None:
        self.predicate = predicate

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        result: list[InputT] = []
        for value in iterable:
            if not self.predicate(value):
                break
            result.append(value)
        return Range(*result)


class Drop[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Apply Python slice-start semantics to the input."""

    def __init__(self, n: int) -> None:
        self.n = n

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*list(iterable)[self.n :])


class DropWhile[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Discard the initial elements while ``predicate`` remains true."""

    def __init__(self, predicate: Callable[[InputT], bool]) -> None:
        self.predicate = predicate

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        result: list[InputT] = []
        dropping = True
        for value in iterable:
            if dropping and not self.predicate(value):
                dropping = False
            if not dropping:
                result.append(value)
        return Range(*result)


class Counted[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Take a bounded prefix from the input's current iterator position."""

    def __init__(self, count: int) -> None:
        if count < 0:
            raise ValueError("Counted count cannot be negative")
        self.count = count

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*islice(iterable, self.count))


class Elements[OutputT](RangeAdaptor[SupportsGetItem, Range[OutputT]]):
    """Project one integer-indexed field from each tuple-like element."""

    def __init__(self, index: int) -> None:
        self.index = index

    def __call__(self, iterable: Iterable[SupportsGetItem]) -> Range[OutputT]:
        return Range(*(cast(OutputT, value[self.index]) for value in iterable))


class Keys[OutputT](Elements[OutputT]):
    """Project index ``0`` from each tuple-like element."""

    def __init__(self) -> None:
        super().__init__(0)


class Values[OutputT](Elements[OutputT]):
    """Project index ``1`` from each tuple-like element."""

    def __init__(self) -> None:
        super().__init__(1)


class Enumerate[InputT](RangeAdaptor[InputT, Range[tuple[int, InputT]]]):
    """Pair each input value with its sequential index."""

    def __init__(self, start: int = 0) -> None:
        self.start = start

    def __call__(self, iterable: Iterable[InputT]) -> Range[tuple[int, InputT]]:
        return Range(*enumerate(iterable, self.start))


class Concat[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Append configured iterables after the piped input."""

    def __init__(self, *iterables: Iterable[InputT]) -> None:
        self.iterables = iterables

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        result: list[InputT] = list(iterable)
        for additional_iterable in self.iterables:
            result.extend(additional_iterable)
        return Range(*result)


class Zip[InputT](RangeAdaptor[InputT, Range[tuple[InputT, ...]]]):
    """Zip the piped input with additional iterables to the shortest length."""

    def __init__(self, *iterables: Iterable[InputT]) -> None:
        self.iterables = iterables

    def __call__(self, iterable: Iterable[InputT]) -> Range[tuple[InputT, ...]]:
        return Range(*zip(iterable, *self.iterables))


class ZipTransform[OutputT](RangeAdaptor[object, Range[OutputT]]):
    """Apply a callable to corresponding values from several iterables."""

    def __init__(
        self, func: Callable[..., OutputT], *iterables: Iterable[object]
    ) -> None:
        self.func = func
        self.iterables = iterables

    def __call__(self, iterable: Iterable[object]) -> Range[OutputT]:
        return Range(*(self.func(*values) for values in zip(iterable, *self.iterables)))


class Adjacent[InputT](RangeAdaptor[InputT, Range[tuple[InputT, ...]]]):
    """Return overlapping windows of ``width`` adjacent elements."""

    def __init__(self, width: int = 2) -> None:
        if width < 1:
            raise ValueError("Adjacent width must be positive")
        self.width = width

    def __call__(self, iterable: Iterable[InputT]) -> Range[tuple[InputT, ...]]:
        values = list(iterable)
        return Range(
            *(
                tuple(values[index : index + self.width])
                for index in range(len(values) - self.width + 1)
            )
        )


class Pairwise[InputT](Adjacent[InputT]):
    """Return overlapping two-element windows."""

    def __init__(self) -> None:
        super().__init__(2)


class AdjacentTransform[InputT, OutputT](RangeAdaptor[InputT, Range[OutputT]]):
    """Apply a callable to each overlapping adjacent window."""

    def __init__(self, func: Callable[..., OutputT], width: int = 2) -> None:
        if width < 1:
            raise ValueError("AdjacentTransform width must be positive")
        self.func = func
        self.width = width

    def __call__(self, iterable: Iterable[InputT]) -> Range[OutputT]:
        values = list(iterable)
        return Range(
            *(
                self.func(*values[index : index + self.width])
                for index in range(len(values) - self.width + 1)
            )
        )


class PairwiseTransform[InputT, OutputT](AdjacentTransform[InputT, OutputT]):
    """Apply a binary callable to each pair of adjacent elements."""

    def __init__(self, func: Callable[[InputT, InputT], OutputT]) -> None:
        super().__init__(func, 2)


class Chunk[InputT](RangeAdaptor[InputT, Range[Range[InputT]]]):
    """Partition input into non-overlapping chunks of up to ``size`` elements."""

    def __init__(self, size: int) -> None:
        if size < 1:
            raise ValueError("Chunk size must be positive")
        self.size = size

    def __call__(self, iterable: Iterable[InputT]) -> Range[Range[InputT]]:
        values = list(iterable)
        return Range(
            *(
                Range(*values[index : index + self.size])
                for index in range(0, len(values), self.size)
            )
        )


class Slide[InputT](RangeAdaptor[InputT, Range[Range[InputT]]]):
    """Return overlapping windows of ``width`` elements."""

    def __init__(self, width: int) -> None:
        if width < 1:
            raise ValueError("Slide width must be positive")
        self.width = width

    def __call__(self, iterable: Iterable[InputT]) -> Range[Range[InputT]]:
        values = list(iterable)
        return Range(
            *(
                Range(*values[index : index + self.width])
                for index in range(len(values) - self.width + 1)
            )
        )


class ChunkBy[InputT](RangeAdaptor[InputT, Range[Range[InputT]]]):
    """Split input when the adjacent-value predicate returns false."""

    def __init__(self, predicate: Callable[[InputT, InputT], bool]) -> None:
        self.predicate = predicate

    def __call__(self, iterable: Iterable[InputT]) -> Range[Range[InputT]]:
        values = list(iterable)
        if not values:
            return Range()

        chunks: list[Range[InputT]] = []
        current_chunk = [values[0]]
        for previous, value in zip(values, values[1:]):
            if self.predicate(previous, value):
                current_chunk.append(value)
            else:
                chunks.append(Range(*current_chunk))
                current_chunk = [value]
        chunks.append(Range(*current_chunk))
        return Range(*chunks)


class Stride[InputT](RangeAdaptor[InputT, Range[InputT]]):
    """Select every ``step``-th input element, starting with the first."""

    def __init__(self, step: int) -> None:
        if step < 1:
            raise ValueError("Stride step must be positive")
        self.step = step

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*islice(iterable, 0, None, self.step))


class CartesianProduct[InputT](RangeAdaptor[InputT, Range[tuple[InputT, ...]]]):
    """Return the Cartesian product of the input and configured iterables."""

    def __init__(self, *iterables: Iterable[InputT]) -> None:
        self.iterables = iterables

    def __call__(self, iterable: Iterable[InputT]) -> Range[tuple[InputT, ...]]:
        return Range(*product(iterable, *self.iterables))


class Join[InputT](RangeAdaptor[Iterable[InputT], Range[InputT]]):
    """Flatten one level of nested iterables."""

    def __call__(self, iterable: Iterable[Iterable[InputT]]) -> Range[InputT]:
        result: list[InputT] = []
        for sub_iterable in iterable:
            result.extend(sub_iterable)
        return Range(*result)


class JoinWith[InputT](RangeAdaptor[Iterable[InputT], Range[InputT]]):
    """Flatten nested iterables with a separator pattern between them."""

    def __init__(self, separator: Iterable[InputT]) -> None:
        self.separator = tuple(separator)

    def __call__(self, iterable: Iterable[Iterable[InputT]]) -> Range[InputT]:
        result: list[InputT] = []
        first = True
        for sub_iterable in iterable:
            if not first:
                result.extend(self.separator)
            result.extend(sub_iterable)
            first = False
        return Range(*result)


class Split[InputT](RangeAdaptor[InputT, Range[Range[InputT]]]):
    """Split input into ranges wherever a separator pattern occurs."""

    def __init__(self, separator: Iterable[InputT]) -> None:
        self.separator = tuple(separator)

    def __call__(self, iterable: Iterable[InputT]) -> Range[Range[InputT]]:
        values = list(iterable)
        separator_length = len(self.separator)
        if separator_length == 0:
            raise ValueError("Split separator cannot be empty")

        result: list[Range[InputT]] = []
        current_chunk: list[InputT] = []
        index = 0
        while index < len(values):
            if values[index : index + separator_length] == list(self.separator):
                result.append(Range(*current_chunk))
                current_chunk = []
                index += separator_length
            else:
                current_chunk.append(values[index])
                index += 1
        result.append(Range(*current_chunk))
        return Range(*result)
