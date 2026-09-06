# rangeslib

[![Tests and quality](https://github.com/TheUltimateOrion/RangesLib/actions/workflows/tests.yml/badge.svg)](https://github.com/TheUltimateOrion/RangesLib/actions/workflows/tests.yml)
[![Documentation](https://github.com/TheUltimateOrion/RangesLib/actions/workflows/docs.yml/badge.svg)](https://theultimateorion.github.io/RangesLib/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

`rangeslib` is a typed Python library for eager, C++-inspired range pipelines.
The public API is intentionally small:

```python
from rangeslib import ranges, views
```

The mental model is:

```text
ranges creates values
views transforms values
views.to converts the final result
```

## Quick Start

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

`Range` values are eager and reusable. Most adaptors return another `Range`; the
terminal `views.to(...)` adaptor returns whatever collection or factory you ask
for.

## Existing Iterables

Ordinary Python iterables can start pipelines too:

```python
from rangeslib import views

text = "abcdef" | views.take(3) | views.to("".join)
assert text == "abc"

chars = "abc" | views.all()
assert list(chars) == ["a", "b", "c"]
```

`views.all()` is the eager Python counterpart to C++ `views::all`: it adapts an
existing iterable into a reusable `Range`.

## Reusable Pipelines

Adaptors can be composed before data is supplied:

```python
from rangeslib import views

first_three_even = views.filter(lambda value: value % 2 == 0) | views.take(3)

assert list([1, 2, 3, 4, 5, 6] | first_three_even) == [2, 4, 6]
assert list([10, 11, 12, 14] | first_three_even) == [10, 12, 14]
```

## Sources And Views

The `ranges` facade creates source ranges:

```python
from rangeslib import ranges

ranges.empty()
ranges.single("value")
ranges.iota(1, 5)
ranges.indices(3)
ranges.repeat("x", 3)
```

The `views` facade contains transformations such as:

```text
all, reverse, filter, transform, take, drop, counted,
elements, keys, values, enumerate, concat, zip, cartesian_product,
adjacent, pairwise, chunk, slide, stride, join, split, to
```

See [docs/usage.md](docs/usage.md) for the full API catalog.

## C++ Ranges Correspondence

`rangeslib` borrows naming and broad behavior from C++20/23/26 ranges, but it
is not a lazy C++ view implementation. The most important differences are:

- Python iterables replace C++ iterator/sentinel pairs.
- `Range` stores eager values instead of reference-like lazy views.
- Tuple results are ordinary Python tuples, not tuples of references.
- Python type checking is useful but cannot express every C++ tuple-like rule.

See [docs/cpp-comparison.md](docs/cpp-comparison.md) for details.

## Installation

Python 3.12 or newer is required.

```bash
python -m pip install .
```

For development:

```bash
python -m pip install -e ".[dev]"
```

`rangeslib` has no runtime dependencies.

## Development

Useful commands live in `scripts/`:

```bash
./scripts/run_tests.sh       # tests only
./scripts/typecheck.sh       # mypy + Pyright
./scripts/check.sh           # Ruff, typing, tests, coverage
./scripts/check_all.sh       # check.sh + strict Sphinx docs
./scripts/check_package.sh   # sdist/wheel build and install smoke test
./scripts/run_playground.sh  # manual playground
```

Before a release commit, run:

```bash
./scripts/check_all.sh
./scripts/check_package.sh
```

## Documentation

Build the Sphinx site with:

```bash
./scripts/generate_docs.sh
```

Generated HTML is written to `docs/_build/html/` and published to GitHub Pages
after CI succeeds on `main`.

## Releases

Changing `[project].version` in `pyproject.toml` on `main` automatically runs
the complete quality and package checks, then creates the matching Git tag and
GitHub Release and publishes the distribution to PyPI through Trusted
Publishing after the PyPI project is configured.

For future work, prefer opening or collecting issues before adding more adaptors
immediately. See [docs/roadmap.md](docs/roadmap.md).

See [docs/publishing.md](docs/publishing.md) for the PyPI setup checklist.
