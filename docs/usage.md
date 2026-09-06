# Usage

## Installation

`rangeslib` requires Python 3.12 or newer and has no runtime dependencies.

```bash
python -m pip install .
```

Contributor tooling is installed separately:

```bash
python -m pip install -e ".[dev]"
```

## Public API

Application code should import the public facade modules and, when needed, the
`Range` container:

```python
from rangeslib import Range, ranges, views
```

Modules beginning with `_` are private implementation details.

## Range

`Range` is an eager mutable sequence backed by `collections.UserList`.
Construction is positional:

```python
from rangeslib import Range

values = Range(1, 2, 3)
nested = Range([1, 2, 3])

assert list(values) == [1, 2, 3]
assert list(nested) == [[1, 2, 3]]
```

List-like reconstruction operations preserve `Range`:

```python
assert list(values[1:]) == [2, 3]
assert list(values + [4]) == [1, 2, 3, 4]
assert list([0] + values) == [0, 1, 2, 3]
assert list(values * 2) == [1, 2, 3, 1, 2, 3]
assert list(values.copy()) == [1, 2, 3]
```

## Generators

The `ranges` module constructs eager `Range` values.

| Factory | Result | Edge behavior |
| --- | --- | --- |
| `ranges.empty()` | empty `Range[int]` | always empty |
| `ranges.single(value)` | one-element `Range[T]` | preserves the value type |
| `ranges.iota(start, end)` | integers in `[start, end)` | same direction rules as built-in `range` |
| `ranges.indices(count)` | integers in `[0, count)` | non-positive counts are empty |
| `ranges.repeat(value, count)` | `count` copies of `value` | non-positive counts are empty |

## Pipelines

Adaptors can be called directly or placed on the right side of `|`:

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

Ordinary iterables can start pipelines because adaptors implement reflected `|`
dispatch:

```python
text = "abcdef" | views.take(3) | views.to("".join)
assert text == "abc"
```

Adaptors can also be composed and reused:

```python
pipeline = views.filter(lambda value: value % 2 == 0) | views.take(3)

assert list([1, 2, 3, 4, 5, 6] | pipeline) == [2, 4, 6]
assert list([10, 11, 12, 14] | pipeline) == [10, 12, 14]
```

## Materialization

Most adaptors return a fully materialized `Range`, making results repeatable.
`views.to` is the terminal conversion adaptor and returns the target callable's
result.

Use `views.all()` to materialize an existing iterable as a reusable `Range`. It
is the closest equivalent to C++ `views::all` in the current eager design:

```python
assert list([1, 2, 3] | views.all()) == [1, 2, 3]
assert list(("a", "b") | views.all()) == ["a", "b"]
assert list("abc" | views.all()) == ["a", "b", "c"]
```

`views.take(count)` and `views.counted(count)` stop early for non-negative
counts, so they can bound one-shot or infinite iterators. Negative `take`
intentionally follows Python slice semantics and materializes the input first.

## Adaptor Catalog

- `all`, `reverse`, `filter`, `transform`, `take`, `drop`, and `counted` process values.
- `takewhile` / `take_while` and `dropwhile` / `drop_while` process prefixes.
- `elements`, `keys`, and `values` project indexed tuple-like elements.
- `enumerate`, `concat`, `zip`, `zip_transform`, and `cartesian_product` combine values.
- `adjacent`, `pairwise`, `adjacent_transform`, and `pairwise_transform` create tuple windows.
- `chunk`, `slide`, `chunk_by`, and `stride` group or sample finite inputs.
- `join`, `join_with`, and `split` handle nested values and separator patterns.
- `to` converts the final iterable to a collection or custom result.

## Delimiters

`split` and `join_with` accept either scalar delimiters or iterable separator
patterns:

```python
assert [list(chunk) for chunk in [1, 0, 2, 0] | views.split(0)] == [[1], [2], []]
assert [list(chunk) for chunk in [1, 0, 0, 2] | views.split([0, 0])] == [[1], [2]]
assert list([[1], [2, 3]] | views.join_with(0)) == [1, 0, 2, 3]
assert list([[1], [2, 3]] | views.join_with([0, 0])) == [1, 0, 0, 2, 3]
```

An empty `split` separator raises `ValueError` before consuming the input.
An empty `join_with` separator is valid and behaves like `join`.

## Type Checking

The installed distribution includes a `py.typed` marker. Public type assertions
are kept in `tests/typecheck/public_api.py` and run in CI with both mypy and
Pyright.

The facade preserves useful public types, including mixed two-range `zip` and
`cartesian_product`, exact `pairwise` tuples, and typed `keys` / `values` over
pair-like inputs.

## Performance Checks

For local performance measurements, run:

```bash
PYTHONPATH=src .venv/bin/python scripts/benchmark.py
```

The benchmark script is not part of CI because timing varies by machine. Use it
for comparing changes locally before and after implementation work.
