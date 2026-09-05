from __future__ import annotations

from typing import Any, Callable, Iterable, TypeVar

from ._adaptors import (
    Adjacent,
    AdjacentTransform,
    CartesianProduct,
    Chunk,
    ChunkBy,
    Concat,
    Counted,
    Drop,
    DropWhile,
    Elements,
    Enumerate,
    Filter,
    Join,
    JoinWith,
    Keys,
    Pairwise,
    PairwiseTransform,
    Reverse,
    Slide,
    Split,
    Stride,
    Take,
    TakeWhile,
    To,
    Transform,
    Values,
    Zip,
    ZipTransform,
)

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


def to(target_type: Callable[[Iterable[InputT]], OutputT]) -> To[InputT, OutputT]:
    """Create an adaptor that converts its input with ``target_type``."""
    return To(target_type)


def reverse() -> Reverse[Any]:
    """Create an adaptor that reverses its input."""
    return Reverse()


def filter(predicate: Callable[[InputT], bool]) -> Filter[InputT]:
    """Create an adaptor that keeps values matching ``predicate``."""
    return Filter(predicate)


def transform(func: Callable[[InputT], OutputT]) -> Transform[InputT, OutputT]:
    """Create an adaptor that maps values with ``func``."""
    return Transform(func)


def take(count: int) -> Take[Any]:
    """Create an adaptor that takes at most ``count`` values."""
    return Take(count)


def takewhile(predicate: Callable[[InputT], bool]) -> TakeWhile[InputT]:
    """Create an adaptor that takes values while ``predicate`` is true."""
    return TakeWhile(predicate)


def drop(count: int) -> Drop[Any]:
    """Create an adaptor that drops the first ``count`` values."""
    return Drop(count)


def dropwhile(predicate: Callable[[InputT], bool]) -> DropWhile[InputT]:
    """Create an adaptor that drops values while ``predicate`` is true."""
    return DropWhile(predicate)


def counted(count: int) -> Counted[Any]:
    """Create an adaptor that takes a bounded prefix."""
    return Counted(count)


def elements(index: int) -> Elements[Any]:
    """Create an adaptor that projects one indexed field."""
    return Elements(index)


def keys() -> Keys[Any]:
    """Create an adaptor that projects field zero."""
    return Keys()


def values() -> Values[Any]:
    """Create an adaptor that projects field one."""
    return Values()


def enumerate(start: int = 0) -> Enumerate[Any]:
    """Create an adaptor that pairs values with indexes."""
    return Enumerate(start)


def concat(*iterables: Iterable[InputT]) -> Concat[InputT]:
    """Create an adaptor that appends additional iterables."""
    return Concat(*iterables)


def zip(*iterables: Iterable[InputT]) -> Zip[InputT]:
    """Create an adaptor that zips input with additional iterables."""
    return Zip(*iterables)


def zip_transform(func: Callable[..., OutputT], *iterables: Iterable[Any]) -> ZipTransform[OutputT]:
    """Create an adaptor that transforms corresponding values."""
    return ZipTransform(func, *iterables)


def adjacent(width: int = 2) -> Adjacent[Any]:
    """Create an adaptor that returns overlapping windows."""
    return Adjacent(width)


def pairwise() -> Pairwise[Any]:
    """Create an adaptor that returns adjacent pairs."""
    return Pairwise()


def adjacent_transform(func: Callable[..., OutputT], width: int = 2) -> AdjacentTransform[Any, OutputT]:
    """Create an adaptor that transforms overlapping windows."""
    return AdjacentTransform(func, width)


def pairwise_transform(func: Callable[[InputT, InputT], OutputT]) -> PairwiseTransform[InputT, OutputT]:
    """Create an adaptor that transforms adjacent pairs."""
    return PairwiseTransform(func)


def chunk(size: int) -> Chunk[Any]:
    """Create an adaptor that partitions input into chunks."""
    return Chunk(size)


def slide(width: int) -> Slide[Any]:
    """Create an adaptor that returns overlapping windows."""
    return Slide(width)


def chunk_by(predicate: Callable[[InputT, InputT], bool]) -> ChunkBy[InputT]:
    """Create an adaptor that splits between non-matching adjacent values."""
    return ChunkBy(predicate)


def stride(step: int) -> Stride[Any]:
    """Create an adaptor that selects every ``step``-th value."""
    return Stride(step)


def cartesian_product(*iterables: Iterable[InputT]) -> CartesianProduct[InputT]:
    """Create an adaptor for the Cartesian product."""
    return CartesianProduct(*iterables)


def join() -> Join[Any]:
    """Create an adaptor that flattens one nesting level."""
    return Join()


def join_with(separator: Iterable[InputT]) -> JoinWith[InputT]:
    """Create an adaptor that flattens with a separator pattern."""
    return JoinWith(separator)


def split(separator: Iterable[InputT]) -> Split[InputT]:
    """Create an adaptor that splits on a separator pattern."""
    return Split(separator)


__all__ = [
    "adjacent",
    "adjacent_transform",
    "cartesian_product",
    "chunk",
    "chunk_by",
    "concat",
    "counted",
    "drop",
    "dropwhile",
    "elements",
    "enumerate",
    "filter",
    "join",
    "join_with",
    "keys",
    "pairwise",
    "pairwise_transform",
    "reverse",
    "slide",
    "split",
    "stride",
    "take",
    "takewhile",
    "to",
    "transform",
    "values",
    "zip",
    "zip_transform",
]
