# rangeslib

`rangeslib` is a typed Python library for composing eager ranges and iterable
transformations with readable pipeline syntax.

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

- Small public API: `Range`, `ranges`, and `views`
- Typed, list-like `Range` values with normal slicing, copying, concatenation,
  and multiplication behavior
- Sources: `empty`, `single`, `iota`, `indices`, and `repeat`
- Adaptors for filtering, mapping, slicing, windows, chunks, joins, zips,
  products, projection, and conversion
- Pipelines starting from `Range`, `list`, `str`, built-in `range`, generators,
  and other iterables
- Eager and explicit result materialization, with bounded consumption for
  operations such as positive `take` and `counted`
- Inline typing metadata (`py.typed`), static type checking, API contract tests,
  Sphinx documentation, and package-build validation in CI

## Requirements

Python 3.12 or newer is required.

## Installation

From a source checkout, install the runtime package with:

```bash
python -m pip install .
```

For local development, install the contributor toolchain instead:

```bash
python -m pip install -e ".[dev]"
```

`rangeslib` has no runtime dependencies.

## Usage

Create source ranges with `ranges`:

```python
from rangeslib import ranges

assert list(ranges.empty()) == []
assert list(ranges.single("value")) == ["value"]
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

`Range` intentionally uses positional construction. `Range(1, 2, 3)` contains
three values, while `Range([1, 2, 3])` contains one list value. List-like
operations still return flat `Range` objects:

```python
from rangeslib import Range

values = Range(1, 2, 3)
assert list(values[1:]) == [2, 3]
assert list(values + [4]) == [1, 2, 3, 4]
assert list(values * 2) == [1, 2, 3, 1, 2, 3]
```

See [docs/usage.md](docs/usage.md) for the public API behavior contract and
[docs/architecture.md](docs/architecture.md) for the design and maintenance
invariants.

## Development

Run the complete unit suite:

```bash
./run_tests.sh
```

Run coverage with the same threshold used by CI:

```bash
coverage run -m unittest discover -s tests
coverage report
```

Run the manual playground:

```bash
./run_playground.sh
```

After installing `.[dev]`, the full local quality gate is:

```bash
ruff check src tests
ruff format --check src
mypy src/rangeslib tests/typecheck/public_api.py
coverage run -m unittest discover -s tests
coverage report
python -m sphinx -W --keep-going -b html docs docs/_build/html
python -m build
```

## Documentation

Build the Sphinx site with:

```bash
./generate_docs.sh
```

Generated HTML is written to `docs/_build/html/`. Documentation is published
to GitHub Pages from `main`.

## Compatibility and releases

The project is still in the `0.x` series. Public API changes are documented in
[docs/changelog.md](docs/changelog.md) and migration notes live in
[docs/migration.md](docs/migration.md). Private modules beginning with `_` are
implementation details and are not covered by the public compatibility policy.
