# rangeslib

A small, typed Python library for composing ranges, generators, and collection adaptors with readable pipeline syntax.

```python
from rangeslib import Filter, Iota, Take, To, Transform

values = (
    Iota(1, 11)
    | Filter(lambda value: value % 2 == 0)
    | Transform(lambda value: value * 10)
    | Take(3)
    | To(list)
)

assert values == [20, 40, 60]
```

## Features

- `Range[T]`, a list-like typed range container
- Range generators: `Empty`, `Single`, `Iota`, `Indices`, and `Repeat`
- Range adaptors: `Filter`, `Transform`, `Take`, `Counted`, `TakeWhile`, `Drop`, `DropWhile`, `Reverse`, `Elements`, `Keys`, `Values`, `Enumerate`, `Join`, `JoinWith`, `Split`, `Concat`, and `To`
- Readable `|` pipelines for `Range` values
- Direct adaptor calls for any Python `Iterable`
- Generic input and output types for transformations and conversions
- A small public API with private implementation modules
- Automated tests on Python 3.12, 3.13, and 3.14 through GitHub Actions

## Installation

The project requires Python 3.12 or newer.

```bash
python -m pip install -e .
```

For local development, create and activate a virtual environment first:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Usage

Generators create `Range` values:

```python
from rangeslib import Empty, Indices, Iota, Repeat, Single

assert list(Empty()) == []
assert list(Single("item")) == ["item"]
assert list(Iota(2, 5)) == [2, 3, 4]
assert list(Indices(3)) == [0, 1, 2]
assert list(Repeat("x", 3)) == ["x", "x", "x"]
```

Adaptors transform an iterable and can be used directly:

```python
from rangeslib import Filter, Take, Transform

result = Take(2)(Filter(lambda value: value > 2)([1, 2, 3, 4]))
assert list(result) == [3, 4]

result = Transform(str)(range(3))
assert list(result) == ["0", "1", "2"]
```

`TakeWhile` and `DropWhile` operate on the beginning of an iterable:

```python
from rangeslib import DropWhile, TakeWhile

assert list(TakeWhile(lambda value: value < 3)([1, 2, 3, 4])) == [1, 2]
assert list(DropWhile(lambda value: value < 3)([1, 2, 3, 4])) == [3, 4]
```

`Join` accepts an iterable of iterables and flattens one level:

```python
from rangeslib import Join

result = Join()((values for values in [[1, 2], (3, 4)]))
assert list(result) == [1, 2, 3, 4]
```

`JoinWith` inserts an iterable separator between inner iterables, while `Split`
divides an iterable wherever it finds a separator pattern:

```python
from rangeslib import JoinWith, Split

joined = JoinWith([0, 0])([[1, 2], [3, 4]])
chunks = Split([0, 0])([1, 2, 0, 0, 3, 4])

assert list(joined) == [1, 2, 0, 0, 3, 4]
assert [list(chunk) for chunk in chunks] == [[1, 2], [3, 4]]
```

The tuple-like projection adaptors mirror C++ `elements`, `keys`, and `values`:

```python
from rangeslib import Elements, Keys, Values

pairs = [("a", 1), ("b", 2)]
assert list(Elements(0)(pairs)) == ["a", "b"]
assert list(Keys()(pairs)) == ["a", "b"]
assert list(Values()(pairs)) == [1, 2]
```

`Enumerate` adds indexes, `Counted` takes a bounded prefix from an iterable,
and `Concat` appends additional iterables to the piped input:

```python
from rangeslib import Concat, Counted, Enumerate

assert list(Counted(2)(value for value in [10, 20, 30])) == [10, 20]
assert list(Enumerate(1)(["a", "b"])) == [(1, "a"), (2, "b")]
assert list(Concat([3, 4])([1, 2])) == [1, 2, 3, 4]
```

Or they can be composed with a `Range` using the pipe operator:

```python
from rangeslib import Filter, Iota, Reverse, Take

result = Iota(1, 7) | Reverse() | Filter(lambda value: value % 2 == 0) | Take(2)
assert list(result) == [6, 4]
```

`To` finishes a pipeline by converting its input with any compatible callable:

```python
from rangeslib import Iota, To

as_list = Iota(1, 4) | To(list)
as_tuple = Iota(1, 4) | To(tuple)

assert as_list == [1, 2, 3]
assert as_tuple == (1, 2, 3)
```

## Public API

Import public classes from `rangeslib`:

```python
from rangeslib import Range, RangeAdaptor, RangeGenerator, Ranges
```

The implementation is organized into private modules under `rangeslib`:

- `_core.py` contains the core container and base types
- `_generators.py` contains range source generators
- `_adaptors.py` contains iterable transformations
- `__init__.py` defines the supported public exports

The `Ranges` namespace is also available when a grouped API is preferred:

```python
from rangeslib import Ranges

values = Ranges.Iota(1, 4) | Ranges.Transform(str)
```

## Testing

Run the complete test suite with:

```bash
./run_tests.sh
```

The same tests run automatically on every push through the workflow in `.github/workflows/tests.yml`.
