# Usage

## Installation

`rangeslib` requires Python 3.12 or newer.

```bash
python -m pip install -r requirements.txt
```

## Public API

Application code should import the two public facade modules and, when needed,
the `Range` container:

```python
from rangeslib import Range, ranges, views
```

Implementation modules beginning with `_` are private and should not be
imported by applications.

## Generators

The `ranges` module creates eager `Range` values:

```python
from rangeslib import ranges

assert list(ranges.empty()) == []
assert list(ranges.single(7)) == [7]
assert list(ranges.iota(1, 4)) == [1, 2, 3]
assert list(ranges.indices(3)) == [0, 1, 2]
assert list(ranges.repeat("x", 3)) == ["x", "x", "x"]
```

## Pipelines

The `views` module provides lowercase adaptor factories. They can start a
pipeline from any iterable because adaptors implement reflected `|` dispatch:

```python
from rangeslib import ranges, views

result = (
    ranges.iota(1, 7)
    | views.reverse()
    | views.filter(lambda value: value % 2 == 0)
    | views.transform(lambda value: value * 10)
    | views.take(2)
)

assert list(result) == [60, 40]
```

Strings, lists, generators, and built-in `range` values work too:

```python
from rangeslib import views

text = "abcdef" | views.take(3) | views.to("".join)
assert text == "abc"
```

## Adaptor catalog

- `filter`, `transform`, `take`, `takewhile`, `drop`, and `dropwhile` process values.
- `counted` consumes a bounded prefix, including from a partially consumed iterator.
- `elements`, `keys`, and `values` project indexed tuple-like elements.
- `enumerate` adds indexes; `concat` appends iterables.
- `zip` and `zip_transform` combine corresponding values.
- `adjacent`, `pairwise`, `slide`, and their transform variants create windows.
- `chunk` creates non-overlapping groups; `chunk_by` splits between values.
- `stride` selects every Nth value; `cartesian_product` creates combinations.
- `join`, `join_with`, and `split` handle nested values and separator patterns.
- `to` converts the final iterable to a collection or custom result.

All results are eager. Most adaptors return `Range`; `to` returns the target
callable's result.
