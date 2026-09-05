from __future__ import annotations

from abc import ABC, abstractmethod
from collections import UserList
from typing import Iterable


class RangeAdaptor[InputT, OutputT](ABC):
    def __ror__(self, iterable: Iterable[InputT]) -> OutputT:
        return self(iterable)

    @abstractmethod
    def __call__(self, iterable: Iterable[InputT]) -> OutputT:
        raise NotImplementedError


class RangeGenerator(ABC):
    pass


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
