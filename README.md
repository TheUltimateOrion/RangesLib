# rangeslib

A typed Python library for composing eager ranges and iterable transformations with readable pipeline syntax.

```python
from rangeslib import ranges, views

result = (
    ranges.iota(1, 11)
    | views.filter(lambda value: value % 2 == 0)
    | views.transform(lambda value: value * 10)
    | views.take(3)
    | views.to(list)
)

assert result == [20, 40, 60]
```

## Features

- Lowercase `ranges` and `views` facade for normal application code
- Typed, list-like `Range` values
- Sources: `empty`, `single`, `iota`, `indices`, and `repeat`
- Transformations: filtering, mapping, slicing, windows, chunks, joins, zips, and products
- Pipelines starting from `Range`, `list`, `str`, `range`, and other iterables
- Eager, predictable results with standard Python collection behavior
- Sphinx documentation and GitHub Pages deployment

## Installation

Python 3.12 or newer is required.

```bash
python -m pip install -r requirements.txt
```

## Usage

Create source ranges with `ranges`:

```python
from rangeslib import ranges

assert list(ranges.empty()) == []
assert list(ranges.single(7)) == [7]
assert list(ranges.iota(2, 5)) == [2, 3, 4]
assert list(ranges.indices(3)) == [0, 1, 2]
assert list(ranges.repeat("x", 3)) == ["x", "x", "x"]
```

Compose transformations with `views`:

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

Ordinary Python iterables can start pipelines too:

```python
from rangeslib import views

text = "abcdef" | views.take(3) | views.to("".join)
assert text == "abc"
```

See [docs/usage.md](docs/usage.md) for the complete adaptor catalog and
[docs/architecture.md](docs/architecture.md) for implementation details.

## Testing

Run all tests with:

```bash
./run_tests.sh
```

Run the manual playground with:

```bash
./run_playground.sh
```

## Documentation

Install the documentation dependencies and build the Sphinx site:

```bash
python -m pip install -r requirements.txt
./generate_docs.sh
```

The generated HTML is written to `docs/_build/html/`. Documentation is
published automatically to GitHub Pages when changes are pushed to `main`.
