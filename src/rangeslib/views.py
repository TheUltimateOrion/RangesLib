from __future__ import annotations

from typing import Any, Callable, Iterable, Protocol, cast

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
from ._core import Range


class _TypePreservingView(Protocol):
    def __call__[T](self, iterable: Iterable[T], /) -> Range[T]: ...

    def __ror__[T](self, iterable: Iterable[T], /) -> Range[T]: ...


class _EnumerateView(Protocol):
    def __call__[T](self, iterable: Iterable[T], /) -> Range[tuple[int, T]]: ...

    def __ror__[T](self, iterable: Iterable[T], /) -> Range[tuple[int, T]]: ...


class _AdjacentView(Protocol):
    def __call__[T](self, iterable: Iterable[T], /) -> Range[tuple[T, ...]]: ...

    def __ror__[T](self, iterable: Iterable[T], /) -> Range[tuple[T, ...]]: ...


class _ChunkView(Protocol):
    def __call__[T](self, iterable: Iterable[T], /) -> Range[Range[T]]: ...

    def __ror__[T](self, iterable: Iterable[T], /) -> Range[Range[T]]: ...


class _JoinView(Protocol):
    def __call__[T](self, iterable: Iterable[Iterable[T]], /) -> Range[T]: ...

    def __ror__[T](self, iterable: Iterable[Iterable[T]], /) -> Range[T]: ...


def to[InputT, OutputT](
    target_type: Callable[[Iterable[InputT]], OutputT],
) -> To[InputT, OutputT]:
    """Convert the pipeline input with ``target_type``.

    ``to`` is the only public adaptor that does not necessarily return
    :class:`~rangeslib.Range`; it returns exactly what the supplied callable
    produces.
    """
    return To(target_type)


def reverse() -> _TypePreservingView:
    """Reverse all input values and return an eager ``Range``."""
    return cast(_TypePreservingView, Reverse[object]())


def filter[InputT](predicate: Callable[[InputT], bool]) -> Filter[InputT]:
    """Keep values for which ``predicate`` returns ``True``."""
    return Filter(predicate)


def transform[InputT, OutputT](
    func: Callable[[InputT], OutputT],
) -> Transform[InputT, OutputT]:
    """Map every input value through ``func``."""
    return Transform(func)


def take(count: int) -> _TypePreservingView:
    """Take values using Python slice-stop semantics.

    Positive and zero counts select a prefix. Negative counts behave like
    ``list(iterable)[:count]`` and therefore require complete input
    materialization.
    """
    return cast(_TypePreservingView, Take[object](count))


def takewhile[InputT](predicate: Callable[[InputT], bool]) -> TakeWhile[InputT]:
    """Take initial values while ``predicate`` remains ``True``."""
    return TakeWhile(predicate)


def drop(count: int) -> _TypePreservingView:
    """Drop values using Python slice-start semantics.

    Negative counts behave like ``list(iterable)[count:]`` and therefore
    require complete input materialization.
    """
    return cast(_TypePreservingView, Drop[object](count))


def dropwhile[InputT](predicate: Callable[[InputT], bool]) -> DropWhile[InputT]:
    """Drop initial values while ``predicate`` remains ``True``."""
    return DropWhile(predicate)


def counted(count: int) -> _TypePreservingView:
    """Consume at most ``count`` values from the current iterator position.

    Unlike ``take``, ``counted`` does not first materialize the entire input.
    ``count`` must be non-negative.
    """
    return cast(_TypePreservingView, Counted[object](count))


def elements(index: int) -> Elements[Any]:
    """Project integer-indexed field ``index`` from every input value."""
    return Elements[Any](index)


def keys() -> Keys[Any]:
    """Project field ``0`` from every tuple-like input value."""
    return Keys[Any]()


def values() -> Values[Any]:
    """Project field ``1`` from every tuple-like input value."""
    return Values[Any]()


def enumerate(start: int = 0) -> _EnumerateView:
    """Pair each input value with a sequential integer index."""
    return cast(_EnumerateView, Enumerate[object](start))


def concat[InputT](*iterables: Iterable[InputT]) -> Concat[InputT]:
    """Append configured iterables after the pipeline input."""
    return Concat(*iterables)


def zip[InputT](*iterables: Iterable[InputT]) -> Zip[InputT]:
    """Zip the pipeline input with configured iterables to the shortest length."""
    return Zip(*iterables)


def zip_transform[OutputT](
    func: Callable[..., OutputT], *iterables: Iterable[Any]
) -> ZipTransform[OutputT]:
    """Zip corresponding values and call ``func`` for each group."""
    return ZipTransform(func, *iterables)


def adjacent(width: int = 2) -> _AdjacentView:
    """Return overlapping tuple windows of ``width`` values."""
    return cast(_AdjacentView, Adjacent[object](width))


def pairwise() -> _AdjacentView:
    """Return overlapping two-value tuples."""
    return cast(_AdjacentView, Pairwise[object]())


def adjacent_transform[OutputT](
    func: Callable[..., OutputT], width: int = 2
) -> AdjacentTransform[Any, OutputT]:
    """Call ``func`` for each overlapping window of ``width`` values."""
    return AdjacentTransform[Any, OutputT](func, width)


def pairwise_transform[InputT, OutputT](
    func: Callable[[InputT, InputT], OutputT],
) -> PairwiseTransform[InputT, OutputT]:
    """Call a binary ``func`` for each adjacent pair."""
    return PairwiseTransform(func)


def chunk(size: int) -> _ChunkView:
    """Partition the input into non-overlapping ``Range`` chunks.

    ``size`` must be positive. The final chunk may contain fewer values.
    """
    return cast(_ChunkView, Chunk[object](size))


def slide(width: int) -> _ChunkView:
    """Return overlapping ``Range`` windows of exactly ``width`` values."""
    return cast(_ChunkView, Slide[object](width))


def chunk_by[InputT](
    predicate: Callable[[InputT, InputT], bool],
) -> ChunkBy[InputT]:
    """Split whenever ``predicate(previous, current)`` returns ``False``."""
    return ChunkBy(predicate)


def stride(step: int) -> _TypePreservingView:
    """Select every ``step``-th value, starting with the first.

    ``step`` must be positive.
    """
    return cast(_TypePreservingView, Stride[object](step))


def cartesian_product[InputT](
    *iterables: Iterable[InputT],
) -> CartesianProduct[InputT]:
    """Return the Cartesian product of the input and configured iterables."""
    return CartesianProduct(*iterables)


def join() -> _JoinView:
    """Flatten one level of nested iterables."""
    return cast(_JoinView, Join[object]())


def join_with[InputT](separator: Iterable[InputT]) -> JoinWith[InputT]:
    """Flatten nested iterables with ``separator`` inserted between them."""
    return JoinWith(separator)


def split[InputT](separator: Iterable[InputT]) -> Split[InputT]:
    """Split input wherever the separator pattern occurs.

    Empty chunks are preserved. An empty separator raises ``ValueError`` when
    the adaptor is applied.
    """
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
