from types import SimpleNamespace

from ._adaptors import Drop, Filter, Reverse, Take, To, Transform
from ._core import Range, RangeAdaptor, RangeGenerator
from ._generators import Empty, Indices, Iota, Repeat, Single


Ranges = SimpleNamespace(
    Range=Range,
    RangeAdaptor=RangeAdaptor,
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
    Transform=Transform,
)

__all__ = [
    "Drop",
    "Empty",
    "Filter",
    "Indices",
    "Iota",
    "Range",
    "RangeAdaptor",
    "RangeGenerator",
    "Ranges",
    "Repeat",
    "Reverse",
    "Single",
    "Take",
    "To",
    "Transform",
]
