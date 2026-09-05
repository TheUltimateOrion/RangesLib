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

Create and activate a virtual environment, then install the development tools:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

### Format code locally

`scripts/format.sh` is the mutating developer command. It applies Ruff's safe automatic
lint fixes and then formats every Python file Ruff discovers in the repository:

```bash
./scripts/format.sh
```

CI never runs this command because CI should not silently modify source code.

### Run the local quality gate

`scripts/check.sh` is the read-only source-quality gate used by the complete
CI check. It checks the whole repository with Ruff, checks formatting, runs
both mypy and Pyright, and runs the
test suite with branch coverage:

```bash
./scripts/check.sh
```

It may create ignored artifacts such as `.coverage`, but it does not rewrite
tracked source files.

Run the complete release-quality gate, including a Sphinx build with warnings
as errors, with:

```bash
./scripts/check_all.sh
```

For a fast static-type-only pass, run:

```bash
./scripts/typecheck.sh
```

Ruff checks syntax, style, and common quality issues. Mypy and Pyright both
check static types: they deliberately use separate type-checking engines, so a
change must satisfy both the Python implementation and the Pylance-compatible
analyzer.

For a faster runtime-only test pass:

```bash
./scripts/run_tests.sh
```

To validate the distributable source archive and wheel in an isolated
environment:

```bash
./scripts/check_package.sh
```

Run the manual playground with:

```bash
./scripts/run_playground.sh
```

A recommended pre-push sequence is:

```bash
./scripts/format.sh
./scripts/check_all.sh
./scripts/check_package.sh
```

The same scripts are invoked by GitHub Actions, which keeps local validation and
CI behavior synchronized.

## Documentation

Build the Sphinx site with:

```bash
./scripts/generate_docs.sh
```

Generated HTML is written to `docs/_build/html/`.

Documentation deployment is gated by CI. A push to `main` first runs the
**Tests and quality** workflow. GitHub Pages is built and deployed only after
that workflow succeeds, and the deployment workflow checks out the exact commit
SHA that CI validated.

## Compatibility and releases

The project is still in the `0.x` series. Public API changes are documented in
[docs/changelog.md](docs/changelog.md) and migration notes live in
[docs/migration.md](docs/migration.md). Private modules beginning with `_` are
implementation details and are not covered by the public compatibility policy.
