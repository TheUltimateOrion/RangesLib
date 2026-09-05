from collections import UserList
from abc import ABC, abstractmethod
from typing import Callable, Iterable
from types import SimpleNamespace


class Range[T](UserList[T]):
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


class RangeGenerator(ABC):
    pass

class Empty(RangeGenerator):
    def __new__(cls) -> Range[int]:
        return Range()

class Single(RangeGenerator):
    def __new__(cls, value: int) -> Range[int]:
        return Range(value)

class Iota(RangeGenerator):
    def __new__(cls, start: int, end: int) -> Range[int]:
        return Range(*range(start, end))

class Indices(RangeGenerator):
    def __new__(cls, n: int) -> Range[int]:
        return Iota(0, n)

class Repeat(RangeGenerator):
    def __new__[T](cls, value: T, n: int) -> Range[T]:
        return Range(*[value] * n)

class RangeAdaptor[InputT, OutputT](ABC):
    @abstractmethod
    def __call__(self, iterable: Iterable[InputT]) -> OutputT:
        raise NotImplementedError


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


class Drop[InputT](RangeAdaptor[InputT, Range[InputT]]):
    def __init__(self, n: int) -> None:
        self.n = n

    def __call__(self, iterable: Iterable[InputT]) -> Range[InputT]:
        return Range(*list(iterable)[self.n:])

Ranges: SimpleNamespace = SimpleNamespace(
    Range=Range,
    RangeGenerator=RangeGenerator,
    To=To,
    Reverse=Reverse(),
    Filter=Filter,
    Take=Take,
    Drop=Drop,
    Single=Single,
    Empty=Empty,
    Iota=Iota,
    Indices=Indices,
    Repeat=Repeat,
    Transform=Transform
)

# ==========================================
# Usage Demonstrations
# ==========================================

def is_even(value: int) -> bool:
    return value % 2 == 0


def is_greater_than_five(value: int) -> bool:
    return value > 5

if __name__ == "__main__":
    # 1. Pipe syntax works flawlessly
    r1: Range[int] = Ranges.Iota(1, 11)  # Creates [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    r2: Range[int] = r1 | Ranges.Reverse | Ranges.Filter(is_even) | Ranges.Take(2)
    print("Pipe Syntax:")
    print(f"r1: {r1}")
    print(f"r2: {r2}")  # Output: [10, 8]

    print("\nFunctional Syntax (Without Pipes):")
    # 2. Standard functional syntax now works perfectly without pipes too!
    r3 = Ranges.Reverse(r1)
    r4 = Ranges.Filter(is_greater_than_five)(r1)
    r5 = Ranges.Take(3)(r1)
    r6: list[int] = r1 | Ranges.To(list)
    r7: tuple[int, ...] = r1 | Ranges.To(tuple)

    print(f"Reverse(r1): {r3}")
    print(f"Filter(>5, r1): {r4}")
    print(f"Take(3, r1): {r5}")
    print(f"To(list): {r6}")
    print(f"To(tuple): {r7}")
