from types import SimpleNamespace

from ._adaptors import Drop, DropWhile, Filter, Join, JoinWith, Reverse, Split, Take, TakeWhile, To, Transform
from ._core import Range, RangeAdaptor, RangeGenerator
from ._generators import Empty, Indices, Iota, Repeat, Single


Ranges: SimpleNamespace = SimpleNamespace(
    Range=Range,
    RangeAdaptor=RangeAdaptor,
    RangeGenerator=RangeGenerator,
    To=To,
    Reverse=Reverse(),
    Filter=Filter,
    Take=Take,
    Drop=Drop,
    DropWhile=DropWhile,
    Join=Join,
    JoinWith=JoinWith,
    Split=Split,
    TakeWhile=TakeWhile,
    Single=Single,
    Empty=Empty,
    Iota=Iota,
    Indices=Indices,
    Repeat=Repeat,
    Transform=Transform,
)

__all__ = [
    "Drop",
    "DropWhile",
    "Empty",
    "Filter",
    "Indices",
    "Iota",
    "Join",
    "JoinWith",
    "Range",
    "RangeAdaptor",
    "RangeGenerator",
    "Ranges",
    "Repeat",
    "Reverse",
    "Single",
    "Split",
    "Take",
    "TakeWhile",
    "To",
    "Transform",
]
