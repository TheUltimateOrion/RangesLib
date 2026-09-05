from __future__ import annotations

from itertools import islice
from typing import Any, Callable, Iterable

from ._core import Range, RangeAdaptor


class To[InputT, OutputT](RangeAdaptor[InputT, OutputT]):
    def __init__(self, target_type: Callable[[Iterable[InputT]], OutputT]) -> None:
        self.target_type = target_type

    def __call__(self, iterable: Iterable[InputT]) -> OutputT:
        return self.target_type(iterable)


class Reverse[InputT](RangeAdaptor[InputT, Range[InputT]]):
    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*reversed(list(iterable)))


class Filter[InputT](RangeAdaptor[InputT, Range[InputT]]):
    def __init__(self, predicate: Callable[[InputT], bool]) -> None:
        self.predicate = predicate

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*filter(self.predicate, iterable))


class Transform[InputT, OutputT](RangeAdaptor[InputT, Range[OutputT]]):
    def __init__(self, func: Callable[[InputT], OutputT]) -> None:
        self.func = func

    def __call__(self, iterable: Iterable[InputT]) -> Range[OutputT]:
        return Range(*map(self.func, iterable))


class Take[InputT](RangeAdaptor[InputT, Range[InputT]]):
    def __init__(self, n: int) -> None:
        self.n = n

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*list(iterable)[:self.n])

class TakeWhile[InputT](RangeAdaptor[InputT, Range[InputT]]):
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
    def __init__(self, n: int) -> None:
        self.n = n

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*list(iterable)[self.n:])

class DropWhile[InputT](RangeAdaptor[InputT, Range[InputT]]):
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
    def __init__(self, count: int) -> None:
        if count < 0:
            raise ValueError("Counted count cannot be negative")
        self.count = count

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*islice(iterable, self.count))


class Elements[InputT](RangeAdaptor[InputT, Range[Any]]):
    def __init__(self, index: int) -> None:
        self.index = index

    def __call__(self, iterable: Iterable[InputT]) -> Range[Any]:
        return Range(*(value[self.index] for value in iterable))  # type: ignore[index]


class Keys[InputT](Elements[InputT]):
    def __init__(self) -> None:
        super().__init__(0)


class Values[InputT](Elements[InputT]):
    def __init__(self) -> None:
        super().__init__(1)


class Enumerate[InputT](RangeAdaptor[InputT, Range[tuple[int, InputT]]]):
    def __init__(self, start: int = 0) -> None:
        self.start = start

    def __call__(self, iterable: Iterable[InputT]) -> Range[tuple[int, InputT]]:
        return Range(*enumerate(iterable, self.start))


class Concat[InputT](RangeAdaptor[InputT, Range[InputT]]):
    def __init__(self, *iterables: Iterable[InputT]) -> None:
        self.iterables = iterables

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        result: list[InputT] = list(iterable)
        for additional_iterable in self.iterables:
            result.extend(additional_iterable)
        return Range(*result)


class Join[InputT](RangeAdaptor[Iterable[InputT], Range[InputT]]):
    def __call__(self, iterable: Iterable[Iterable[InputT]]) -> Range[InputT]:
        result: list[InputT] = []
        for sub_iterable in iterable:
            result.extend(sub_iterable)
        return Range(*result)

class JoinWith[InputT](RangeAdaptor[Iterable[InputT], Range[InputT]]):
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
            if values[index:index + separator_length] == list(self.separator):
                result.append(Range(*current_chunk))
                current_chunk = []
                index += separator_length
            else:
                current_chunk.append(values[index])
                index += 1
        result.append(Range(*current_chunk))
        return Range(*result)