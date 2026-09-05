# Usage

## Installation

`rangeslib` requires Python 3.12 or newer. Install the package and its
documentation dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Public imports

Import supported names from the package root:

```python
from rangeslib import Filter, Iota, Take, To, Transform
```

Private modules beginning with `_` are implementation details and should not be imported by applications.

The recommended everyday API uses the lowercase `ranges` and `views` modules:

```python
from rangeslib import ranges, views

result = ranges.iota(1, 6) | views.filter(lambda value: value % 2 == 0) | views.take(2)
assert list(result) == [2, 4]
```

The uppercase class-based API remains available for advanced use and
backward compatibility.

## Generators

Generators create `Range` values:

```python
from rangeslib import Empty, Indices, Iota, Repeat, Single

Empty()                  # Range()
Single(7)                # Range(7)
Iota(1, 4)               # Range(1, 2, 3)
Indices(3)               # Range(0, 1, 2)
Repeat("x", 3)           # Range("x", "x", "x")
```

## Pipelines

Adaptors can be chained with `|`. A `Range` supports the left-hand operation, and adaptors implement reflected dispatch so ordinary iterables can start a pipeline too:

```python
from rangeslib import Filter, Take, Transform

result = "12345" | Filter(lambda value: value != "3") | Transform(int) | Take(3)
assert list(result) == [1, 2, 4]
```

Most adaptors return an eager `Range`. `To` is the terminal conversion adaptor:

```python
from rangeslib import Iota, To

result = Iota(1, 4) | To(tuple)
assert result == (1, 2, 3)
```

## Iterable requirements

Adaptors accept any iterable unless their operation needs a more specific shape:

- `Elements`, `Keys`, and `Values` need indexable tuple-like elements.
- `Join` and `JoinWith` need an iterable of inner iterables.
- `Zip`, `ZipTransform`, and `CartesianProduct` need additional iterables.
- `Split` needs a non-empty separator pattern.

The implementation currently materializes results into `Range`, so it is eager rather than a lazy C++-style view.
